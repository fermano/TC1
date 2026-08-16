from src.billing_manifest_rows import coalesce_retry_rows


def test_keeps_only_newest_retry_row_for_invoice():
    rows = [
        {"invoice_id": "inv-2048", "attempt": 1, "amount": 7200},
        {"invoice_id": "inv-2048", "attempt": 2, "amount": 7200},
    ]

    assert coalesce_retry_rows(rows) == [rows[1]]
