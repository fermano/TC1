"""Small service helpers for TC1 operations changes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class OperationSignal:
    name: str
    severity: str
    owner: str
    observed_at: datetime


@dataclass(frozen=True)
class ReleaseMarker:
    version: str
    channel: str
    observed_at: datetime


SEVERITY_RANK = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

OWNER_SLUG_RE = re.compile(r"[^a-z0-9]+")
RELEASE_MARKER_TIMESTAMP_FORMAT = "%Y%m%d%H%M"


def normalize_owner(owner: str) -> str:
    cleaned = OWNER_SLUG_RE.sub("-", owner.strip().lower()).strip("-")
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


def group_signals_by_owner(signals: Iterable[OperationSignal]) -> dict[str, list[OperationSignal]]:
    grouped: dict[str, list[OperationSignal]] = {}
    for signal in signals:
        grouped.setdefault(normalize_owner(signal.owner), []).append(signal)
    return grouped


def build_release_marker(version: str, channel: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime(RELEASE_MARKER_TIMESTAMP_FORMAT)
    normalized_channel = OWNER_SLUG_RE.sub("-", channel.strip().lower()).strip("-") or "internal"
    return f"{version}-{normalized_channel}-{timestamp}"


def parse_release_marker(marker: str) -> ReleaseMarker:
    try:
        prefix, timestamp = marker.rsplit("-", maxsplit=1)
        version, channel = prefix.split("-", maxsplit=1)
    except ValueError as exc:
        raise ValueError("release marker must be '<version>-<channel>-<YYYYMMDDHHMM>'") from exc

    if not all((version, channel, timestamp)):
        raise ValueError("release marker must be '<version>-<channel>-<YYYYMMDDHHMM>'")
    if len(timestamp) != 12:
        raise ValueError("release marker timestamp must use YYYYMMDDHHMM")

    try:
        observed_at = datetime.strptime(timestamp, RELEASE_MARKER_TIMESTAMP_FORMAT)
    except ValueError as exc:
        raise ValueError("release marker timestamp must use YYYYMMDDHHMM") from exc

    return ReleaseMarker(
        version=version,
        channel=channel,
        observed_at=observed_at.replace(tzinfo=timezone.utc),
    )
