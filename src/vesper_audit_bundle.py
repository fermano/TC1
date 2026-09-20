from __future__ import annotations

from collections.abc import Mapping

from src.vesper_settlement_export import vesper_settlement_reference


def audit_bundle_settlement(metadata: Mapping[str, object]) -> dict[str, str] | None:
    reference = vesper_settlement_reference(metadata)
    if reference is None:
        return None
    return {"settlement_reference": reference}
