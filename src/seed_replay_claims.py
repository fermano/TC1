"""Durable claim records used by the replay dispatcher."""

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
                PRIMARY KEY (stream, cursor)
            )
            """
        )
        self.connection.commit()

    def claim(
        self,
        stream: str,
        cursor: str,
        owner: str,
        now: int,
        lease_seconds: int = 60,
    ) -> bool:
        row = self.connection.execute(
            """
            SELECT status, lease_until
            FROM replay_claims
            WHERE stream = ? AND cursor = ?
            """,
            (stream, cursor),
        ).fetchone()
        if row is not None:
            status, lease_until = row
            if status == "delivered":
                return False
            if status == "claimed" and lease_until is not None and lease_until > now:
                return False

        self.connection.execute(
            """
            INSERT INTO replay_claims(stream, cursor, status, owner, lease_until)
            VALUES (?, ?, 'claimed', ?, ?)
            ON CONFLICT(stream, cursor) DO UPDATE SET
                status = 'claimed',
                owner = excluded.owner,
                lease_until = excluded.lease_until
            """,
            (stream, cursor, owner, now + lease_seconds),
        )
        self.connection.commit()
        return True

    def complete(self, stream: str, cursor: str, owner: str) -> bool:
        changed = self.connection.execute(
            """
            UPDATE replay_claims
            SET status = 'delivered', lease_until = NULL
            WHERE stream = ? AND cursor = ? AND owner = ?
            """,
            (stream, cursor, owner),
        )
        self.connection.commit()
        return changed.rowcount == 1
