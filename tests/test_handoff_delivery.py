import pytest

from src.handoff_delivery import HandoffDeliveryLedger
from src.handoff_models import DeliverySnapshot, HandoffDeliveryEvent, HandoffRecord


def event(delivery, signal, sequence, action="upsert", summary="Open"):
    record = None if action == "retract" else HandoffRecord(
        signal, "release", "high", summary
    )
    return HandoffDeliveryEvent(delivery, signal, sequence, action, record)


def test_replayed_delivery_is_idempotent():
    ledger = HandoffDeliveryLedger()
    delivery = event("d-1", "sig-9", 1)

    assert ledger.apply([delivery, delivery]) == DeliverySnapshot(
        (HandoffRecord("sig-9", "release", "high", "Open"),), 1
    )


def test_changed_payload_for_delivery_identifier_is_rejected():
    ledger = HandoffDeliveryLedger()
    ledger.apply([event("d-1", "sig-9", 1)])

    with pytest.raises(ValueError, match="already bound"):
        ledger.apply([event("d-1", "sig-9", 1, summary="Changed")])


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
