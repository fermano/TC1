"""Dispatch replayed webhook records after acquiring a durable claim."""

from __future__ import annotations

from typing import Any

from .seed_replay_claims import ReplayClaimStore


def replay_idempotency_key(stream: str, cursor: str) -> str:
    """Return the stable gateway identity for one logical replay delivery."""

    return f"replay:{len(stream)}:{stream}:{cursor}"


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

        self.gateway.send(
            payload,
            idempotency_key=replay_idempotency_key(stream, cursor),
        )

        if not self.store.complete(stream, cursor, owner):
            return "stale"
        return "delivered"
