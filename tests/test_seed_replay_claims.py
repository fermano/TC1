import sqlite3

from src.seed_replay_claims import ReplayClaimStore
from src.seed_replay_dispatch import ReplayDispatcher


class Gateway:
    def __init__(self) -> None:
        self.sent = []

    def send(self, payload, **kwargs):
        self.sent.append((payload, kwargs))


def test_active_claim_blocks_second_owner():
    store = ReplayClaimStore(sqlite3.connect(":memory:"))

    assert store.claim("billing", "c-17", "worker-a", now=100)
    assert not store.claim("billing", "c-17", "worker-b", now=120)


def test_completed_claim_is_not_replayed():
    store = ReplayClaimStore(sqlite3.connect(":memory:"))

    assert store.claim("billing", "c-18", "worker-a", now=100)
    assert store.complete("billing", "c-18", "worker-a")
    assert not store.claim("billing", "c-18", "worker-b", now=200)


def test_dispatches_once_on_the_normal_path():
    store = ReplayClaimStore(sqlite3.connect(":memory:"))
    gateway = Gateway()
    dispatcher = ReplayDispatcher(store, gateway)

    assert dispatcher.dispatch(
        "billing", "c-19", {"event": "invoice.paid"}, "worker-a", now=100
    ) == "delivered"
    assert len(gateway.sent) == 1
