from __future__ import annotations

from collections.abc import Mapping

from src.vesper_settlement_export import vesper_settlement_reference


def preview_includes_settlement(metadata: Mapping[str, object]) -> bool:
    return vesper_settlement_reference(metadata) is not None
