"""Compatibility entry point used by the Solstice RC2 preview build."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from src.release_region import resolve_release_region
from src.solstice_packet import solstice_packet_region_value


def preview_packet_region(
    packet: Mapping[str, str | None],
    allowed_regions: Iterable[str],
    default_region: str,
) -> str:
    return resolve_release_region(
        solstice_packet_region_value(packet),
        allowed_regions,
        default_region,
    )
