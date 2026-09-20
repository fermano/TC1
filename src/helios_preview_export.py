"""Compatibility preview used by Helios RC4 export checks."""

from __future__ import annotations

from collections.abc import Mapping

from src.invoice_export_watermark import invoice_export_is_deliverable


def preview_has_release_reference(metadata: Mapping[str, object]) -> bool:
    return invoice_export_is_deliverable(metadata)
