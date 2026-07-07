import hashlib
import json
import sqlite3

import pytest

from src.checkpoint_models import Checkpoint, CheckpointBatchResult
from src.release_checkpoint_store import ReleaseCheckpointStore


def store():
    connection = sqlite3.connect(":memory:")
    value = ReleaseCheckpointStore(connection)
    value.initialize()
    return value


def test_batch_applies_all_checkpoint_updates():
    value = store()

    result = value.apply_batch(
        "batch-1",
        [Checkpoint("billing", 4, 91), Checkpoint("notifications", 2, 8)],
    )

    assert result == CheckpointBatchResult(
        "batch-1",
        (Checkpoint("billing", 4, 91), Checkpoint("notifications", 2, 8)),
    )


def test_identical_batch_retry_returns_original_result():
    value = store()
    updates = [Checkpoint("billing", 4, 91)]

    first = value.apply_batch("batch-1", updates)
    second = value.apply_batch("batch-1", list(updates))

    assert second == first


def test_batch_retry_identity_and_result_are_independent_of_iteration_order():
    value = store()
    original = [
        Checkpoint("notifications", 2, 8),
        Checkpoint("billing", 4, 91),
    ]

    first = value.apply_batch("batch-1", original)
    second = value.apply_batch("batch-1", list(reversed(original)))

    assert second == first
    assert second.checkpoints == (
        Checkpoint("billing", 4, 91),
        Checkpoint("notifications", 2, 8),
    )


def test_changed_payload_for_batch_id_is_rejected_without_rebinding():
    value = store()
    original = [Checkpoint("billing", 4, 91)]
    value.apply_batch("batch-1", original)

    with pytest.raises(ValueError, match="already bound"):
        value.apply_batch("batch-1", [Checkpoint("billing", 4, 92)])

    assert value.apply_batch("batch-1", original).checkpoints == tuple(original)
    assert value.read_legacy("billing") == Checkpoint("billing", 4, 91)


def test_new_generation_supersedes_higher_old_generation_offset():
    value = store()
    value.apply_batch("batch-1", [Checkpoint("billing", 4, 91)])

    value.apply_batch("batch-2", [Checkpoint("billing", 5, 2)])

    assert value.read("billing") == Checkpoint("billing", 5, 2)


def test_failed_second_write_rolls_back_first_write_and_batch_binding():
    connection = sqlite3.connect(":memory:")
    value = ReleaseCheckpointStore(connection)
    value.initialize()
    connection.execute(
        "CREATE TRIGGER reject_notifications BEFORE INSERT ON checkpoints "
        "WHEN NEW.stream_id='notifications' BEGIN SELECT RAISE(ABORT, 'blocked'); END"
    )
    connection.commit()
    updates = [Checkpoint("billing", 4, 91), Checkpoint("notifications", 2, 8)]

    with pytest.raises(sqlite3.IntegrityError, match="blocked"):
        value.apply_batch("batch-1", updates)

    assert value.read("billing") is None
    assert value.read_legacy("billing") is None
    assert connection.execute(
        "SELECT 1 FROM applied_checkpoint_batches WHERE batch_id='batch-1'"
    ).fetchone() is None
    connection.execute("DROP TRIGGER reject_notifications")
    connection.commit()
    assert value.apply_batch("batch-1", updates).checkpoints == tuple(updates)


def test_initialize_upgrades_legacy_only_database_and_preserves_legacy_view():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE checkpoints "
        "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
    )
    connection.execute("INSERT INTO checkpoints VALUES ('billing', 11, 884)")
    connection.commit()
    value = ReleaseCheckpointStore(connection)

    value.initialize()

    expected = Checkpoint("billing", 11, 884)
    assert value.read("billing") == expected
    assert value.read_legacy("billing") == expected
    assert connection.execute(
        "SELECT value FROM checkpoint_store_metadata WHERE name='layout'"
    ).fetchone() == ("current-with-legacy-compatibility-v1",)


def test_reentry_reconciles_greatest_checkpoint_in_each_layout():
    value = store()
    value.apply_batch(
        "batch-1",
        [Checkpoint("billing", 11, 884), Checkpoint("notifications", 5, 20)],
    )
    value.connection.execute(
        "UPDATE checkpoints SET generation=12, offset=7 WHERE stream_id='billing'"
    )
    value.connection.execute(
        "UPDATE checkpoint_state SET generation=6, offset=1 WHERE stream_id='notifications'"
    )
    value.connection.commit()

    value.initialize()

    assert value.read("billing") == Checkpoint("billing", 12, 7)
    assert value.read_legacy("billing") == Checkpoint("billing", 12, 7)
    assert value.read("notifications") == Checkpoint("notifications", 6, 1)
    assert value.read_legacy("notifications") == Checkpoint("notifications", 6, 1)


def test_failed_legacy_migration_is_atomic_and_safely_retryable():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE checkpoints "
        "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
    )
    connection.execute("INSERT INTO checkpoints VALUES ('billing', 11, 884)")
    connection.commit()
    value = ReleaseCheckpointStore(connection)

    def reject_current_inserts(action, table, _column, _database, _source):
        if action == sqlite3.SQLITE_INSERT and table == "checkpoint_state":
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    connection.set_authorizer(reject_current_inserts)
    with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
        value.initialize()
    connection.set_authorizer(lambda *_args: sqlite3.SQLITE_OK)

    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert tables == {"checkpoints"}
    assert connection.execute("SELECT * FROM checkpoints").fetchall() == [
        ("billing", 11, 884)
    ]

    value.initialize()
    assert value.read("billing") == Checkpoint("billing", 11, 884)


def test_initialize_canonicalizes_safe_pre_migration_batch_binding():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE checkpoint_state "
        "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
    )
    connection.execute(
        "CREATE TABLE applied_checkpoint_batches "
        "(batch_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL, result_json TEXT NOT NULL)"
    )
    old_updates = [
        {"stream_id": "notifications", "generation": 2, "offset": 8},
        {"stream_id": "billing", "generation": 4, "offset": 91},
    ]
    old_payload = json.dumps(old_updates, sort_keys=True, separators=(",", ":"))
    old_digest = hashlib.sha256(old_payload.encode("utf-8")).hexdigest()
    connection.executemany(
        "INSERT INTO checkpoint_state VALUES (?, ?, ?)",
        [("notifications", 2, 8), ("billing", 4, 91)],
    )
    connection.execute(
        "INSERT INTO applied_checkpoint_batches VALUES (?, ?, ?)",
        ("batch-1", old_digest, old_payload),
    )
    connection.commit()
    value = ReleaseCheckpointStore(connection)

    value.initialize()
    result = value.apply_batch(
        "batch-1",
        [Checkpoint("billing", 4, 91), Checkpoint("notifications", 2, 8)],
    )

    assert result.checkpoints == (
        Checkpoint("billing", 4, 91),
        Checkpoint("notifications", 2, 8),
    )
    assert value.read_legacy("billing") == Checkpoint("billing", 4, 91)


def test_reordered_retry_promotes_older_binding_when_result_values_differed():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE checkpoint_state "
        "(stream_id TEXT PRIMARY KEY, generation INTEGER NOT NULL, offset INTEGER NOT NULL)"
    )
    connection.execute(
        "CREATE TABLE applied_checkpoint_batches "
        "(batch_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL, result_json TEXT NOT NULL)"
    )
    old_request = [
        {"stream_id": "notifications", "generation": 2, "offset": 8},
        {"stream_id": "billing", "generation": 4, "offset": 91},
    ]
    old_result = [
        {"stream_id": "notifications", "generation": 2, "offset": 8},
        {"stream_id": "billing", "generation": 5, "offset": 2},
    ]
    old_payload = json.dumps(old_request, sort_keys=True, separators=(",", ":"))
    old_result_json = json.dumps(old_result, sort_keys=True, separators=(",", ":"))
    old_digest = hashlib.sha256(old_payload.encode("utf-8")).hexdigest()
    connection.executemany(
        "INSERT INTO checkpoint_state VALUES (?, ?, ?)",
        [("notifications", 2, 8), ("billing", 5, 2)],
    )
    connection.execute(
        "INSERT INTO applied_checkpoint_batches VALUES (?, ?, ?)",
        ("batch-1", old_digest, old_result_json),
    )
    connection.commit()
    value = ReleaseCheckpointStore(connection)

    value.initialize()
    result = value.apply_batch(
        "batch-1",
        [Checkpoint("billing", 4, 91), Checkpoint("notifications", 2, 8)],
    )

    assert result.checkpoints == (
        Checkpoint("billing", 5, 2),
        Checkpoint("notifications", 2, 8),
    )
    canonical_request = json.dumps(
        list(reversed(old_request)), sort_keys=True, separators=(",", ":")
    )
    assert connection.execute(
        "SELECT payload_digest FROM applied_checkpoint_batches WHERE batch_id='batch-1'"
    ).fetchone() == (
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
    )
