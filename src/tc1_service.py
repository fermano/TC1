"""Small service helpers for TC1 operations changes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class OperationSignal:
    name: str
    severity: str
    owner: str
    observed_at: datetime


SEVERITY_RANK = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def normalize_owner(owner: str) -> str:
    cleaned = owner.strip().lower().replace(" ", "-")
    return cleaned or "unassigned"


def highest_severity(signals: Iterable[OperationSignal]) -> str:
    rank = 0
    severity = "low"
    for signal in signals:
        signal_rank = SEVERITY_RANK.get(signal.severity, 0)
        if signal_rank > rank:
            rank = signal_rank
            severity = signal.severity
    return severity


def build_release_marker(version: str, channel: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
    normalized_channel = channel.strip().lower().replace(" ", "-").replace("_", "-")
    normalized_channel = "-".join(part for part in normalized_channel.split("-") if part)
    normalized_channel = normalized_channel or "internal"
    return f"{version}-{normalized_channel}-{timestamp}"
