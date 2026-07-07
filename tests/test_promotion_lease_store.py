import sqlite3

import pytest

from src.promotion_lease_models import PromotionLease
from src.promotion_lease_store import PromotionLeaseStore


def store():
    connection = sqlite3.connect(":memory:")
    value = PromotionLeaseStore(connection)
    value.initialize()
    return value


def database_now(value):
    return value.connection.execute("SELECT unixepoch()").fetchone()[0]


def expire(value, resource):
    expired_at = database_now(value) - 1
    value.connection.execute(
        "UPDATE promotion_fences SET expires_at=? WHERE resource=?",
        (expired_at, resource),
    )
    value.connection.execute(
        "UPDATE promotion_leases SET expires_at=? WHERE resource=?",
        (expired_at, resource),
    )
    value.connection.commit()


def test_first_owner_receives_first_fence():
    value = store()
    before = database_now(value)

    lease = value.acquire("rc-17", "worker-a", 30, 100)

    after = database_now(value)
    assert lease.resource == "rc-17"
    assert lease.owner == "worker-a"
    assert lease.fence == 1
    assert before + 30 <= lease.expires_at <= after + 30


def test_unexpired_lease_blocks_different_owner():
    value = store()
    value.acquire("rc-17", "worker-a", 30, -10_000)

    assert value.acquire("rc-17", "worker-b", 30, 10_000_000_000) is None


def test_takeover_increments_fence_and_rejects_stale_publisher():
    value = store()
    old = value.acquire("rc-17", "worker-a", 30, -10_000)
    expire(value, "rc-17")
    new = value.acquire("rc-17", "worker-b", 30, 10_000_000_000)

    assert new.fence == 2
    assert value.can_publish("rc-17", old.owner, old.fence, -10_000) is False
    assert value.can_publish("rc-17", new.owner, new.fence, 10_000_000_000) is True


def test_same_owner_renewal_also_increments_fence():
    value = store()
    first = value.acquire("rc-17", "worker-a", 30, 100)
    second = value.acquire("rc-17", "worker-a", 30, 110)

    assert second.fence == first.fence + 1


def test_acquire_keeps_existing_viewer_row_in_sync():
    value = store()

    lease = value.acquire("rc-17", "worker-a", 30, 100)

    viewer_row = value.connection.execute(
        "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource=?",
        ("rc-17",),
    ).fetchone()
    assert viewer_row == (lease.resource, lease.owner, lease.expires_at)


def test_initialize_reconciles_existing_viewer_row_from_fence():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE promotion_fences "
        "(resource TEXT PRIMARY KEY, owner TEXT NOT NULL, "
        "fence INTEGER NOT NULL, expires_at INTEGER NOT NULL)"
    )
    connection.execute(
        "CREATE TABLE promotion_leases "
        "(resource TEXT PRIMARY KEY, owner TEXT NOT NULL, expires_at INTEGER NOT NULL)"
    )
    connection.execute(
        "INSERT INTO promotion_fences VALUES ('rc-41', 'worker-b', 18, 200)"
    )
    connection.execute(
        "INSERT INTO promotion_leases VALUES ('rc-41', 'worker-a', 100)"
    )
    connection.commit()

    PromotionLeaseStore(connection).initialize()

    assert connection.execute(
        "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource='rc-41'"
    ).fetchone() == ("rc-41", "worker-b", 200)


def test_failed_takeover_keeps_prior_fence():
    value = store()
    value.acquire("rc-17", "worker-a", 30, 100)
    expire(value, "rc-17")
    original = value.read("rc-17")
    viewer_row = value.connection.execute(
        "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource=?",
        ("rc-17",),
    ).fetchone()
    value.connection.execute(
        "CREATE TRIGGER reject_worker_b BEFORE UPDATE ON promotion_fences "
        "WHEN NEW.owner='worker-b' BEGIN SELECT RAISE(ABORT, 'blocked'); END"
    )
    value.connection.commit()

    with pytest.raises(sqlite3.IntegrityError, match="blocked"):
        value.acquire("rc-17", "worker-b", 30, 131)

    assert value.read("rc-17") == original
    assert value.connection.execute(
        "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource=?",
        ("rc-17",),
    ).fetchone() == viewer_row


def test_failed_viewer_update_rolls_back_new_fence():
    value = store()
    value.acquire("rc-17", "worker-a", 30, 100)
    expire(value, "rc-17")
    original = value.read("rc-17")
    viewer_row = value.connection.execute(
        "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource=?",
        ("rc-17",),
    ).fetchone()
    value.connection.execute(
        "CREATE TRIGGER reject_viewer_worker_b BEFORE UPDATE ON promotion_leases "
        "WHEN NEW.owner='worker-b' BEGIN SELECT RAISE(ABORT, 'viewer blocked'); END"
    )
    value.connection.commit()

    with pytest.raises(sqlite3.IntegrityError, match="viewer blocked"):
        value.acquire("rc-17", "worker-b", 30, 131)

    assert value.read("rc-17") == original
    assert value.connection.execute(
        "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource=?",
        ("rc-17",),
    ).fetchone() == viewer_row
