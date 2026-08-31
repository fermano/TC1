from src.tc1_rc81_transfer import build_transfer_row


def test_uses_route_scoped_shape():
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "ach",
        "transfer_id": "tr-884",
        "hold_seconds": 45,
    })
    assert row["route_id"] == "ach"
    assert row["action"] == "hold"
    assert row["source"] == "rc81-route-window"


def test_defaults_missing_hold_window():
    row = build_transfer_row({"tenant_id": "kitebank", "route_id": "wire", "transfer_id": "tr-101"})
    assert row["hold_seconds"] == 300
    assert row["action"] == "hold"


def test_explicit_zero_hold_seconds_releases_snake_case_fixture():
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "ach",
        "transfer_id": "tr-884",
        "hold_seconds": 0,
    })
    assert row["hold_seconds"] == 0
    assert row["action"] == "release"
