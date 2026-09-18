"""Persistent in-process ledger for retried handoff deliveries."""

from __future__ import annotations

from collections.abc import Iterable

from src.handoff_models import (
    DeliverySnapshot,
    HandoffDeliveryEvent,
    HandoffRecord,
    normalize_delivery_lane,
)


class HandoffDeliveryLedger:
    def __init__(self) -> None:
        self._deliveries: dict[tuple[int, str, str], HandoffDeliveryEvent] = {}
        self._entries: dict[str, tuple[tuple[int, int], HandoffRecord | None]] = {}
        self._first_seen: dict[str, int] = {}

    def apply(self, events: Iterable[HandoffDeliveryEvent]) -> DeliverySnapshot:
        for event in events:
            self._validate(event)
            delivery_key = (event.producer_epoch, event.lane, event.delivery_id)
            prior_delivery = self._deliveries.get(delivery_key)
            if prior_delivery is not None:
                if prior_delivery != event:
                    raise ValueError(
                        "epoch delivery ID is already bound to a different event"
                    )
                continue

            # The support ribbon has one row per case, irrespective of the
            # delivery lane that supplied its most recent update.
            entry_key = event.signal_id
            current = self._entries.get(entry_key)
            self._deliveries[delivery_key] = event
            self._first_seen.setdefault(entry_key, len(self._first_seen))

            version = (event.producer_epoch, event.sequence)
            if current is not None and version <= current[0]:
                continue

            record = event.record if event.action == "upsert" else None
            self._entries[entry_key] = (version, record)

        active = [
            (self._first_seen[entry_key], record)
            for entry_key, (_, record) in self._entries.items()
            if record is not None
        ]
        active.sort(key=lambda item: item[0])
        return DeliverySnapshot(
            records=tuple(record for _, record in active),
            accepted_delivery_count=len(self._deliveries),
        )

    def case_timeline(
        self, signal_id: str, *, lane: str | None = None
    ) -> tuple[HandoffDeliveryEvent, ...]:
        selected_lane = normalize_delivery_lane(lane) if lane is not None else None
        events = (
            event
            for event in self._deliveries.values()
            if event.signal_id == signal_id
            and (selected_lane is None or event.lane == selected_lane)
        )
        return tuple(
            sorted(
                events,
                key=lambda event: (
                    event.producer_epoch,
                    event.sequence,
                    event.lane,
                    event.delivery_id,
                ),
            )
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
