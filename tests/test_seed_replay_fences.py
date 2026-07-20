import sqlite3

from src.seed_replay_claims import ReplayClaimStore


def test_old_fence_cannot_complete_after_takeover():
    store = ReplayClaimStore(sqlite3.connect(":memory:"))
    first = store.claim("billing", "evt-3", "shared-owner", 100, 60)
    second = store.claim("billing", "evt-3", "shared-owner", 161, 60)

    assert second > first
    assert not store.complete("billing", "evt-3", "shared-owner", first)
    assert store.complete("billing", "evt-3", "shared-owner", second)
