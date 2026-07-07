"""Retry-aware handoff delivery state."""

from __future__ import annotations

from collections.abc import Iterable

from src.handoff_models import HandoffDeliveryEvent, HandoffRecord


class ActiveHandoffState:
    def __init__(self) -> None:
        self._deliveries: dict[tuple[int, str], HandoffDeliveryEvent] = {}
        self._active: dict[str, tuple[tuple[int, int], HandoffRecord]] = {}

    def apply(self, events: Iterable[HandoffDeliveryEvent]) -> tuple[HandoffRecord, ...]:
        for event in events:
            delivery_key = (event.producer_epoch, event.delivery_id)
            prior_delivery = self._deliveries.get(delivery_key)
            if prior_delivery is not None:
                if prior_delivery != event:
                    raise ValueError("delivery key is already bound to a different event")
                continue

            self._deliveries[delivery_key] = event
            version = (event.producer_epoch, event.sequence)
            current = self._active.get(event.signal_id)
            if current is not None and version <= current[0]:
                continue

            if event.action == "retract":
                self._active.pop(event.signal_id, None)
            elif event.action == "upsert" and event.record is not None:
                self._active[event.signal_id] = (version, event.record)
            else:
                raise ValueError("handoff delivery must be an upsert with a record or retract")

        return tuple(value[1] for value in self._active.values())
