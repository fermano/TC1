"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

from collections.abc import Iterable
from src.handoff_models import HandoffRecord


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
    rows: Iterable[HandoffRecord],
    *,
    minimum_severity: str | None = None,
    owner_fallback: str = "unassigned",
) -> list[HandoffRecord]:
    """Normalize canonical handoff records and filter without reordering."""
    fallback = owner_fallback.strip() or "unassigned"
    row_list = [
        HandoffRecord(
            signal_id=row.signal_id.strip() if row.signal_id else None,
            owner=row.owner.strip() or fallback,
            severity=row.severity.strip().lower(),
            summary=row.summary.strip(),
        )
        for row in rows
    ]
    if minimum_severity is None:
        return row_list
    threshold = minimum_severity.strip().lower()
    if threshold not in SEVERITY_RANK:
        raise ValueError(f"unknown minimum severity: {minimum_severity}")

    minimum_rank = SEVERITY_RANK[threshold]
    return [
        row
        for row in row_list
        if SEVERITY_RANK.get(row.severity, 0) >= minimum_rank
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
