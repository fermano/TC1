"""Release-only Solstice packet adapter."""

from __future__ import annotations

from collections.abc import Mapping

from src.region_policy import RegionPolicy
from src.release_region import resolve_release_region


def resolve_solstice_packet_region(
    policy: RegionPolicy,
    packet: Mapping[str, str | None],
) -> str:
    """Return the selected region for the release packet consumer.

    This consumer still uses the package-compatibility resolver while Solstice
    remains on its current package line.
    """
    return resolve_release_region(
        packet.get("region"),
        policy.allowed_regions,
        policy.default_region,
    )
