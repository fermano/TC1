"""Human-readable rendering for TC1 handoff summaries."""

from __future__ import annotations

from src.tc1_service import HandoffSummary


def format_handoff_summary(summary: HandoffSummary) -> str:
    """Render a one-line handoff summary for release notes and email digests.

    Example: ``3 signals · highest=critical · owners: platform-ops, release``.
    """
    owners = ", ".join(summary.owners) if summary.owners else "none"
    signal_word = "signal" if summary.signal_count == 1 else "signals"
    return (
        f"{summary.signal_count} {signal_word} · "
        f"highest={summary.highest_severity} · "
        f"owners: {owners}"
    )
