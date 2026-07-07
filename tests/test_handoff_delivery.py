import pytest

from src.handoff_delivery import HandoffDeliveryLedger
from src.handoff_models import DeliverySnapshot, HandoffDeliveryEvent, HandoffRecord


def event(
    delivery,
    signal,
    sequence,
    action="upsert",
    summary="Open",
    *,
    epoch=18,
):
    record = None if action == "retract" else HandoffRecord(
        signal, "release", "high", summary
    )
    return HandoffDeliveryEvent(epoch, delivery, signal, sequence, action, record)


def test_replayed_delivery_is_idempotent():
    ledger = HandoffDeliveryLedger()
    delivery = event("d-1", "sig-9", 1)

    assert ledger.apply([delivery, delivery]) == DeliverySnapshot(
        (HandoffRecord("sig-9", "release", "high", "Open"),), 1
    )


def test_changed_payload_for_epoch_delivery_identifier_is_rejected():
    ledger = HandoffDeliveryLedger()
    ledger.apply([event("d-1", "sig-9", 1)])

    with pytest.raises(ValueError, match="already bound"):
        ledger.apply([event("d-1", "sig-9", 1, summary="Changed")])

    assert ledger.apply([]) == DeliverySnapshot(
        (HandoffRecord("sig-9", "release", "high", "Open"),), 1
    )


def test_delivery_identifier_can_repeat_in_a_new_epoch():
    ledger = HandoffDeliveryLedger()
    ledger.apply([event("d-1", "sig-9", 8, summary="Old leader", epoch=18)])

    assert ledger.apply(
        [event("d-1", "sig-9", 1, summary="New leader", epoch=19)]
    ) == DeliverySnapshot(
        (HandoffRecord("sig-9", "release", "high", "New leader"),), 2
    )


def test_stale_upsert_does_not_resurrect_retracted_signal():
    ledger = HandoffDeliveryLedger()
    ledger.apply([
        event("d-1", "sig-9", 2),
        event("d-2", "sig-9", 3, action="retract"),
    ])

    assert ledger.apply([event("d-3", "sig-9", 1)]) == DeliverySnapshot((), 3)


def test_newer_upsert_reactivates_in_original_position():
    ledger = HandoffDeliveryLedger()
    ledger.apply([
        event("d-1", "sig-9", 2),
        event("d-2", "sig-10", 1),
        event("d-3", "sig-9", 3, action="retract"),
    ])

    assert ledger.apply([event("d-4", "sig-9", 4, summary="Reopened")]).records == (
        HandoffRecord("sig-9", "release", "high", "Reopened"),
        HandoffRecord("sig-10", "release", "high", "Open"),
    )


def test_new_epoch_reactivates_after_retraction_with_lower_sequence():
    ledger = HandoffDeliveryLedger()
    ledger.apply(
        [
            event("d-1", "sig-9", 11, epoch=18),
            event("d-2", "sig-10", 1, epoch=18),
            event("d-3", "sig-9", 12, action="retract", epoch=18),
        ]
    )

    snapshot = ledger.apply(
        [event("d-1", "sig-9", 1, summary="New leader", epoch=19)]
    )

    assert snapshot == DeliverySnapshot(
        (
            HandoffRecord("sig-9", "release", "high", "New leader"),
            HandoffRecord("sig-10", "release", "high", "Open"),
        ),
        4,
    )


def test_delayed_older_epoch_cannot_override_new_epoch():
    ledger = HandoffDeliveryLedger()
    ledger.apply([event("d-1", "sig-9", 1, summary="Current", epoch=19)])

    snapshot = ledger.apply(
        [event("d-2", "sig-9", 999, summary="Former leader", epoch=18)]
    )

    assert snapshot.records == (
        HandoffRecord("sig-9", "release", "high", "Current"),
    )


@pytest.mark.parametrize("epoch", [0, -1, True, 1.5])
def test_invalid_producer_epoch_is_rejected_without_mutation(epoch):
    ledger = HandoffDeliveryLedger()

    with pytest.raises(ValueError, match="positive integer"):
        ledger.apply([event("d-1", "sig-9", 1, epoch=epoch)])

    assert ledger.apply([]) == DeliverySnapshot((), 0)


def test_malformed_delivery_does_not_poison_epoch_delivery_key():
    ledger = HandoffDeliveryLedger()
    malformed = HandoffDeliveryEvent(
        18,
        "d-1",
        "sig-9",
        1,
        "retract",
        HandoffRecord("sig-9", "release", "high", "Invalid"),
    )

    with pytest.raises(ValueError, match="upsert with a record or retract"):
        ledger.apply([malformed])

    assert ledger.apply([event("d-1", "sig-9", 1)]) == DeliverySnapshot(
        (HandoffRecord("sig-9", "release", "high", "Open"),), 1
    )
