from datetime import datetime, timezone

from src.tc1_service import OperationSignal, highest_severity, normalize_owner


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
