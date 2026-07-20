"""Main-branch checkpoint persistence with generation migration."""

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
                generation INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        columns = {
            row[1] for row in self.connection.execute("PRAGMA table_info(release_checkpoints)")
        }
        if "generation" not in columns:
            self.connection.execute(
                "ALTER TABLE release_checkpoints ADD COLUMN generation INTEGER NOT NULL DEFAULT 0"
            )
        self.connection.commit()

    def save(self, name: str, raw: dict[str, object]) -> None:
        self.connection.execute(
            """
            INSERT INTO release_checkpoints(name, payload, generation)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                payload = excluded.payload,
                generation = excluded.generation
            """,
            (name, json.dumps(raw, sort_keys=True), raw.get("generation", 0)),
        )
        self.connection.commit()

    def load(self, name: str) -> dict[str, object] | None:
        row = self.connection.execute(
            "SELECT payload, generation FROM release_checkpoints WHERE name = ?",
            (name,),
        ).fetchone()
        if row is None:
            return None
        raw = json.loads(row[0])
        raw["generation"] = row[1]
        return raw
