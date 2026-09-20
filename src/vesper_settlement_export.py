from __future__ import annotations

from collections.abc import Mapping

from src.settlement_event_view import structured_settlement_event


def vesper_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    """Use the current structured settlement contract in Vesper RC1."""

    event = structured_settlement_event(metadata)
    if event.state != "committed":
        return None
    return event.token
