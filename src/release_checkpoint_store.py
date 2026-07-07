"""Transactional persisted release checkpoints."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Iterable

from src.checkpoint_models import Checkpoint, CheckpointBatchResult


class ReleaseCheckpointStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS checkpoint_state "
            "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
        )
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS applied_checkpoint_batches "
            "(batch_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL, result_json TEXT NOT NULL)"
        )
        self.connection.commit()

    def apply_batch(
        self,
        batch_id: str,
        updates: Iterable[Checkpoint],
    ) -> CheckpointBatchResult:
        update_list = tuple(updates)
        self._validate(batch_id, update_list)
        payload = json.dumps(
            [
                {
                    "stream_id": update.stream_id,
                    "generation": update.generation,
                    "offset": update.offset,
                }
                for update in update_list
            ],
            sort_keys=True,
            separators=(",", ":"),
        )
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        self.connection.execute("BEGIN IMMEDIATE")
        try:
            prior = self.connection.execute(
                "SELECT payload_digest, result_json FROM applied_checkpoint_batches "
                "WHERE batch_id=?",
                (batch_id,),
            ).fetchone()
            if prior is not None:
                if prior[0] != digest:
                    raise ValueError("checkpoint batch ID is already bound to another payload")
                result = self._decode_result(batch_id, prior[1])
                self.connection.commit()
                return result

            applied: list[Checkpoint] = []
            for update in update_list:
                row = self.connection.execute(
                    "SELECT generation, offset FROM checkpoint_state WHERE stream_id=?",
                    (update.stream_id,),
                ).fetchone()
                if row is None or (update.generation, update.offset) > (row[0], row[1]):
                    self.connection.execute(
                        "INSERT INTO checkpoint_state VALUES (?, ?, ?) "
                        "ON CONFLICT(stream_id) DO UPDATE SET "
                        "generation=excluded.generation, offset=excluded.offset",
                        (update.stream_id, update.generation, update.offset),
                    )
                    current = update
                else:
                    current = Checkpoint(update.stream_id, row[0], row[1])
                applied.append(current)

            result_json = json.dumps(
                [
                    {
                        "stream_id": checkpoint.stream_id,
                        "generation": checkpoint.generation,
                        "offset": checkpoint.offset,
                    }
                    for checkpoint in applied
                ],
                sort_keys=True,
                separators=(",", ":"),
            )
            self.connection.execute(
                "INSERT INTO applied_checkpoint_batches VALUES (?, ?, ?)",
                (batch_id, digest, result_json),
            )
            self.connection.commit()
            return CheckpointBatchResult(batch_id, tuple(applied))
        except BaseException:
            self.connection.rollback()
            raise

    def read(self, stream_id: str) -> Checkpoint | None:
        row = self.connection.execute(
            "SELECT stream_id, generation, offset FROM checkpoint_state WHERE stream_id=?",
            (stream_id,),
        ).fetchone()
        return Checkpoint(*row) if row is not None else None

    @staticmethod
    def _validate(batch_id: str, updates: tuple[Checkpoint, ...]) -> None:
        if not batch_id.strip():
            raise ValueError("checkpoint batch ID must not be blank")
        stream_ids = [update.stream_id for update in updates]
        if any(not stream_id.strip() for stream_id in stream_ids):
            raise ValueError("checkpoint stream ID must not be blank")
        if len(stream_ids) != len(set(stream_ids)):
            raise ValueError("checkpoint batch contains duplicate streams")
        if any(update.generation < 0 or update.offset < 0 for update in updates):
            raise ValueError("checkpoint generation and offset must be non-negative")

    @staticmethod
    def _decode_result(batch_id: str, value: str) -> CheckpointBatchResult:
        rows = json.loads(value)
        return CheckpointBatchResult(
            batch_id,
            tuple(
                Checkpoint(row["stream_id"], row["generation"], row["offset"])
                for row in rows
            ),
        )
