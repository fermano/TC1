"""Canonical release-handoff records shared by intake and reporting."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HandoffRecord:
    signal_id: str | None
    owner: str
    severity: str
    summary: str
