import pytest

from src.handoff_delivery import ActiveHandoffState
from src.handoff_models import HandoffDeliveryEvent, HandoffRecord


def event(epoch, delivery, signal, sequence, action="upsert", summary="Open"):
    record = None if action == "retract" else HandoffRecord(
        signal, "release", "high", summary
    )
    return HandoffDeliveryEvent(epoch, delivery, signal, sequence, action, record)


def test_replayed_delivery_is_idempotent():
    state = ActiveHandoffState()
    delivery = event(18, "d-1", "sig-9", 1)

    assert state.apply([delivery, delivery]) == (
        HandoffRecord("sig-9", "release", "high", "Open"),
    )


def test_delivery_identifier_can_repeat_in_a_new_epoch():
    state = ActiveHandoffState()

    state.apply([event(18, "d-1", "sig-9", 8, summary="Old leader")])
    assert state.apply([event(19, "d-1", "sig-9", 1, summary="New leader")]) == (
        HandoffRecord("sig-9", "release", "high", "New leader"),
    )


def test_changed_payload_for_same_epoch_delivery_is_rejected():
    state = ActiveHandoffState()
    state.apply([event(18, "d-1", "sig-9", 1)])

    with pytest.raises(ValueError, match="already bound"):
        state.apply([event(18, "d-1", "sig-9", 1, summary="Changed")])


def test_retraction_removes_active_record():
    state = ActiveHandoffState()

    state.apply([event(18, "d-1", "sig-9", 1)])
    assert state.apply([event(18, "d-2", "sig-9", 2, action="retract")]) == ()
