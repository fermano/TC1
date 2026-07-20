import sqlite3

from src.rc58_receipt_ledger import ReceiptLedger


def test_newer_attempt_replaces_older_attempt():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))

    assert ledger.record("tenant-a", "evt-17", 1, "pending", None)
    assert ledger.record("tenant-a", "evt-17", 2, "delivered", "receipt-2")
    assert ledger.lookup("evt-17")["receipt"] == "receipt-2"


def test_stale_attempt_is_ignored():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))

    assert ledger.record("tenant-a", "evt-18", 4, "retracted", None)
    assert not ledger.record("tenant-a", "evt-18", 3, "delivered", "late")
    assert ledger.lookup("evt-18")["state"] == "retracted"
