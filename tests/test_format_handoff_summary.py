from src.tc1_service import HandoffSummary
from src.tc1_reporting import format_handoff_summary


def test_format_renders_severity_and_owners():
    summary = HandoffSummary(highest_severity="critical", owners=("platform-ops", "release"), signal_count=3)
    assert format_handoff_summary(summary) == "highest=critical; owners=platform-ops, release"
