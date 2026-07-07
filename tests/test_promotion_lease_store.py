import sqlite3

from src.promotion_lease_store import PromotionLeaseJournal


def test_restart_replays_last_lease_event():
    connection = sqlite3.connect(":memory:")
    first = PromotionLeaseJournal(connection)
    first.initialize()
    first.acquire("rc-17", "worker-a", 30, 100)

    restarted = PromotionLeaseJournal(connection)

    assert restarted.current("rc-17").owner == "worker-a"


def test_release_allows_later_owner():
    connection = sqlite3.connect(":memory:")
    value = PromotionLeaseJournal(connection)
    value.initialize()
    value.acquire("rc-17", "worker-a", 30, 100)
    value.release("rc-17", "worker-a", 105)

    acquired = value.acquire("rc-17", "worker-b", 30, 106)

    assert acquired.owner == "worker-b"


def test_unexpired_journal_entry_blocks_second_owner():
    connection = sqlite3.connect(":memory:")
    value = PromotionLeaseJournal(connection)
    value.initialize()
    value.acquire("rc-17", "worker-a", 30, 100)

    assert value.acquire("rc-17", "worker-b", 30, 110) is None
