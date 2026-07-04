"""Severity distribution helpers for TC1 handoff summaries."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from src.tc1_service import SEVERITY_RANK, OperationSignal


def severity_breakdown(signals: Iterable[OperationSignal]) -> dict[str, int]:
    """Return a count of signals per severity label.

    Unlike :func:`highest_severity`, this preserves the full distribution so a
    handoff can show how many critical vs. low signals are outstanding. Unknown
    or misspelled severity labels are reported under their literal label rather
    than silently dropped, so mis-tagged signals stay visible. Results are
    ordered by severity rank (highest first); any unknown labels are listed last
    in alphabetical order.
    """
    counts = Counter(signal.severity for signal in signals)

    def sort_key(item: tuple[str, int]) -> tuple[int, str]:
        label, _ = item
        rank = SEVERITY_RANK.get(label)
        if rank is None:
            return (0, label)
        return (-rank, "")

    return {label: count for label, count in sorted(counts.items(), key=sort_key)}
