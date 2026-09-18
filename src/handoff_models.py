"""Canonical release-handoff records shared by intake and reporting."""

from __future__ import annotations

from dataclasses import dataclass
import re


DEFAULT_DELIVERY_LANE = "primary"
_LANE_TOKEN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def normalize_delivery_lane(lane: str | None, *, field_name: str = "lane") -> str:
    if lane is None:
        return DEFAULT_DELIVERY_LANE
    if not isinstance(lane, str):
        raise ValueError(f"{field_name} must be a string")

    normalized = lane.strip().lower()
    if not normalized:
        raise ValueError(f"{field_name} must not be blank")
    if len(normalized) > 32 or not _LANE_TOKEN.fullmatch(normalized):
        raise ValueError(f"{field_name} must be a short lower-case token")
    return normalized


@dataclass(frozen=True)
class HandoffRecord:
    signal_id: str | None
    owner: str
    severity: str
    summary: str
    lane: str | None = DEFAULT_DELIVERY_LANE

    def __post_init__(self) -> None:
        object.__setattr__(self, "lane", normalize_delivery_lane(self.lane))


@dataclass(frozen=True)
class HandoffDeliveryEvent:
    producer_epoch: int
    delivery_id: str
    signal_id: str
    sequence: int
    action: str
    record: HandoffRecord | None
    lane: str | None = DEFAULT_DELIVERY_LANE

    def __post_init__(self) -> None:
        object.__setattr__(self, "lane", normalize_delivery_lane(self.lane))


@dataclass(frozen=True)
class DeliverySnapshot:
    records: tuple[HandoffRecord, ...]
    accepted_delivery_count: int
