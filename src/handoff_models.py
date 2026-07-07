"""Canonical release-handoff records shared by intake and reporting."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HandoffRecord:
    signal_id: str | None
    owner: str
    severity: str
    summary: str


@dataclass(frozen=True)
class HandoffDeliveryEvent:
    delivery_id: str
    signal_id: str
    sequence: int
    action: str
    record: HandoffRecord | None


@dataclass(frozen=True)
class DeliverySnapshot:
    records: tuple[HandoffRecord, ...]
    accepted_delivery_count: int
