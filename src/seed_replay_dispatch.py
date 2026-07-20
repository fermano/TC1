"""Dispatch replayed webhook records after acquiring a durable claim."""

from __future__ import annotations

from typing import Any

from .seed_replay_claims import ReplayClaimStore


class ReplayDispatcher:
    def __init__(self, store: ReplayClaimStore, gateway: Any) -> None:
        self.store = store
        self.gateway = gateway

    def dispatch(
        self,
        stream: str,
        cursor: str,
        payload: dict[str, Any],
        owner: str,
        now: int,
    ) -> str:
        if not self.store.claim(stream, cursor, owner, now):
            return "skipped"

        # Persisting first prevents an older owner from sending after takeover.
        if not self.store.complete(stream, cursor, owner):
            return "stale"

        self.gateway.send(payload)
        return "delivered"
