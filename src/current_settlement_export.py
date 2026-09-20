from __future__ import annotations

from collections.abc import Mapping

from src.settlement_event_view import structured_settlement_event


def current_settlement_reference(metadata: Mapping[str, object]) -> str | None:
    event = structured_settlement_event(metadata)
    if event.state != "committed":
        return None
    return event.token
