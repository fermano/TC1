from src.tc1_service import HandoffSummary
from src.tc1_reporting import format_handoff_summary


def test_format_includes_count_severity_and_owners():
    summary = HandoffSummary(highest_severity="critical", owners=("platform-ops", "release"), signal_count=3)
    assert format_handoff_summary(summary) == "3 signals · highest=critical · owners: platform-ops, release"


def test_format_uses_singular_for_one_signal():
    summary = HandoffSummary(highest_severity="high", owners=("release",), signal_count=1)
    assert format_handoff_summary(summary) == "1 signal · highest=high · owners: release"


def test_format_shows_none_when_no_owners():
    summary = HandoffSummary(highest_severity="low", owners=(), signal_count=0)
    assert format_handoff_summary(summary) == "0 signals · highest=low · owners: none"
