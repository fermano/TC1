"""Helpers used by support intake and release coordination paths."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypedDict, Union

from src.handoff_models import (
    DEFAULT_DELIVERY_LANE,
    HandoffRecord,
    normalize_delivery_lane,
)


SEVERITY_RANK = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


class _LegacyHandoffRequired(TypedDict):
    owner: str
    severity: str
    summary: str


class LegacyHandoffRow(_LegacyHandoffRequired, total=False):
    event_id: str | None
    signal_id: str | None
    lane: str | None
    delivery_lane: str | None


HandoffInput = Union[HandoffRecord, LegacyHandoffRow]


def resolve_retry_budget(requested: int | None, default: int) -> int:
    """Return the configured retry count unless a request overrides it."""
    return default if requested is None else requested


def filter_handoff_rows(
    rows: Iterable[HandoffInput],
    *,
    minimum_severity: str | None = None,
    owner_fallback: str = "unassigned",
    collapse_retries: bool = False,
) -> list[HandoffRecord]:
    """Normalize handoff records and optionally merge replayed corrections."""
    fallback = owner_fallback.strip() or "unassigned"
    row_list = [_normalize_handoff_row(row) for row in rows]

    if collapse_retries:
        row_list = _collapse_retries(row_list)

    row_list = [
        HandoffRecord(
            signal_id=row.signal_id,
            owner=row.owner or fallback,
            severity=row.severity,
            summary=row.summary,
            lane=row.lane,
        )
        for row in row_list
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


def _normalize_handoff_row(row: HandoffInput) -> HandoffRecord:
    if isinstance(row, HandoffRecord):
        signal_id = row.signal_id.strip() if row.signal_id else None
        owner = row.owner
        severity = row.severity
        summary = row.summary
        lane = row.lane
    else:
        signal_id = _legacy_signal_id(row)
        owner = row["owner"]
        severity = row["severity"]
        summary = row["summary"]
        lane = _legacy_lane(row)

    return HandoffRecord(
        signal_id=signal_id,
        owner=owner.strip(),
        severity=severity.strip().lower(),
        summary=summary.strip(),
        lane=lane,
    )


def _legacy_signal_id(row: LegacyHandoffRow) -> str | None:
    signal_id = row.get("signal_id")
    event_id = row.get("event_id")
    normalized_signal_id = signal_id.strip() if signal_id is not None else ""
    normalized_event_id = event_id.strip() if event_id is not None else ""

    if (
        normalized_signal_id
        and normalized_event_id
        and normalized_signal_id != normalized_event_id
    ):
        raise ValueError("legacy handoff row has conflicting signal_id and event_id")

    return normalized_signal_id or normalized_event_id or None


def _legacy_lane(row: LegacyHandoffRow) -> str:
    if "lane" in row:
        return _required_lane(row["lane"], "lane")
    if "delivery_lane" in row:
        return _required_lane(row["delivery_lane"], "delivery_lane")
    return DEFAULT_DELIVERY_LANE


def _required_lane(value: str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} must be a string")
    return normalize_delivery_lane(value, field_name=field_name)


def _collapse_retries(rows: list[HandoffRecord]) -> list[HandoffRecord]:
    collapsed: list[HandoffRecord] = []
    index_by_signal_lane: dict[tuple[str, str], int] = {}

    for row in rows:
        if row.signal_id is None:
            collapsed.append(row)
            continue

        retry_key = (row.lane, row.signal_id)
        existing_index = index_by_signal_lane.get(retry_key)
        if existing_index is None:
            index_by_signal_lane[retry_key] = len(collapsed)
            collapsed.append(row)
            continue

        existing = collapsed[existing_index]
        existing_rank = SEVERITY_RANK.get(existing.severity, 0)
        row_rank = SEVERITY_RANK.get(row.severity, 0)
        collapsed[existing_index] = HandoffRecord(
            signal_id=existing.signal_id,
            owner=row.owner or existing.owner,
            severity=row.severity if row_rank > existing_rank else existing.severity,
            summary=row.summary or existing.summary,
            lane=existing.lane,
        )

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
