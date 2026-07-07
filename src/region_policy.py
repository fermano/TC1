"""Immutable release-region policy and decision records."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegionPolicy:
    allowed_regions: tuple[str, ...]
    default_region: str


@dataclass(frozen=True)
class RegionDecision:
    requested_region: str | None
    selected_region: str
    source: str
