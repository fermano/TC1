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


def test_release_marker_trims_surrounding_whitespace() -> None:
    assert extract_release_marker("  20260530-rc2  ") == "20260530-rc2"


def test_release_marker_accepts_prefixed_support_note() -> None:
    assert extract_release_marker("  ReLeAsE: 20260530-rc2  ") == "20260530-rc2"


def test_release_marker_rejects_empty_prefixed_note() -> None:
    with pytest.raises(ValueError, match="marker value"):
        extract_release_marker(" release:   ")
