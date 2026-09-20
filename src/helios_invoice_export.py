"""Helios RC4 invoice-export adapter."""

from __future__ import annotations

from collections.abc import Mapping

from src.invoice_export_watermark import invoice_export_is_deliverable
from src.release_watermark_view import structured_release_watermark


def helios_export_reference(metadata: Mapping[str, object]) -> str | None:
    """Return the release reference included in a Helios invoice export."""
    if not invoice_export_is_deliverable(metadata):
        return None
    return structured_release_watermark(metadata).value
