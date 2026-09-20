from __future__ import annotations

from collections.abc import Mapping

from src.vesper_settlement_export import vesper_settlement_reference


def reconciliation_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    return vesper_settlement_reference(metadata)
