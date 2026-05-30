"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypedDict


class HandoffRow(TypedDict):
    owner: str
    severity: str
    summary: str


SEVERITY_RANK = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def resolve_retry_budget(requested: int | None, default: int) -> int:
    """Return the configured retry count unless a request overrides it."""
    return default if requested is None else requested


def filter_handoff_rows(
    rows: Iterable[HandoffRow],
    *,
    minimum_severity: str | None = None,
) -> list[HandoffRow]:
    """Return handoff rows in the order copied from support notes."""
    row_list = list(rows)
    if minimum_severity is None:
        return row_list
    if minimum_severity not in SEVERITY_RANK:
        raise ValueError(f"unknown minimum severity: {minimum_severity}")

    minimum_rank = SEVERITY_RANK[minimum_severity]
    return [
        row
        for row in row_list
        if SEVERITY_RANK.get(row["severity"], 0) >= minimum_rank
    ]


def extract_release_marker(note: str) -> str:
    """Normalize surrounding whitespace for a release marker."""
    marker = note.strip()
    prefix = "release:"
    if marker.lower().startswith(prefix):
        marker = marker[len(prefix) :].strip()
        if not marker:
            raise ValueError("release marker prefix requires a marker value")
    return marker
