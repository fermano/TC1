"""Release-only Solstice packet adapter."""

from __future__ import annotations

from collections.abc import Mapping

from src.region_policy import RegionPolicy
from src.release_region import resolve_release_region_request


def resolve_solstice_packet_region(
    policy: RegionPolicy,
    packet: Mapping[str, str | None],
) -> str:
    """Return the selected region for the release packet consumer."""
    return resolve_release_region_request(policy, packet).selected_region
