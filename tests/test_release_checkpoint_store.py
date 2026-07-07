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


def test_changed_payload_for_batch_id_is_rejected_without_rebinding():
    value = store()
    original = [Checkpoint("billing", 4, 91)]
    value.apply_batch("batch-1", original)

    with pytest.raises(ValueError, match="already bound"):
        value.apply_batch("batch-1", [Checkpoint("billing", 4, 92)])

    assert value.apply_batch("batch-1", original).checkpoints == tuple(original)


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
        "CREATE TRIGGER reject_notifications BEFORE INSERT ON checkpoint_state "
        "WHEN NEW.stream_id='notifications' BEGIN SELECT RAISE(ABORT, 'blocked'); END"
    )
    connection.commit()
    updates = [Checkpoint("billing", 4, 91), Checkpoint("notifications", 2, 8)]

    with pytest.raises(sqlite3.IntegrityError, match="blocked"):
        value.apply_batch("batch-1", updates)

    assert value.read("billing") is None
    connection.execute("DROP TRIGGER reject_notifications")
    connection.commit()
    assert value.apply_batch("batch-1", updates).checkpoints == tuple(updates)
