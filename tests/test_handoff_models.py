from dataclasses import FrozenInstanceError

import pytest

from src.handoff_models import HandoffRecord


def test_handoff_record_equality_uses_all_canonical_fields() -> None:
    first = HandoffRecord("evt-1", "release", "high", "Queue delay")
    same = HandoffRecord("evt-1", "release", "high", "Queue delay")
    changed = HandoffRecord("evt-1", "release", "critical", "Queue delay")

    assert same == first
    assert changed != first


def test_handoff_record_is_immutable() -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")

    with pytest.raises(FrozenInstanceError):
        record.severity = "critical"
