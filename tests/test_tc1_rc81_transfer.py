from src.tc1_rc81_transfer import build_transfer_row


def test_camel_case_zero_hold_seconds_is_explicit():
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "destination_id": "ach",
        "transfer_id": "tr-884",
        "holdSeconds": "0",
    })
    assert row["hold_seconds"] == 0
    assert row["action"] == "release"
