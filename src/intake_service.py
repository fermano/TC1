"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

from collections.abc import Iterable
from typing import NotRequired, TypedDict


class HandoffRow(TypedDict):
    owner: str
    severity: str
    summary: str
    event_id: NotRequired[str]


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
    collapse_retries: bool = False,
) -> list[HandoffRow]:
    """Filter handoff rows and optionally collapse replayed event IDs."""
    row_list = list(rows)
    if minimum_severity is not None:
        if minimum_severity not in SEVERITY_RANK:
            raise ValueError(f"unknown minimum severity: {minimum_severity}")

        minimum_rank = SEVERITY_RANK[minimum_severity]
        row_list = [
            row
            for row in row_list
            if SEVERITY_RANK.get(row["severity"], 0) >= minimum_rank
        ]

    if not collapse_retries:
        return row_list

    collapsed: list[HandoffRow] = []
    seen_event_ids: set[str] = set()
    for row in row_list:
        event_id = row.get("event_id", "").strip()
        if event_id:
            if event_id in seen_event_ids:
                continue
            seen_event_ids.add(event_id)
        collapsed.append(row)
    return collapsed


def extract_release_marker(note: str) -> str:
    """Normalize surrounding whitespace for a release marker."""
    marker = note.strip()
    prefix = "release:"
    if marker.lower().startswith(prefix):
        marker = marker[len(prefix) :].strip()
        if not marker:
            raise ValueError("release marker prefix requires a marker value")
    return marker
