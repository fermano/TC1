"""Release-only Solstice packet adapter."""

from __future__ import annotations

from collections.abc import Mapping

from src.region_policy import RegionPolicy
from src.release_region import resolve_release_region


def solstice_packet_region_value(packet: Mapping[str, str | None]) -> str | None:
    """Select the region field Solstice should resolve for transition packets."""
    region = packet.get("region")
    if region is not None and region.strip():
        return region

    region_hint = packet.get("region_hint")
    if region_hint is not None and region_hint.strip():
        return region_hint

    return region


def resolve_solstice_packet_region(
    policy: RegionPolicy,
    packet: Mapping[str, str | None],
) -> str:
    """Return the selected region for the release packet consumer.

    This consumer still uses the package-compatibility resolver while Solstice
    remains on its current package line.
    """
    return resolve_release_region(
        solstice_packet_region_value(packet),
        policy.allowed_regions,
        policy.default_region,
    )
