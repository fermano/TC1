from dataclasses import FrozenInstanceError

import pytest

from src.handoff_models import (
    DEFAULT_DELIVERY_LANE,
    DeliverySnapshot,
    HandoffDeliveryEvent,
    HandoffRecord,
    normalize_delivery_lane,
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


def test_handoff_record_defaults_to_primary_lane() -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")

    assert record.lane == DEFAULT_DELIVERY_LANE


def test_handoff_record_normalizes_lane_tokens() -> None:
    record = HandoffRecord(
        "evt-1",
        "release",
        "high",
        "Queue delay",
        lane=" Manual-Replay ",
    )

    assert record.lane == "manual-replay"


def test_delivery_event_and_snapshot_are_immutable() -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")
    delivery = HandoffDeliveryEvent(18, "d-1", "evt-1", 1, "upsert", record)
    snapshot = DeliverySnapshot((record,), 1)

    with pytest.raises(FrozenInstanceError):
        delivery.sequence = 2
    with pytest.raises(FrozenInstanceError):
        snapshot.accepted_delivery_count = 2


def test_delivery_event_defaults_to_primary_lane() -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")
    delivery = HandoffDeliveryEvent(18, "d-1", "evt-1", 1, "upsert", record)

    assert delivery.lane == DEFAULT_DELIVERY_LANE


def test_delivery_event_normalizes_lane_tokens() -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")
    delivery = HandoffDeliveryEvent(
        18,
        "d-1",
        "evt-1",
        1,
        "upsert",
        record,
        " Manual-Replay ",
    )

    assert delivery.lane == "manual-replay"


@pytest.mark.parametrize("lane", [" ", "retry lane", "retry_lane", "-retry", "r" * 33])
def test_delivery_event_rejects_invalid_lane_tokens(lane) -> None:
    record = HandoffRecord("evt-1", "release", "high", "Queue delay")

    with pytest.raises(ValueError, match="lane must"):
        HandoffDeliveryEvent(18, "d-1", "evt-1", 1, "upsert", record, lane)


def test_normalize_delivery_lane_treats_none_as_primary() -> None:
    assert normalize_delivery_lane(None) == DEFAULT_DELIVERY_LANE
