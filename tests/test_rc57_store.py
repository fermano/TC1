import sqlite3

from src.rc57_checkpoint import encode_checkpoint
from src.rc57_checkpoint_store import CheckpointStore


def test_fresh_store_round_trip():
    store = CheckpointStore(sqlite3.connect(":memory:"))
    raw = encode_checkpoint("offset-401", 3, "blue")

    store.save("promotion", raw)

    assert store.load("promotion") == raw
