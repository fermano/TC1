import sqlite3
from pathlib import Path

from src.seed_replay_claims import ReplayClaimStore


def test_expired_lease_can_be_taken_after_restart(tmp_path: Path):
    path = tmp_path / "claims.sqlite"
    first = sqlite3.connect(path)
    assert ReplayClaimStore(first).claim("billing", "evt-2", "worker-a", 100, 60)
    first.close()

    second = sqlite3.connect(path)
    store = ReplayClaimStore(second)
    assert not store.claim("billing", "evt-2", "worker-b", 159, 60)
    assert store.claim("billing", "evt-2", "worker-b", 161, 60)
