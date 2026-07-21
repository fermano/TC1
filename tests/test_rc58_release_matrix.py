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


def test_same_event_id_does_not_cross_destination_boundary():
    ledger = ReceiptLedger(sqlite3.connect(":memory:"))

    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-shared", 4, "retracted", None
    )
    assert ledger.record(
        "tenant-a", "audit-archive", "evt-shared", 1, "delivered", "receipt-b"
    )

    assert (
        ledger.lookup("tenant-a", "webhook-primary", "evt-shared")["state"]
        == "retracted"
    )
    assert (
        ledger.lookup("tenant-a", "audit-archive", "evt-shared")["receipt"]
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

    assert (
        ledger.lookup("tenant-a", "webhook-primary", "evt-old")["receipt"]
        == "legacy-receipt"
    )
    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-new", 1, "pending", None
    )
    assert connection.execute("SELECT COUNT(*) FROM delivery_receipts").fetchone() == (
        2,
    )


def test_existing_route_aware_table_gains_full_route_identity():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE delivery_receipts (
            event_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            destination_id TEXT NOT NULL,
            attempt INTEGER NOT NULL,
            state TEXT NOT NULL,
            receipt TEXT
        )
        """
    )
    connection.execute(
        """
        INSERT INTO delivery_receipts(
            event_id, tenant_id, destination_id, attempt, state, receipt
        ) VALUES ('evt-old', 'tenant-a', 'audit-archive', 4, 'retracted', NULL)
        """
    )
    connection.commit()

    ledger = ReceiptLedger(connection)

    primary_key = tuple(
        row[1]
        for row in sorted(
            connection.execute("PRAGMA table_info(delivery_receipts)"),
            key=lambda row: row[5],
        )
        if row[5] > 0
    )
    assert primary_key == ("tenant_id", "destination_id", "event_id")
    assert (
        ledger.lookup("tenant-a", "audit-archive", "evt-old")["state"]
        == "retracted"
    )
    assert ledger.record(
        "tenant-a", "webhook-primary", "evt-old", 1, "delivered", "receipt-new"
    )
    assert ReceiptLedger(connection).lookup(
        "tenant-a", "audit-archive", "evt-old"
    )["state"] == "retracted"


def test_failed_migration_leaves_the_original_receipt_table_intact():
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE delivery_receipts (
            event_id TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            attempt INTEGER NOT NULL,
            state TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        INSERT INTO delivery_receipts(event_id, tenant_id, attempt, state)
        VALUES ('evt-old', 'tenant-a', 2, 'delivered')
        """
    )
    connection.commit()

    with pytest.raises(sqlite3.OperationalError):
        ReceiptLedger(connection)

    assert connection.execute(
        "SELECT event_id, tenant_id, attempt, state FROM delivery_receipts"
    ).fetchall() == [("evt-old", "tenant-a", 2, "delivered")]
    assert connection.execute(
        "SELECT name FROM sqlite_master WHERE name = 'delivery_receipts_v2'"
    ).fetchone() is None


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
