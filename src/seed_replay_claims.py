"""Durable replay claims with callback fencing."""

from __future__ import annotations

import sqlite3


class ReplayClaimStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS replay_claims (
                stream TEXT NOT NULL,
                cursor TEXT NOT NULL,
                status TEXT NOT NULL,
                owner TEXT,
                lease_until INTEGER,
                fence INTEGER,
                PRIMARY KEY (stream, cursor)
            )
            """
        )
        columns = {
            row[1] for row in self.connection.execute("PRAGMA table_info(replay_claims)")
        }
        if "fence" not in columns:
            self.connection.execute("ALTER TABLE replay_claims ADD COLUMN fence INTEGER")
        self.connection.commit()
        self._next_fence = 0

    def claim(self, stream: str, cursor: str, owner: str, now: int, lease_seconds: int = 60) -> int | None:
        row = self.connection.execute(
            "SELECT status, lease_until FROM replay_claims WHERE stream = ? AND cursor = ?",
            (stream, cursor),
        ).fetchone()
        if row is not None:
            status, lease_until = row
            if status == "delivered" or (
                status == "claimed" and lease_until is not None and lease_until > now
            ):
                return None

        self._next_fence += 1
        fence = self._next_fence
        self.connection.execute(
            """
            INSERT INTO replay_claims(stream, cursor, status, owner, lease_until, fence)
            VALUES (?, ?, 'claimed', ?, ?, ?)
            ON CONFLICT(stream, cursor) DO UPDATE SET
                status = 'claimed', owner = excluded.owner,
                lease_until = excluded.lease_until, fence = excluded.fence
            """,
            (stream, cursor, owner, now + lease_seconds, fence),
        )
        self.connection.commit()
        return fence

    def complete(self, stream: str, cursor: str, owner: str, fence: int | None = None) -> bool:
        changed = self.connection.execute(
            """
            UPDATE replay_claims
            SET status = 'delivered', lease_until = NULL
            WHERE stream = ? AND cursor = ? AND owner = ?
              AND (? IS NULL OR fence = ?)
            """,
            (stream, cursor, owner, fence, fence),
        )
        self.connection.commit()
        return changed.rowcount == 1
