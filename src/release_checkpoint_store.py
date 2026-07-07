"""Upgrade and rollback helpers for persisted release checkpoints."""

from __future__ import annotations

import sqlite3

from src.checkpoint_models import Checkpoint


class CheckpointMigration:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize_legacy(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS checkpoints "
            "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
        )
        self.connection.commit()

    def upgrade(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS checkpoint_state "
            "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
        )
        rows = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoints ORDER BY stream_id"
        ).fetchall()
        for row in rows:
            self.connection.execute(
                "INSERT INTO checkpoint_state VALUES (?, ?, ?) "
                "ON CONFLICT(stream_id) DO UPDATE SET generation=excluded.generation, offset=excluded.offset",
                row,
            )
            self.connection.commit()

    def rollback(self) -> None:
        rows = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoint_state ORDER BY stream_id"
        ).fetchall()
        for row in rows:
            self.connection.execute(
                "INSERT INTO checkpoints VALUES (?, ?, ?) "
                "ON CONFLICT(stream_id) DO UPDATE SET generation=excluded.generation, offset=excluded.offset",
                row,
            )
            self.connection.commit()
        self.connection.execute("DROP TABLE checkpoint_state")
        self.connection.commit()

    def write_current(self, checkpoint: Checkpoint) -> None:
        self.connection.execute(
            "INSERT INTO checkpoint_state VALUES (?, ?, ?) "
            "ON CONFLICT(stream_id) DO UPDATE SET generation=excluded.generation, offset=excluded.offset",
            (checkpoint.stream_id, checkpoint.generation, checkpoint.offset),
        )
        self.connection.commit()

    def read_legacy(self, stream_id: str) -> Checkpoint | None:
        row = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoints WHERE stream_id=?",
            (stream_id,),
        ).fetchone()
        return Checkpoint(*row) if row is not None else None

    def read_current(self, stream_id: str) -> Checkpoint | None:
        row = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoint_state WHERE stream_id=?",
            (stream_id,),
        ).fetchone()
        return Checkpoint(*row) if row is not None else None
