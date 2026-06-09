from datetime import datetime, timezone

import pytest

from src.tc1_service import (
    OperationSignal,
    filter_signals_by_severity,
    summarize_signals_for_handoff,
)


def _signal(name, severity, owner="ops"):
    return OperationSignal(name, severity, owner, datetime.now(timezone.utc))


def test_filter_preserves_order_and_threshold():
    signals = [
        _signal("queue-delay", "medium"),
        _signal("copy-cleanup", "low"),
        _signal("escalation", "critical"),
        _signal("draft-note", "unknown"),
    ]
    filtered = filter_signals_by_severity(signals, min_severity="high")
    assert [s.name for s in filtered] == ["escalation"]


def test_filter_returns_all_without_threshold():
    signals = [_signal("a", "low"), _signal("b", "high")]
    assert filter_signals_by_severity(signals) == signals


def test_filter_rejects_unknown_threshold():
    with pytest.raises(ValueError, match="unknown minimum severity"):
        filter_signals_by_severity([_signal("a", "low")], min_severity="urgent")


def test_summarize_applies_min_severity():
    signals = [
        _signal("queue-delay", "medium", "platform"),
        _signal("escalation", "critical", "release"),
    ]
    summary = summarize_signals_for_handoff(signals, min_severity="high")
    assert summary.signal_count == 1
    assert summary.highest_severity == "critical"
    assert summary.owners == ("release",)
