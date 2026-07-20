import os
import sqlite3

import pytest

from src.rc58_receipt_ledger import ReceiptLedger


pytestmark = pytest.mark.skipif(
    os.getenv("RC58_MATRIX") != "1",
    reason="RC-58 release compatibility matrix",
)


def test_same_event_id_does_not_cross_tenant_boundary():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))

    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-shared", 1, "delivered", "receipt-a"
    )
    assert ledger.record(
        "tenant-b", "webhook-primary", "evt-shared", 1, "delivered", "receipt-b"
    )

    assert (
        ledger.lookup("tenant-a", "webhook-primary", "evt-shared")["receipt"]
        == "receipt-a"
    )
    assert (
        ledger.lookup("tenant-b", "webhook-primary", "evt-shared")["receipt"]
        == "receipt-b"
    )


def test_existing_receipt_table_accepts_route_aware_recording():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE delivery_receipts (
            event_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            attempt INTEGER NOT NULL,
            state TEXT NOT NULL,
            receipt TEXT
        )
        """
    )
    connection.execute(
        """
        INSERT INTO delivery_receipts(event_id, tenant_id, attempt, state, receipt)
        VALUES ('evt-old', 'tenant-a', 2, 'delivered', 'legacy-receipt')
        """
    )
    connection.commit()

    ledger = ReceiptLedger(connection)

    assert ledger.lookup("tenant-a", "webhook-primary", "evt-old")["receipt"] == "legacy-receipt"
    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-new", 1, "pending", None
    )


def test_retracted_receipt_remains_route_local():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))
    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-retract", 4, "retracted", None
    )
    assert ledger.record(
        "tenant-b", "webhook-primary", "evt-retract", 1, "delivered", "receipt-b"
    )
    assert (
        ledger.lookup("tenant-a", "webhook-primary", "evt-retract")["state"]
        == "retracted"
    )
