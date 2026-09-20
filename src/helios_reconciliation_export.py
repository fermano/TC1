"""Helios RC4 reconciliation export compatibility path."""

from __future__ import annotations

from collections.abc import Mapping

from src.invoice_export_watermark import invoice_export_is_deliverable


def reconciliation_export_enabled(metadata: Mapping[str, object]) -> bool:
    return invoice_export_is_deliverable(metadata)
