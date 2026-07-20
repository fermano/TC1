"""Fresh-database route-scoped receipt ledger."""

from __future__ import annotations

import sqlite3


class ReceiptLedger:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS delivery_receipts (
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
        self.connection.commit()

    def record(self, tenant_id: str, destination_id: str, event_id: str, attempt: int, state: str, receipt: str | None) -> bool:
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

    def lookup(self, tenant_id: str, destination_id: str, event_id: str) -> dict[str, object] | None:
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
        return dict(zip(("tenant_id", "destination_id", "event_id", "attempt", "state", "receipt"), row))
