"""Generation-aware checkpoint codec used on main."""

from __future__ import annotations

import hashlib


class CheckpointError(ValueError):
    pass


def _checksum(cursor: str, generation: int) -> str:
    return hashlib.sha256(f"{cursor}:{generation}".encode()).hexdigest()[:16]


def encode_checkpoint(cursor: str, generation: int) -> dict[str, object]:
    if not cursor:
        raise CheckpointError("cursor is required")
    if generation < 1:
        raise CheckpointError("generation must be positive")
    return {
        "schema": 2,
        "cursor": cursor,
        "generation": generation,
        "checksum": _checksum(cursor, generation),
    }


def decode_checkpoint(raw: dict[str, object]) -> dict[str, object]:
    schema = raw.get("schema")
    cursor = raw.get("cursor")
    if not isinstance(cursor, str) or not cursor:
        raise CheckpointError("invalid cursor")
    if schema == 1:
        return {"cursor": cursor, "generation": 0}
    if schema != 2:
        raise CheckpointError("unsupported checkpoint schema")
    generation = raw.get("generation")
    if not isinstance(generation, int) or generation < 1:
        raise CheckpointError("invalid generation")
    if raw.get("checksum") != _checksum(cursor, generation):
        raise CheckpointError("checkpoint checksum mismatch")
    return {"cursor": cursor, "generation": generation}


def legacy_read_checkpoint(raw: dict[str, object]) -> str:
    if raw.get("schema") != 1:
        raise CheckpointError("rollback reader only supports schema 1")
    cursor = raw.get("cursor")
    if not isinstance(cursor, str) or not cursor:
        raise CheckpointError("invalid cursor")
    return cursor
