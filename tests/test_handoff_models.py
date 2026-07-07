from dataclasses import FrozenInstanceError

import pytest

from src.handoff_models import (
    DeliverySnapshot,
    HandoffDeliveryEvent,
    HandoffRecord,
)


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


def test_delivery_event_and_snapshot_are_immutable() -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")
    delivery = HandoffDeliveryEvent(18, "d-1", "evt-1", 1, "upsert", record)
    snapshot = DeliverySnapshot((record,), 1)

    with pytest.raises(FrozenInstanceError):
        delivery.sequence = 2
    with pytest.raises(FrozenInstanceError):
        snapshot.accepted_delivery_count = 2
