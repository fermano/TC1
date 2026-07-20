import sqlite3

from src.rc58_receipt_ledger import ReceiptLedger


def test_same_event_is_independent_across_tenants():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))

    assert ledger.record("tenant-a", "evt-17", 1, "delivered", "receipt-a")
    assert ledger.record("tenant-b", "evt-17", 1, "delivered", "receipt-b")

    assert ledger.lookup("tenant-a", "evt-17")["receipt"] == "receipt-a"
    assert ledger.lookup("tenant-b", "evt-17")["receipt"] == "receipt-b"


def test_stale_attempt_is_ignored_per_tenant():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))
    assert ledger.record("tenant-a", "evt-18", 4, "retracted", None)
    assert not ledger.record("tenant-a", "evt-18", 3, "delivered", "late")
