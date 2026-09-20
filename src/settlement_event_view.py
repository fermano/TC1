from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class SettlementEvent:
    token: str | None
    state: str | None
    replaces: str | None


def structured_settlement_event(metadata: Mapping[str, object]) -> SettlementEvent:
    settlement = metadata.get("settlement")
    if not isinstance(settlement, Mapping):
        return SettlementEvent(token=None, state=None, replaces=None)

    raw_token = settlement.get("token")
    raw_state = settlement.get("state")
    raw_replaces = settlement.get("replaces")

    token = raw_token.strip() if isinstance(raw_token, str) else ""
    state = raw_state.strip().lower() if isinstance(raw_state, str) else ""
    replaces = raw_replaces.strip() if isinstance(raw_replaces, str) else ""
    return SettlementEvent(token or None, state or None, replaces or None)
