from __future__ import annotations

from collections.abc import Mapping


def legacy_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    """Return the RC1 settlement reference from its supported legacy payload."""

    raw_value = metadata.get("settlement_token")
    if not isinstance(raw_value, str):
        return None

    value = raw_value.strip()
    if not value or metadata.get("settlement_phase") != "committed":
        return None
    return value


def vesper_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    """Select the settlement reference emitted by Vesper RC1 exports."""

    return legacy_settlement_reference(metadata)
