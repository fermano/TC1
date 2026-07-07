import sqlite3

from src.checkpoint_models import Checkpoint
from src.release_checkpoint_store import ReleaseCheckpointStore


def test_reads_legacy_checkpoint_after_initialization():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE checkpoints "
        "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
    )
    connection.execute("INSERT INTO checkpoints VALUES ('billing', 4, 91)")
    store = ReleaseCheckpointStore(connection)

    store.initialize()

    assert store.read("billing") == Checkpoint("billing", 4, 91)


def test_new_write_remains_visible_to_legacy_reader():
    connection = sqlite3.connect(":memory:")
    store = ReleaseCheckpointStore(connection)
    store.initialize()

    store.write(Checkpoint("billing", 5, 2))

    assert store.read_legacy("billing") == Checkpoint("billing", 5, 2)


def test_current_reader_prefers_current_table():
    connection = sqlite3.connect(":memory:")
    store = ReleaseCheckpointStore(connection)
    store.initialize()
    connection.execute("INSERT INTO checkpoints VALUES ('billing', 4, 91)")
    connection.execute("INSERT INTO checkpoint_state VALUES ('billing', 5, 2)")

    assert store.read("billing") == Checkpoint("billing", 5, 2)
