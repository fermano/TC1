import sqlite3

from src.promotion_lease_models import PromotionLease
from src.promotion_lease_store import PromotionLeaseStore


def store():
    connection = sqlite3.connect(":memory:")
    value = PromotionLeaseStore(connection)
    value.initialize()
    return value


def test_first_owner_receives_first_fence():
    value = store()
    assert value.acquire("rc-17", "worker-a", 30, 100) == PromotionLease(
        "rc-17", "worker-a", 1, 130
    )


def test_unexpired_lease_blocks_different_owner():
    value = store()
    value.acquire("rc-17", "worker-a", 30, 100)
    assert value.acquire("rc-17", "worker-b", 30, 110) is None


def test_takeover_increments_fence_and_rejects_stale_publisher():
    value = store()
    old = value.acquire("rc-17", "worker-a", 30, 100)
    new = value.acquire("rc-17", "worker-b", 30, 131)

    assert new.fence == 2
    assert value.can_publish("rc-17", old.owner, old.fence, 132) is False
    assert value.can_publish("rc-17", new.owner, new.fence, 132) is True


def test_same_owner_renewal_also_increments_fence():
    value = store()
    first = value.acquire("rc-17", "worker-a", 30, 100)
    second = value.acquire("rc-17", "worker-a", 30, 110)

    assert second.fence == first.fence + 1
