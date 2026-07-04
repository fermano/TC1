from datetime import datetime, timezone

from src.tc1_service import OperationSignal
from src.tc1_severity import severity_breakdown


def _signal(severity):
    return OperationSignal("s", severity, "ops", datetime.now(timezone.utc))


def test_breakdown_counts_by_severity():
    signals = [_signal("low"), _signal("critical"), _signal("low"), _signal("high")]
    assert severity_breakdown(signals) == {"critical": 1, "high": 1, "low": 2}


def test_breakdown_orders_by_descending_rank():
    signals = [_signal("low"), _signal("critical"), _signal("medium")]
    assert list(severity_breakdown(signals).keys()) == ["critical", "medium", "low"]


def test_breakdown_keeps_unknown_labels_visible_last():
    signals = [_signal("critical"), _signal("sev1"), _signal("mystery")]
    result = severity_breakdown(signals)
    assert result["sev1"] == 1
    assert list(result.keys()) == ["critical", "mystery", "sev1"]


def test_breakdown_empty_is_empty_dict():
    assert severity_breakdown([]) == {}
