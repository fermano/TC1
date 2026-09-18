from datetime import datetime, timezone

from src.escalation_deadlines import (
    CaseLifecycleEvent,
    OwnerCloseWarning,
    normalize_escalation_deadline,
    schedule_owner_close_warning,
)


def test_normalizes_offset_deadline_to_utc():
    assert (
        normalize_escalation_deadline("2026-06-17T09:00:00-04:00")
        == "2026-06-17T13:00:00Z"
    )


def test_schedules_owner_warning_before_configured_close_time():
    warning = schedule_owner_close_warning(
        " case-944 ",
        " support-owner ",
        "2026-09-18T17:00:00-03:00",
        warn_before_seconds=900,
    )

    assert warning == OwnerCloseWarning(
        case_id="case-944",
        owner="support-owner",
        warn_at=datetime(2026, 9, 18, 19, 45, tzinfo=timezone.utc),
        close_at=datetime(2026, 9, 18, 20, 0, tzinfo=timezone.utc),
    )


def test_manual_close_before_warning_due_suppresses_warning():
    warning = schedule_owner_close_warning(
        "case-944",
        "support-owner",
        "2026-09-18T20:00:00Z",
        warn_before_seconds=900,
        lifecycle_events=[
            CaseLifecycleEvent("manual_closed", "2026-09-18T19:40:00Z"),
        ],
    )

    assert warning is None


def test_manual_close_at_warning_due_suppresses_warning():
    warning = schedule_owner_close_warning(
        "case-944",
        "support-owner",
        "2026-09-18T20:00:00Z",
        warn_before_seconds=900,
        lifecycle_events=[
            CaseLifecycleEvent("manual_closed", "2026-09-18T19:45:00Z"),
        ],
    )

    assert warning is None


def test_reopened_before_warning_due_suppresses_warning():
    warning = schedule_owner_close_warning(
        "case-944",
        "support-owner",
        "2026-09-18T20:00:00Z",
        warn_before_seconds=900,
        lifecycle_events=[
            CaseLifecycleEvent("reopened", "2026-09-18T19:44:00Z"),
        ],
    )

    assert warning is None


def test_manual_close_after_warning_due_does_not_remove_schedule():
    warning = schedule_owner_close_warning(
        "case-944",
        "support-owner",
        "2026-09-18T20:00:00Z",
        warn_before_seconds=900,
        lifecycle_events=[
            CaseLifecycleEvent("manual-closed", "2026-09-18T19:50:00Z"),
        ],
    )

    assert warning is not None
    assert warning.warn_at == datetime(2026, 9, 18, 19, 45, tzinfo=timezone.utc)


def test_reopened_after_warning_due_does_not_remove_schedule():
    warning = schedule_owner_close_warning(
        "case-944",
        "support-owner",
        "2026-09-18T20:00:00Z",
        warn_before_seconds=900,
        lifecycle_events=[
            CaseLifecycleEvent("reopened", "2026-09-18T19:46:00Z"),
        ],
    )

    assert warning is not None
    assert warning.warn_at == datetime(2026, 9, 18, 19, 45, tzinfo=timezone.utc)
