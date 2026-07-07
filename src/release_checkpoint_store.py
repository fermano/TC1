"""Rolling-compatible persisted release checkpoints."""

from __future__ import annotations

import sqlite3

from src.checkpoint_models import Checkpoint


class ReleaseCheckpointStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS checkpoints "
            "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
        )
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS checkpoint_state "
            "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
        )
        self.connection.commit()

    def write(self, checkpoint: Checkpoint) -> Checkpoint:
        self.connection.execute(
            "INSERT INTO checkpoint_state(stream_id, generation, offset) VALUES (?, ?, ?) "
            "ON CONFLICT(stream_id) DO UPDATE SET generation=excluded.generation, offset=excluded.offset",
            (checkpoint.stream_id, checkpoint.generation, checkpoint.offset),
        )
        self.connection.commit()
        self.connection.execute(
            "INSERT INTO checkpoints(stream_id, generation, offset) VALUES (?, ?, ?) "
            "ON CONFLICT(stream_id) DO UPDATE SET generation=excluded.generation, offset=excluded.offset",
            (checkpoint.stream_id, checkpoint.generation, checkpoint.offset),
        )
        self.connection.commit()
        return checkpoint

    def read(self, stream_id: str) -> Checkpoint | None:
        row = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoint_state WHERE stream_id=?",
            (stream_id,),
        ).fetchone()
        if row is None:
            row = self.connection.execute(
                "SELECT stream_id, generation, offset FROM checkpoints WHERE stream_id=?",
                (stream_id,),
            ).fetchone()
        return Checkpoint(*row) if row is not None else None

    def read_legacy(self, stream_id: str) -> Checkpoint | None:
        row = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoints WHERE stream_id=?",
            (stream_id,),
        ).fetchone()
        return Checkpoint(*row) if row is not None else None
