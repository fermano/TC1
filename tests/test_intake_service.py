import pytest

from src.handoff_models import HandoffRecord
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
        HandoffRecord("evt-1", "platform", "high", "Queue delay"),
        HandoffRecord("evt-2", "support", "low", "Copy cleanup"),
    ]

    assert filter_handoff_rows(rows) == rows


def test_handoff_rows_filter_by_minimum_severity_in_input_order() -> None:
    rows = [
        HandoffRecord("evt-1", "platform", "medium", "Queue delay"),
        HandoffRecord("evt-2", "support", "low", "Copy cleanup"),
        HandoffRecord("evt-3", "release", "critical", "Escalation"),
        HandoffRecord("evt-4", "docs", "unknown", "Draft note"),
    ]

    assert filter_handoff_rows(rows, minimum_severity="high") == [
        HandoffRecord("evt-3", "release", "critical", "Escalation"),
    ]


def test_handoff_rows_reject_unknown_minimum_severity() -> None:
    rows = [
        HandoffRecord("evt-1", "platform", "medium", "Queue delay"),
    ]

    with pytest.raises(ValueError, match="unknown minimum severity"):
        filter_handoff_rows(rows, minimum_severity="urgent")


def test_handoff_rows_normalize_severity_owner_and_summary() -> None:
    rows = [
        HandoffRecord(" evt-1 ", "   ", " HIGH ", "  Queue delay  "),
    ]

    assert filter_handoff_rows(rows, owner_fallback="release-ops") == [
        HandoffRecord("evt-1", "release-ops", "high", "Queue delay"),
    ]


def test_handoff_rows_accept_normalized_threshold() -> None:
    rows = [HandoffRecord("evt-1", "release", "CRITICAL", "Escalation")]

    assert filter_handoff_rows(rows, minimum_severity=" High ") == [
        HandoffRecord("evt-1", "release", "critical", "Escalation")
    ]


def test_handoff_rows_accept_legacy_event_id_and_return_canonical_records() -> None:
    rows = [
        {
            "event_id": " evt-17 ",
            "owner": " platform ",
            "severity": " HIGH ",
            "summary": " Queue delay ",
        }
    ]

    assert filter_handoff_rows(rows) == [
        HandoffRecord("evt-17", "platform", "high", "Queue delay")
    ]


def test_handoff_rows_accept_matching_legacy_identifier_aliases() -> None:
    rows = [
        {
            "event_id": " evt-17 ",
            "signal_id": "evt-17",
            "owner": "platform",
            "severity": "high",
            "summary": "Queue delay",
        }
    ]

    assert filter_handoff_rows(rows)[0].signal_id == "evt-17"


def test_handoff_rows_reject_conflicting_legacy_identifier_aliases() -> None:
    rows = [
        {
            "event_id": "evt-17",
            "signal_id": "evt-18",
            "owner": "platform",
            "severity": "high",
            "summary": "Queue delay",
        }
    ]

    with pytest.raises(ValueError, match="conflicting signal_id and event_id"):
        filter_handoff_rows(rows)


def test_handoff_rows_keep_retries_when_collapse_is_disabled() -> None:
    rows = [
        HandoffRecord("evt-17", "platform", "medium", "Preliminary"),
        HandoffRecord("evt-17", "release", "critical", "Confirmed blocker"),
    ]

    assert filter_handoff_rows(rows) == rows


def test_handoff_rows_merge_retries_in_first_seen_position() -> None:
    rows = [
        HandoffRecord("evt-17", "platform", "medium", "Preliminary"),
        HandoffRecord("evt-22", "support", "high", "Separate event"),
        HandoffRecord("evt-17", "release-ops", "critical", "Confirmed blocker"),
    ]

    assert filter_handoff_rows(rows, collapse_retries=True) == [
        HandoffRecord("evt-17", "release-ops", "critical", "Confirmed blocker"),
        HandoffRecord("evt-22", "support", "high", "Separate event"),
    ]


def test_handoff_rows_merge_canonical_and_legacy_retry_identifiers() -> None:
    rows = [
        HandoffRecord("evt-17", "platform", "medium", "Preliminary"),
        {
            "event_id": " evt-17 ",
            "owner": "release-ops",
            "severity": "critical",
            "summary": "Confirmed blocker",
        },
    ]

    assert filter_handoff_rows(rows, collapse_retries=True) == [
        HandoffRecord("evt-17", "release-ops", "critical", "Confirmed blocker")
    ]


def test_handoff_rows_keep_highest_recognized_severity_and_latest_text() -> None:
    rows = [
        HandoffRecord("evt-17", "platform", "high", "Queue blocked"),
        HandoffRecord("evt-17", "release-ops", "mystery", "Rollback approved"),
        HandoffRecord("evt-17", "incident", "medium", "Recovery started"),
    ]

    assert filter_handoff_rows(rows, collapse_retries=True) == [
        HandoffRecord("evt-17", "incident", "high", "Recovery started")
    ]


def test_handoff_rows_do_not_erase_text_with_blank_corrections() -> None:
    rows = [
        HandoffRecord("evt-17", "platform", "medium", "Queue delay"),
        HandoffRecord("evt-17", "   ", "high", "   "),
    ]

    assert filter_handoff_rows(
        rows,
        owner_fallback="release-ops",
        collapse_retries=True,
    ) == [HandoffRecord("evt-17", "platform", "high", "Queue delay")]


def test_handoff_rows_apply_owner_fallback_after_merging_blank_corrections() -> None:
    rows = [
        HandoffRecord("evt-17", "   ", "medium", "Queue delay"),
        HandoffRecord("evt-17", "", "high", "Confirmed"),
    ]

    assert filter_handoff_rows(
        rows,
        owner_fallback="release-ops",
        collapse_retries=True,
    ) == [HandoffRecord("evt-17", "release-ops", "high", "Confirmed")]


def test_handoff_rows_keep_missing_and_blank_identifiers_distinct() -> None:
    rows = [
        {
            "owner": "support",
            "severity": "low",
            "summary": "Missing identifier",
        },
        {
            "event_id": "   ",
            "owner": "support",
            "severity": "low",
            "summary": "Blank identifier",
        },
    ]

    assert filter_handoff_rows(rows, collapse_retries=True) == [
        HandoffRecord(None, "support", "low", "Missing identifier"),
        HandoffRecord(None, "support", "low", "Blank identifier"),
    ]


def test_handoff_rows_filter_merged_retries_by_final_severity() -> None:
    rows = [
        HandoffRecord("evt-17", "platform", "medium", "Preliminary"),
        HandoffRecord("evt-17", "release-ops", "critical", "Confirmed blocker"),
    ]

    assert filter_handoff_rows(
        rows,
        minimum_severity="high",
        collapse_retries=True,
    ) == [HandoffRecord("evt-17", "release-ops", "critical", "Confirmed blocker")]


def test_handoff_rows_keep_unknown_severity_without_a_threshold() -> None:
    rows = [HandoffRecord("evt-17", "docs", " UNKNOWN ", "Draft note")]

    assert filter_handoff_rows(rows, collapse_retries=True) == [
        HandoffRecord("evt-17", "docs", "unknown", "Draft note")
    ]


def test_handoff_rows_preserve_missing_required_field_key_error() -> None:
    malformed_row = {
        "event_id": "evt-17",
        "severity": "high",
        "summary": "Missing owner",
    }

    with pytest.raises(KeyError, match="owner"):
        filter_handoff_rows([malformed_row])  # type: ignore[list-item]


def test_release_marker_trims_surrounding_whitespace() -> None:
    assert extract_release_marker("  20260530-rc2  ") == "20260530-rc2"


def test_release_marker_accepts_prefixed_support_note() -> None:
    assert extract_release_marker("  ReLeAsE: 20260530-rc2  ") == "20260530-rc2"


def test_release_marker_rejects_empty_prefixed_note() -> None:
    with pytest.raises(ValueError, match="marker value"):
        extract_release_marker(" release:   ")
