"""Human-readable rendering for TC1 handoff summaries."""

from __future__ import annotations

from src.tc1_service import HandoffSummary


def format_handoff_summary(summary: HandoffSummary) -> str:
    owners = ", ".join(summary.owners)
    return f"highest={summary.highest_severity}; owners={owners}"
