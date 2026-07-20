import sqlite3

from src.seed_replay_claims import ReplayClaimStore
from src.seed_replay_dispatch import ReplayDispatcher


class Gateway:
    def __init__(self):
        self.calls = []

    def send(self, payload):
        self.calls.append(payload)


def test_late_owner_is_skipped_after_completion():
    store = ReplayClaimStore(sqlite3.connect(":memory:"))
    gateway = Gateway()
    dispatcher = ReplayDispatcher(store, gateway)

    assert dispatcher.dispatch("billing", "evt-1", {}, "worker-a", 100) == "delivered"
    assert dispatcher.dispatch("billing", "evt-1", {}, "worker-b", 200) == "skipped"
    assert len(gateway.calls) == 1
