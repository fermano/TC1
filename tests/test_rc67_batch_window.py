from src.rc67_batch_window import build_window_rows


def test_selects_rows_by_created_at_window():
    receipts = [
        {
            "tenant_id": "atlas",
            "receipt_id": "r-1",
            "state": "sent",
            "amount_cents": 1200,
            "created_at": 100,
        },
        {
            "tenant_id": "atlas",
            "receipt_id": "r-2",
            "state": "sent",
            "amount_cents": 1300,
            "created_at": 200,
        },
        {
            "tenant_id": "atlas",
            "receipt_id": "r-3",
            "state": "draft",
            "amount_cents": 1400,
            "created_at": 110,
        },
    ]

    assert build_window_rows(receipts, window_start=90, window_end=150) == [
        {
            "tenant_id": "atlas",
            "receipt_id": "r-1",
            "amount_cents": 1200,
            "created_at": 100,
        }
    ]


def test_deduplicates_receipts_by_tenant_and_id():
    receipts = [
        {
            "tenant_id": "atlas",
            "receipt_id": "r-1",
            "state": "sent",
            "amount_cents": 1200,
            "created_at": 100,
        },
        {
            "tenant_id": "atlas",
            "receipt_id": "r-1",
            "state": "settled",
            "amount_cents": 1200,
            "created_at": 101,
        },
    ]

    assert build_window_rows(receipts, window_start=90, window_end=150) == [
        {
            "tenant_id": "atlas",
            "receipt_id": "r-1",
            "amount_cents": 1200,
            "created_at": 100,
        }
    ]
