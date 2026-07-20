import sqlite3

from src.seed_replay_claims import ReplayClaimStore
from src.seed_replay_dispatch import ReplayDispatcher, replay_idempotency_key


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
    assert gateway.sent == [
        (
            {"event": "invoice.paid"},
            {"idempotency_key": "replay:7:billing:c-19"},
        )
    ]


def test_replay_identity_keeps_stream_and_cursor_boundaries():
    assert replay_idempotency_key("billing:eu", "evt-1") != replay_idempotency_key(
        "billing", "eu:evt-1"
    )


class DeduplicatingGateway:
    def __init__(self) -> None:
        self.attempts = []
        self.deliveries = []
        self.seen_keys = set()
        self.on_first_attempt = None

    def send(self, payload, **kwargs):
        self.attempts.append((payload, kwargs))
        key = kwargs["idempotency_key"]
        if key not in self.seen_keys:
            self.seen_keys.add(key)
            self.deliveries.append(payload)

        if len(self.attempts) == 1 and self.on_first_attempt is not None:
            self.on_first_attempt()


def test_restart_takeover_reuses_gateway_identity_and_rejects_late_completion(
    tmp_path,
):
    path = tmp_path / "replay-claims.sqlite"
    first_connection = sqlite3.connect(path)
    first = ReplayDispatcher(ReplayClaimStore(first_connection), DeduplicatingGateway())
    gateway = first.gateway
    takeover = {}

    def dispatch_from_replacement_worker():
        replacement_connection = sqlite3.connect(path)
        try:
            replacement = ReplayDispatcher(
                ReplayClaimStore(replacement_connection), gateway
            )
            takeover["result"] = replacement.dispatch(
                "billing-eu",
                "evt-8841",
                {"event": "invoice.paid"},
                "worker-b",
                now=161,
            )
        finally:
            replacement_connection.close()

    gateway.on_first_attempt = dispatch_from_replacement_worker
    try:
        result = first.dispatch(
            "billing-eu",
            "evt-8841",
            {"event": "invoice.paid"},
            "worker-a",
            now=100,
        )
    finally:
        first_connection.close()

    assert result == "stale"
    assert takeover["result"] == "delivered"
    assert len(gateway.attempts) == 2
    assert gateway.attempts[0][1] == gateway.attempts[1][1]
    assert gateway.attempts[0][1]["idempotency_key"] == (
        "replay:10:billing-eu:evt-8841"
    )
    assert gateway.deliveries == [{"event": "invoice.paid"}]
