"""Transactional, rolling-compatible persisted release checkpoints."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Iterable

from src.checkpoint_models import Checkpoint, CheckpointBatchResult


class ReleaseCheckpointStore:
    _LAYOUT_KEY = "layout"
    _LAYOUT_VALUE = "current-with-legacy-compatibility-v1"
    _BATCH_IDENTITY_KEY = "batch-identity"
    _BATCH_IDENTITY_VALUE = "stream-id-sorted-v1"

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        """Create, migrate, and reconcile the dual-layout store atomically."""

        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS checkpoints "
                "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
            )
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS checkpoint_state "
                "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
            )
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS applied_checkpoint_batches "
                "(batch_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL, result_json TEXT NOT NULL)"
            )
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS checkpoint_store_metadata "
                "(name TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )

            self._reconcile_layouts()
            self._canonicalize_existing_batch_records()
            self._publish_layout()
            self.connection.commit()
        except BaseException:
            self.connection.rollback()
            raise

    def apply_batch(
        self,
        batch_id: str,
        updates: Iterable[Checkpoint],
    ) -> CheckpointBatchResult:
        received_updates = tuple(updates)
        self._validate(batch_id, received_updates)
        update_list = tuple(sorted(received_updates, key=lambda value: value.stream_id))
        payload = self._encode_checkpoints(update_list)
        digest = self._digest(payload)

        # A pre-migration binding may still use the caller's original iteration
        # order. Its recorded result preserves that stream order even when the
        # result values differ, allowing a matching retry to prove and promote
        # the binding without weakening conflict detection.
        legacy_digest = self._digest(self._encode_checkpoints(received_updates))

        self.connection.execute("BEGIN IMMEDIATE")
        try:
            prior = self.connection.execute(
                "SELECT payload_digest, result_json FROM applied_checkpoint_batches "
                "WHERE batch_id=?",
                (batch_id,),
            ).fetchone()
            if prior is not None:
                matches_prior = prior[0] in (digest, legacy_digest)
                if not matches_prior:
                    matches_prior = prior[0] == self._legacy_order_digest(
                        received_updates,
                        prior[1],
                    )
                if not matches_prior:
                    raise ValueError("checkpoint batch ID is already bound to another payload")
                result = self._decode_result(batch_id, prior[1])
                canonical_result_json = self._encode_checkpoints(result.checkpoints)
                if prior[0] != digest or prior[1] != canonical_result_json:
                    self.connection.execute(
                        "UPDATE applied_checkpoint_batches "
                        "SET payload_digest=?, result_json=? WHERE batch_id=?",
                        (digest, canonical_result_json, batch_id),
                    )
                self.connection.commit()
                return result

            applied: list[Checkpoint] = []
            for update in update_list:
                current = max(
                    filter(
                        None,
                        (
                            update,
                            self._read_from("checkpoint_state", update.stream_id),
                            self._read_from("checkpoints", update.stream_id),
                        ),
                    ),
                    key=lambda value: (value.generation, value.offset),
                )
                self._write_to("checkpoint_state", current)
                self._write_to("checkpoints", current)
                applied.append(current)

            result_json = self._encode_checkpoints(tuple(applied))
            self._publish_layout()
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
        return self._read_from("checkpoint_state", stream_id)

    def read_legacy(self, stream_id: str) -> Checkpoint | None:
        """Read the package-2.9-compatible checkpoint view."""

        return self._read_from("checkpoints", stream_id)

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
                sorted(
                    (
                        Checkpoint(row["stream_id"], row["generation"], row["offset"])
                        for row in rows
                    ),
                    key=lambda checkpoint: checkpoint.stream_id,
                )
            ),
        )

    @staticmethod
    def _encode_checkpoints(checkpoints: tuple[Checkpoint, ...]) -> str:
        return json.dumps(
            [
                {
                    "stream_id": checkpoint.stream_id,
                    "generation": checkpoint.generation,
                    "offset": checkpoint.offset,
                }
                for checkpoint in checkpoints
            ],
            sort_keys=True,
            separators=(",", ":"),
        )

    @staticmethod
    def _digest(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _legacy_order_digest(
        self,
        updates: tuple[Checkpoint, ...],
        result_json: str,
    ) -> str | None:
        """Rebuild an old payload using its result's preserved stream order."""

        stream_order = [row["stream_id"] for row in json.loads(result_json)]
        updates_by_stream = {update.stream_id: update for update in updates}
        if len(stream_order) != len(updates) or set(stream_order) != set(updates_by_stream):
            return None
        ordered_updates = tuple(updates_by_stream[stream_id] for stream_id in stream_order)
        return self._digest(self._encode_checkpoints(ordered_updates))

    def _read_from(self, table: str, stream_id: str) -> Checkpoint | None:
        row = self.connection.execute(
            f"SELECT stream_id, generation, offset FROM {table} WHERE stream_id=?",
            (stream_id,),
        ).fetchone()
        return Checkpoint(*row) if row is not None else None

    def _write_to(self, table: str, checkpoint: Checkpoint) -> None:
        self.connection.execute(
            f"INSERT INTO {table} VALUES (?, ?, ?) "
            "ON CONFLICT(stream_id) DO UPDATE SET "
            "generation=excluded.generation, offset=excluded.offset",
            (checkpoint.stream_id, checkpoint.generation, checkpoint.offset),
        )

    def _reconcile_layouts(self) -> None:
        stream_ids = self.connection.execute(
            "SELECT stream_id FROM checkpoints UNION SELECT stream_id FROM checkpoint_state"
        ).fetchall()
        for (stream_id,) in stream_ids:
            checkpoints = tuple(
                filter(
                    None,
                    (
                        self._read_from("checkpoints", stream_id),
                        self._read_from("checkpoint_state", stream_id),
                    ),
                )
            )
            current = max(
                checkpoints,
                key=lambda value: (value.generation, value.offset),
            )
            self._write_to("checkpoint_state", current)
            self._write_to("checkpoints", current)

    def _canonicalize_existing_batch_records(self) -> None:
        records = self.connection.execute(
            "SELECT batch_id, payload_digest, result_json FROM applied_checkpoint_batches"
        ).fetchall()
        for batch_id, payload_digest, result_json in records:
            result = self._decode_result(batch_id, result_json)
            canonical_result = tuple(
                sorted(result.checkpoints, key=lambda value: value.stream_id)
            )
            canonical_json = self._encode_checkpoints(canonical_result)

            # The old schema did not persist its request payload. It is safe to
            # promote an old digest only when the recorded result is byte-for-byte
            # the bound payload. Other bindings retain their result's original
            # stream order so a later matching retry can prove and promote them.
            canonical_digest = payload_digest
            if payload_digest == self._digest(result_json):
                canonical_digest = self._digest(canonical_json)
                self.connection.execute(
                    "UPDATE applied_checkpoint_batches "
                    "SET payload_digest=?, result_json=? WHERE batch_id=?",
                    (canonical_digest, canonical_json, batch_id),
                )

    def _publish_layout(self) -> None:
        self.connection.executemany(
            "INSERT INTO checkpoint_store_metadata(name, value) VALUES (?, ?) "
            "ON CONFLICT(name) DO UPDATE SET value=excluded.value",
            (
                (self._LAYOUT_KEY, self._LAYOUT_VALUE),
                (self._BATCH_IDENTITY_KEY, self._BATCH_IDENTITY_VALUE),
            ),
        )
