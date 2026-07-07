import sqlite3

from src.promotion_lease_models import PromotionLease
from src.promotion_lease_store import PromotionLeaseStore


def store():
    connection = sqlite3.connect(":memory:")
    value = PromotionLeaseStore(connection)
    value.initialize()
    return value


def test_owner_can_acquire_empty_lease():
    value = store()
    assert value.acquire("rc-17", "worker-a", 30, 100) == PromotionLease(
        "rc-17", "worker-a", 130
    )


def test_other_owner_waits_for_unexpired_lease():
    value = store()
    value.acquire("rc-17", "worker-a", 30, 100)
    assert value.acquire("rc-17", "worker-b", 30, 110) is None


def test_other_owner_takes_over_expired_lease():
    value = store()
    value.acquire("rc-17", "worker-a", 30, 100)
    assert value.acquire("rc-17", "worker-b", 30, 131) == PromotionLease(
        "rc-17", "worker-b", 161
    )
