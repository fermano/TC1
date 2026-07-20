"""Dispatch replayed webhook records with a callback fence."""

from __future__ import annotations

from typing import Any

from .seed_replay_claims import ReplayClaimStore


class ReplayDispatcher:
    def __init__(self, store: ReplayClaimStore, gateway: Any) -> None:
        self.store = store
        self.gateway = gateway

    def dispatch(self, stream: str, cursor: str, payload: dict[str, Any], owner: str, now: int) -> str:
        fence = self.store.claim(stream, cursor, owner, now)
        if fence is None:
            return "skipped"

        self.gateway.send(payload)

        if not self.store.complete(stream, cursor, owner, fence):
            return "stale"
        return "delivered"
