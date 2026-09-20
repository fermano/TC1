"""Helios RC4 invoice-export adapter."""

from __future__ import annotations

from collections.abc import Mapping

from src.invoice_export_watermark import legacy_release_watermark
from src.release_watermark_view import structured_release_watermark


def helios_export_reference(metadata: Mapping[str, object]) -> str | None:
    """Return the release reference included in a Helios invoice export."""
    legacy = legacy_release_watermark(metadata)
    if legacy:
        return legacy

    structured = structured_release_watermark(metadata)
    if structured.phase == "final":
        return structured.value
    return None
