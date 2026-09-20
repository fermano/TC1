"""Compatibility entry point used by the Solstice RC2 preview build."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from src.release_region import resolve_release_region


def preview_packet_region(
    packet: Mapping[str, str | None],
    allowed_regions: Iterable[str],
    default_region: str,
) -> str:
    return resolve_release_region(
        packet.get("region"),
        allowed_regions,
        default_region,
    )
