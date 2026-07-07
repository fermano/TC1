"""Persistent in-process ledger for retried handoff deliveries."""

from __future__ import annotations

from collections.abc import Iterable

from src.handoff_models import DeliverySnapshot, HandoffDeliveryEvent, HandoffRecord


class HandoffDeliveryLedger:
    def __init__(self) -> None:
        self._deliveries: dict[tuple[int, str], HandoffDeliveryEvent] = {}
        self._entries: dict[
            str, tuple[tuple[int, int], HandoffRecord | None]
        ] = {}
        self._first_seen: dict[str, int] = {}

    def apply(self, events: Iterable[HandoffDeliveryEvent]) -> DeliverySnapshot:
        for event in events:
            self._validate(event)
            delivery_key = (event.producer_epoch, event.delivery_id)
            prior_delivery = self._deliveries.get(delivery_key)
            if prior_delivery is not None:
                if prior_delivery != event:
                    raise ValueError(
                        "epoch delivery ID is already bound to a different event"
                    )
                continue

            current = self._entries.get(event.signal_id)
            self._deliveries[delivery_key] = event
            self._first_seen.setdefault(event.signal_id, len(self._first_seen))

            version = (event.producer_epoch, event.sequence)
            if current is not None and version <= current[0]:
                continue

            record = event.record if event.action == "upsert" else None
            self._entries[event.signal_id] = (version, record)

        active = [
            (self._first_seen[signal_id], record)
            for signal_id, (_, record) in self._entries.items()
            if record is not None
        ]
        active.sort(key=lambda item: item[0])
        return DeliverySnapshot(
            records=tuple(record for _, record in active),
            accepted_delivery_count=len(self._deliveries),
        )

    @staticmethod
    def _validate(event: HandoffDeliveryEvent) -> None:
        if (
            isinstance(event.producer_epoch, bool)
            or not isinstance(event.producer_epoch, int)
            or event.producer_epoch <= 0
        ):
            raise ValueError("producer epoch must be a positive integer")
        if event.action == "upsert" and event.record is not None:
            return
        if event.action == "retract" and event.record is None:
            return
        raise ValueError("handoff delivery must be an upsert with a record or retract")
