from src.release_notes import (
    OperationSignal,
    build_release_marker,
    group_signal_owners,
    highest_severity,
)


def test_blank_release_marker_channel_uses_internal_default():
    assert build_release_marker("2026.06.24", "") == "2026.06.24-internal"
    assert build_release_marker("2026.06.24", "   ") == "2026.06.24-internal"


def test_generator_backed_severity_uses_highest_signal():
    signals = (
        OperationSignal("platform", severity)
        for severity in ("low", "critical", "medium")
    )

    assert highest_severity(signals) == "critical"


def test_blank_owner_uses_configured_fallback():
    signals = (OperationSignal(owner, "high") for owner in ("", "platform"))

    assert group_signal_owners(signals, "engineering-ops") == (
        "engineering-ops",
        "platform",
    )
