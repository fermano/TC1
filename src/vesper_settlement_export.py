from __future__ import annotations

from collections.abc import Mapping

from src.settlement_event_view import structured_settlement_event


def legacy_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    raw_value = metadata.get("settlement_token")
    if not isinstance(raw_value, str):
        return None
    value = raw_value.strip()
    if not value or metadata.get("settlement_phase") != "committed":
        return None
    return value


def vesper_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    """Avoid emitting a settlement whenever the transition event retracts."""

    event = structured_settlement_event(metadata)
    if event.state == "retracted":
        return None

    legacy = legacy_settlement_reference(metadata)
    if legacy is not None:
        return legacy
    if event.state == "committed":
        return event.token
    return None
