import sqlite3

from src.rc58_receipt_ledger import ReceiptLedger


def test_route_receipt_round_trip():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))
    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-17", 1, "delivered", "receipt-1"
    )
    assert (
        ledger.lookup("tenant-a", "webhook-primary", "evt-17")["receipt"]
        == "receipt-1"
    )


def test_stale_callback_cannot_replace_retraction():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))
    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-18", 4, "retracted", None
    )
    assert not ledger.record(
        "tenant-a", "webhook-primary", "evt-18", 3, "delivered", "late"
    )
    assert (
        ledger.lookup("tenant-a", "webhook-primary", "evt-18")["state"]
        == "retracted"
    )
