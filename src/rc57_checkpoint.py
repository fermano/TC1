"""Additive RC-57 checkpoint envelope for the rolling window."""

from __future__ import annotations

import hashlib


class CheckpointError(ValueError):
    pass


def _checksum(cursor: str, generation: int) -> str:
    return hashlib.sha256(f"{cursor}:{generation}".encode()).hexdigest()[:16]


def encode_checkpoint(
    cursor: str,
    generation: int,
    rollback_tag: str | None = None,
) -> dict[str, object]:
    if not cursor:
        raise CheckpointError("cursor is required")
    if generation < 1:
        raise CheckpointError("generation must be positive")
    raw: dict[str, object] = {
        "schema": 1,
        "cursor": cursor,
        "generation": generation,
        "checksum": _checksum(cursor, generation),
    }
    if rollback_tag is not None:
        raw["rollback_tag"] = rollback_tag
    return raw


def decode_checkpoint(raw: dict[str, object]) -> dict[str, object]:
    if raw.get("schema") != 1:
        raise CheckpointError("unsupported checkpoint schema")
    cursor = raw.get("cursor")
    generation = raw.get("generation", 0)
    if not isinstance(cursor, str) or not cursor:
        raise CheckpointError("invalid cursor")
    if not isinstance(generation, int) or generation < 0:
        raise CheckpointError("invalid generation")
    checksum = raw.get("checksum")
    if checksum is not None and checksum != _checksum(cursor, generation):
        raise CheckpointError("checkpoint checksum mismatch")
    rollback_tag = raw.get("rollback_tag")
    if rollback_tag is not None and not isinstance(rollback_tag, str):
        raise CheckpointError("invalid rollback tag")
    return {
        "cursor": cursor,
        "generation": generation,
        "rollback_tag": rollback_tag,
    }


def legacy_read_checkpoint(raw: dict[str, object]) -> tuple[str, str | None]:
    if raw.get("schema") != 1:
        raise CheckpointError("rollback reader only supports schema 1")
    state = decode_checkpoint(raw)
    return str(state["cursor"]), state["rollback_tag"]
