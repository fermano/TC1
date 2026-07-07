import sqlite3

from src.checkpoint_models import Checkpoint
from src.release_checkpoint_store import CheckpointMigration


def migration_with_legacy_checkpoint():
    connection = sqlite3.connect(":memory:")
    migration = CheckpointMigration(connection)
    migration.initialize_legacy()
    connection.execute("INSERT INTO checkpoints VALUES ('billing', 4, 91)")
    connection.commit()
    return migration


def test_upgrade_copies_legacy_checkpoint():
    migration = migration_with_legacy_checkpoint()

    migration.upgrade()

    assert migration.read_current("billing") == Checkpoint("billing", 4, 91)


def test_rollback_copies_current_checkpoint_for_old_worker():
    migration = migration_with_legacy_checkpoint()
    migration.upgrade()
    migration.write_current(Checkpoint("billing", 5, 2))

    migration.rollback()

    assert migration.read_legacy("billing") == Checkpoint("billing", 5, 2)


def test_upgrade_can_run_again_after_rollback():
    migration = migration_with_legacy_checkpoint()
    migration.upgrade()
    migration.write_current(Checkpoint("billing", 5, 2))
    migration.rollback()

    migration.upgrade()

    assert migration.read_current("billing") == Checkpoint("billing", 5, 2)
