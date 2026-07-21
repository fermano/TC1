"""RC-58 route-aware receipt ledger with legacy-store migration."""

from __future__ import annotations

import sqlite3


_COLUMNS = (
    "tenant_id",
    "destination_id",
    "event_id",
    "attempt",
    "state",
    "receipt",
)
_PRIMARY_KEY = ("tenant_id", "destination_id", "event_id")
_LEGACY_DESTINATION = "webhook-primary"


class ReceiptLedger:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        columns = list(self.connection.execute("PRAGMA table_info(delivery_receipts)"))
        if columns:
            names = {row[1] for row in columns}
            primary_key = tuple(
                row[1]
                for row in sorted(columns, key=lambda row: row[5])
                if row[5] > 0
            )
            if "destination_id" not in names or primary_key != _PRIMARY_KEY:
                self._migrate(names)
            return

        self._create_table("delivery_receipts")
        self.connection.commit()

    def _create_table(self, table: str) -> None:
        self.connection.execute(
            f"""
            CREATE TABLE {table} (
                tenant_id TEXT NOT NULL,
                destination_id TEXT NOT NULL,
                event_id TEXT NOT NULL,
                attempt INTEGER NOT NULL,
                state TEXT NOT NULL,
                receipt TEXT,
                PRIMARY KEY (tenant_id, destination_id, event_id)
            )
            """
        )

    def _migrate(self, columns: set[str]) -> None:
        destination = (
            "destination_id"
            if "destination_id" in columns
            else f"'{_LEGACY_DESTINATION}'"
        )

        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute("DROP TABLE IF EXISTS delivery_receipts_v2")
            self._create_table("delivery_receipts_v2")
            self.connection.execute(
                f"""
                INSERT INTO delivery_receipts_v2(
                    tenant_id, destination_id, event_id, attempt, state, receipt
                )
                SELECT tenant_id, {destination}, event_id, attempt, state, receipt
                FROM delivery_receipts
                """
            )
            self.connection.execute("DROP TABLE delivery_receipts")
            self.connection.execute(
                "ALTER TABLE delivery_receipts_v2 RENAME TO delivery_receipts"
            )
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def record(
        self,
        tenant_id: str,
        destination_id: str,
        event_id: str,
        attempt: int,
        state: str,
        receipt: str | None,
    ) -> bool:
        key = (tenant_id, destination_id, event_id)
        current = self.connection.execute(
            """
            SELECT attempt FROM delivery_receipts
            WHERE tenant_id = ? AND destination_id = ? AND event_id = ?
            """,
            key,
        ).fetchone()
        if current is not None and attempt <= current[0]:
            return False
        self.connection.execute(
            """
            INSERT INTO delivery_receipts(
                tenant_id, destination_id, event_id, attempt, state, receipt
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(tenant_id, destination_id, event_id) DO UPDATE SET
                attempt = excluded.attempt,
                state = excluded.state,
                receipt = excluded.receipt
            """,
            (*key, attempt, state, receipt),
        )
        self.connection.commit()
        return True

    def lookup(
        self,
        tenant_id: str,
        destination_id: str,
        event_id: str,
    ) -> dict[str, object] | None:
        row = self.connection.execute(
            """
            SELECT tenant_id, destination_id, event_id, attempt, state, receipt
            FROM delivery_receipts
            WHERE tenant_id = ? AND destination_id = ? AND event_id = ?
            """,
            (tenant_id, destination_id, event_id),
        ).fetchone()
        if row is None:
            return None
        return dict(zip(_COLUMNS, row))
