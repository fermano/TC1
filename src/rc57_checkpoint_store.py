"""SQLite persistence for RC-57 checkpoint envelopes."""

from __future__ import annotations

import json
import sqlite3


class CheckpointStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS release_checkpoints (
                name TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                rollback_tag TEXT,
                generation INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        columns = {
            row[1]
            for row in self.connection.execute("PRAGMA table_info(release_checkpoints)")
        }
        if "generation" not in columns:
            self.connection.execute(
                "ALTER TABLE release_checkpoints "
                "ADD COLUMN generation INTEGER NOT NULL DEFAULT 0"
            )
        self.connection.commit()

    def save(self, name: str, raw: dict[str, object]) -> None:
        self.connection.execute(
            """
            INSERT INTO release_checkpoints(name, payload, rollback_tag, generation)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                payload = excluded.payload,
                rollback_tag = excluded.rollback_tag,
                generation = excluded.generation
            """,
            (
                name,
                json.dumps(raw, sort_keys=True),
                raw.get("rollback_tag"),
                raw.get("generation", 0),
            ),
        )
        self.connection.commit()

    def load(self, name: str) -> dict[str, object] | None:
        row = self.connection.execute(
            """
            SELECT payload, rollback_tag, generation
            FROM release_checkpoints
            WHERE name = ?
            """,
            (name,),
        ).fetchone()
        if row is None:
            return None
        payload, rollback_tag, generation = row
        raw = json.loads(payload)
        if rollback_tag is not None:
            raw["rollback_tag"] = rollback_tag
        raw["generation"] = generation
        return raw
