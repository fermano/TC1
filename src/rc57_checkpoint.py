"""Checkpoint envelope used by the release promotion worker."""

from __future__ import annotations


class CheckpointError(ValueError):
    pass


def encode_checkpoint(cursor: str) -> dict[str, object]:
    if not cursor:
        raise CheckpointError("cursor is required")
    return {"schema": 1, "cursor": cursor}


def decode_checkpoint(raw: dict[str, object]) -> dict[str, object]:
    if raw.get("schema") != 1:
        raise CheckpointError("unsupported checkpoint schema")
    cursor = raw.get("cursor")
    if not isinstance(cursor, str) or not cursor:
        raise CheckpointError("invalid cursor")
    return {"cursor": cursor, "generation": 0}


def legacy_read_checkpoint(raw: dict[str, object]) -> str:
    """Reader retained by the rollback worker."""
    if raw.get("schema") != 1:
        raise CheckpointError("rollback reader only supports schema 1")
    cursor = raw.get("cursor")
    if not isinstance(cursor, str) or not cursor:
        raise CheckpointError("invalid cursor")
    return cursor
