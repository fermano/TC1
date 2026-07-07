"""Immutable export schema state used by cache consumers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchemaSnapshot:
    workspace_id: str
    workspace_version: int
    fields: tuple[str, ...]
