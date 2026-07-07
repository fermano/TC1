"""Persistent in-process ledger for retried handoff deliveries."""

from __future__ import annotations

from collections.abc import Iterable

from src.handoff_models import DeliverySnapshot, HandoffDeliveryEvent, HandoffRecord


class HandoffDeliveryLedger:
    def __init__(self) -> None:
        self._deliveries: dict[str, HandoffDeliveryEvent] = {}
        self._entries: dict[str, tuple[int, HandoffRecord | None]] = {}
        self._first_seen: dict[str, int] = {}

    def apply(self, events: Iterable[HandoffDeliveryEvent]) -> DeliverySnapshot:
        for event in events:
            self._validate(event)
            prior_delivery = self._deliveries.get(event.delivery_id)
            if prior_delivery is not None:
                if prior_delivery != event:
                    raise ValueError("delivery ID is already bound to a different event")
                continue

            current = self._entries.get(event.signal_id)
            self._deliveries[event.delivery_id] = event
            self._first_seen.setdefault(event.signal_id, len(self._first_seen))

            if current is not None and event.sequence <= current[0]:
                continue

            record = event.record if event.action == "upsert" else None
            self._entries[event.signal_id] = (event.sequence, record)

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
        if event.action == "upsert" and event.record is not None:
            return
        if event.action == "retract" and event.record is None:
            return
        raise ValueError("handoff delivery must be an upsert with a record or retract")
