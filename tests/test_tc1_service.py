from datetime import datetime, timezone

import pytest

from src.tc1_service import (
    OperationSignal,
    build_release_marker,
    group_signals_by_owner,
    highest_severity,
    normalize_owner,
    parse_release_marker,
)


def test_normalize_owner_falls_back_to_unassigned():
    assert normalize_owner("   ") == "unassigned"


def test_normalize_owner_slugifies_names():
    assert normalize_owner("Platform Ops") == "platform-ops"


def test_highest_severity_returns_largest_rank():
    signals = [
        OperationSignal("docs-drift", "medium", "docs", datetime.now(timezone.utc)),
        OperationSignal("release-blocker", "critical", "release", datetime.now(timezone.utc)),
        OperationSignal("flake", "low", "qa", datetime.now(timezone.utc)),
    ]

    assert highest_severity(signals) == "critical"


def test_build_release_marker_normalizes_channel_values_from_support_notes():
    marker = build_release_marker("2026.05.25", "Internal Ops___Primary")

    assert marker.startswith("2026.05.25-internal-ops-primary-")


def test_parse_release_marker_returns_structured_fields():
    marker = parse_release_marker("2026.05.25-internal-202605251630")

    assert marker.version == "2026.05.25"
    assert marker.channel == "internal"
    assert marker.observed_at == datetime(2026, 5, 25, 16, 30, tzinfo=timezone.utc)


def test_parse_release_marker_round_trips_normalized_channels():
    marker = build_release_marker("2026.05.25", "Internal Ops___Primary")
    parsed = parse_release_marker(marker)

    assert parsed.version == "2026.05.25"
    assert parsed.channel == "internal-ops-primary"


def test_parse_release_marker_rejects_malformed_marker():
    with pytest.raises(ValueError, match="release marker"):
        parse_release_marker("not-a-marker")


def test_parse_release_marker_rejects_invalid_timestamp():
    with pytest.raises(ValueError, match="timestamp"):
        parse_release_marker("2026.05.25-internal-202613011200")


def test_parse_release_marker_rejects_short_timestamp():
    with pytest.raises(ValueError, match="timestamp"):
        parse_release_marker("2026.05.25-internal-20260525163")


def test_group_signals_by_owner_normalizes_and_preserves_order():
    first = OperationSignal("docs-drift", "medium", "Platform Ops", datetime.now(timezone.utc))
    second = OperationSignal("flake", "low", "platform_ops", datetime.now(timezone.utc))
    third = OperationSignal("unowned", "high", "   ", datetime.now(timezone.utc))

    grouped = group_signals_by_owner([first, second, third])

    assert grouped == {
        "platform-ops": [first, second],
        "unassigned": [third],
    }


def test_group_signals_by_owner_uses_fallback_owner_for_blank_handoffs():
    signal = OperationSignal("handoff", "high", "   ", datetime.now(timezone.utc))

    grouped = group_signals_by_owner([signal], fallback_owner="engineering-ops")

    assert grouped == {"engineering-ops": [signal]}


def test_group_signals_by_owner_keeps_default_unassigned_path_without_fallback():
    signal = OperationSignal("handoff", "high", "   ", datetime.now(timezone.utc))

    grouped = group_signals_by_owner([signal])

    assert grouped == {"unassigned": [signal]}
