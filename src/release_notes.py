from collections.abc import Iterable
from dataclasses import dataclass


SEVERITY_RANK = {
    "low": 0,
    "medium": 1,
    "high": 2,
    "critical": 3,
}


@dataclass(frozen=True)
class OperationSignal:
    owner: str
    severity: str


@dataclass(frozen=True)
class HandoffSummary:
    highest_severity: str
    owners: tuple[str, ...]
    signal_count: int


def build_release_marker(version: str, channel: str) -> str:
    normalized_channel = channel.strip() or "internal"
    return f"{version}-{normalized_channel}"


def summarize_signals_for_handoff(
    signals: Iterable[OperationSignal],
    fallback_owner: str = "engineering-ops",
) -> HandoffSummary:
    rows = tuple(signals)
    owners = tuple(
        dict.fromkeys(signal.owner.strip() or fallback_owner for signal in rows)
    )
    highest = max(
        (signal.severity for signal in rows),
        key=lambda severity: SEVERITY_RANK[severity],
        default="low",
    )
    return HandoffSummary(highest, owners, len(rows))
