"""Read the structured release watermark published by current exporters."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseWatermarkView:
    value: str | None
    phase: str | None


def structured_release_watermark(
    metadata: Mapping[str, object],
) -> ReleaseWatermarkView:
    watermarks = metadata.get("watermarks")
    if not isinstance(watermarks, Mapping):
        return ReleaseWatermarkView(None, None)

    release = watermarks.get("release")
    if not isinstance(release, Mapping):
        return ReleaseWatermarkView(None, None)

    raw_value = release.get("id")
    raw_phase = release.get("phase")
    value = raw_value.strip() if isinstance(raw_value, str) else ""
    phase = raw_phase.strip().lower() if isinstance(raw_phase, str) else ""
    return ReleaseWatermarkView(value or None, phase or None)
