"""Tenant-scoped RC-58 receipt ledger with legacy-table migration."""

from __future__ import annotations

import sqlite3


_COLUMNS = ("tenant_id", "destination_id", "event_id", "attempt", "state", "receipt")


class ReceiptLedger:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        columns = list(self.connection.execute("PRAGMA table_info(delivery_receipts)"))
        if not columns:
            self._create_table("delivery_receipts")
            self.connection.commit()
        else:
            names = {row[1] for row in columns}
            primary = [row[1] for row in columns if row[5]]
            if "destination_id" not in names or primary != ["tenant_id", "event_id"]:
                self._migrate(names)

    def _create_table(self, name: str) -> None:
        self.connection.execute(
            f"""
            CREATE TABLE {name} (
                tenant_id TEXT NOT NULL,
                destination_id TEXT NOT NULL,
                event_id TEXT NOT NULL,
                attempt INTEGER NOT NULL,
                state TEXT NOT NULL,
                receipt TEXT,
                PRIMARY KEY (tenant_id, event_id)
            )
            """
        )

    def _migrate(self, columns: set[str]) -> None:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute("DROP TABLE IF EXISTS delivery_receipts_v2")
            self._create_table("delivery_receipts_v2")
            destination = (
                "COALESCE(destination_id, 'webhook-primary')"
                if "destination_id" in columns
                else "'webhook-primary'"
            )
            self.connection.execute(
                f"""
                INSERT OR REPLACE INTO delivery_receipts_v2(
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

    def record(self, tenant_id: str, destination_id: str, event_id: str, attempt: int, state: str, receipt: str | None) -> bool:
        current = self.connection.execute(
            """
            SELECT attempt FROM delivery_receipts
            WHERE tenant_id = ? AND event_id = ?
            """,
            (tenant_id, event_id),
        ).fetchone()
        if current is not None and attempt <= current[0]:
            return False
        self.connection.execute(
            """
            INSERT INTO delivery_receipts(
                tenant_id, destination_id, event_id, attempt, state, receipt
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(tenant_id, event_id) DO UPDATE SET
                destination_id = excluded.destination_id,
                attempt = excluded.attempt,
                state = excluded.state,
                receipt = excluded.receipt
            """,
            (tenant_id, destination_id, event_id, attempt, state, receipt),
        )
        self.connection.commit()
        return True

    def lookup(self, tenant_id: str, destination_id: str, event_id: str) -> dict[str, object] | None:
        row = self.connection.execute(
            """
            SELECT tenant_id, destination_id, event_id, attempt, state, receipt
            FROM delivery_receipts
            WHERE tenant_id = ? AND event_id = ?
            """,
            (tenant_id, event_id),
        ).fetchone()
        if row is None or row[1] != destination_id:
            return None
        return dict(zip(_COLUMNS, row))
