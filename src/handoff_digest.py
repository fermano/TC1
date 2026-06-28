"""Assemble the owner rows shown in release handoff digests."""

from __future__ import annotations

from collections.abc import Iterable

from src.intake_service import HandoffRow


def assemble_handoff_digest(rows: Iterable[HandoffRow]) -> list[HandoffRow]:
    """Drop copied rows whose owner field is blank before rendering sections."""
    return [row for row in rows if row["owner"].strip()]
