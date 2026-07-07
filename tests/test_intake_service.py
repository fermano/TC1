import pytest

from src.intake_service import (
    extract_release_marker,
    filter_handoff_rows,
    resolve_retry_budget,
)


def test_retry_budget_uses_default_when_omitted() -> None:
    assert resolve_retry_budget(None, 3) == 3


def test_retry_budget_preserves_zero_override() -> None:
    assert resolve_retry_budget(0, 3) == 0


def test_retry_budget_accepts_positive_override() -> None:
    assert resolve_retry_budget(2, 3) == 2


def test_handoff_rows_keep_input_order() -> None:
    rows = [
        {"owner": "platform", "severity": "high", "summary": "Queue delay"},
        {"owner": "support", "severity": "low", "summary": "Copy cleanup"},
    ]

    assert filter_handoff_rows(rows) == rows


def test_handoff_rows_filter_by_minimum_severity_in_input_order() -> None:
    rows = [
        {"owner": "platform", "severity": "medium", "summary": "Queue delay"},
        {"owner": "support", "severity": "low", "summary": "Copy cleanup"},
        {"owner": "release", "severity": "critical", "summary": "Escalation"},
        {"owner": "docs", "severity": "unknown", "summary": "Draft note"},
    ]

    assert filter_handoff_rows(rows, minimum_severity="high") == [
        {"owner": "release", "severity": "critical", "summary": "Escalation"},
    ]


def test_handoff_rows_reject_unknown_minimum_severity() -> None:
    rows = [
        {"owner": "platform", "severity": "medium", "summary": "Queue delay"},
    ]

    with pytest.raises(ValueError, match="unknown minimum severity"):
        filter_handoff_rows(rows, minimum_severity="urgent")


def test_handoff_rows_collapse_replayed_event_ids_in_first_seen_order() -> None:
    rows = [
        {
            "event_id": "evt-17",
            "owner": "platform",
            "severity": "medium",
            "summary": "Queue delay",
        },
        {
            "event_id": "evt-22",
            "owner": "release",
            "severity": "critical",
            "summary": "Approval blocked",
        },
        {
            "event_id": "evt-17",
            "owner": "platform-ops",
            "severity": "high",
            "summary": "Queue delay confirmed",
        },
    ]

    assert filter_handoff_rows(rows, collapse_retries=True) == rows[:2]


def test_handoff_rows_keep_missing_and_blank_event_ids_distinct() -> None:
    rows = [
        {"owner": "support", "severity": "low", "summary": "First note"},
        {
            "event_id": "   ",
            "owner": "support",
            "severity": "low",
            "summary": "Second note",
        },
    ]

    assert filter_handoff_rows(rows, collapse_retries=True) == rows


def test_handoff_rows_filter_before_collapsing_retries() -> None:
    rows = [
        {
            "event_id": "evt-17",
            "owner": "platform",
            "severity": "low",
            "summary": "Preliminary",
        },
        {
            "event_id": "evt-17",
            "owner": "platform-ops",
            "severity": "high",
            "summary": "Confirmed blocker",
        },
    ]

    assert filter_handoff_rows(
        rows,
        minimum_severity="high",
        collapse_retries=True,
    ) == [rows[1]]


def test_release_marker_trims_surrounding_whitespace() -> None:
    assert extract_release_marker("  20260530-rc2  ") == "20260530-rc2"


def test_release_marker_accepts_prefixed_support_note() -> None:
    assert extract_release_marker("  ReLeAsE: 20260530-rc2  ") == "20260530-rc2"


def test_release_marker_rejects_empty_prefixed_note() -> None:
    with pytest.raises(ValueError, match="marker value"):
        extract_release_marker(" release:   ")
