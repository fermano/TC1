"""Workspace-policy reload helpers for queue handoffs."""

from __future__ import annotations

from collections.abc import Mapping


def retry_budget_from_record(record: Mapping[str, object], default: int) -> int:
    """Restore an explicit retry override from a persisted workspace record."""
    requested = record.get("retry_budget")
    if requested is None:
        return default
    return int(requested)
