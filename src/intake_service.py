"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypedDict


class HandoffRow(TypedDict):
    owner: str
    severity: str
    summary: str


def resolve_retry_budget(requested: int | None, default: int) -> int:
    """Return the configured retry count unless a request overrides it."""
    return default if requested is None else requested


def filter_handoff_rows(rows: Iterable[HandoffRow]) -> list[HandoffRow]:
    """Return handoff rows in the order copied from support notes."""
    return list(rows)


def extract_release_marker(note: str) -> str:
    """Normalize surrounding whitespace for a release marker."""
    return note.strip()
