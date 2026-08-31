from src.tc1_rc81_transfer import ARTIFACT_SCHEMA, build_transfer_row


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
    assert row["artifact_schema"] == ARTIFACT_SCHEMA
    assert row["operator_key"] == "ach:tr-884:hold"


def test_defaults_missing_hold_window():
    row = build_transfer_row({"tenant_id": "kitebank", "route_id": "wire", "transfer_id": "tr-101"})
    assert row["hold_seconds"] == 300
    assert row["action"] == "hold"
