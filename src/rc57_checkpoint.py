"""Rollback-readable RC-57 checkpoint envelope."""

from __future__ import annotations


class CheckpointError(ValueError):
    pass


def encode_checkpoint(cursor: str, rollback_tag: str | None = None) -> dict[str, object]:
    if not cursor:
        raise CheckpointError("cursor is required")
    raw: dict[str, object] = {"schema": 1, "cursor": cursor}
    if rollback_tag is not None:
        raw["rollback_tag"] = rollback_tag
    return raw


def decode_checkpoint(raw: dict[str, object]) -> dict[str, object]:
    if raw.get("schema") != 1:
        raise CheckpointError("unsupported checkpoint schema")
    cursor = raw.get("cursor")
    if not isinstance(cursor, str) or not cursor:
        raise CheckpointError("invalid cursor")
    rollback_tag = raw.get("rollback_tag")
    return {
        "cursor": cursor,
        "generation": 0,
        "rollback_tag": rollback_tag if isinstance(rollback_tag, str) else None,
    }


def legacy_read_checkpoint(raw: dict[str, object]) -> tuple[str, str | None]:
    state = decode_checkpoint(raw)
    return str(state["cursor"]), state["rollback_tag"]
