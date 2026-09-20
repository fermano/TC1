from __future__ import annotations

from collections.abc import Mapping


def legacy_release_watermark(metadata: Mapping[str, object]) -> str | None:
    value = metadata.get("release_watermark")
    return value.strip() if isinstance(value, str) and value.strip() else None


def invoice_export_is_deliverable(metadata: Mapping[str, object]) -> bool:
    return legacy_release_watermark(metadata) is not None
