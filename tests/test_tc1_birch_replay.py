from src.tc1_birch_replay import restore_deliveries


def test_active_birch_delivery_has_current_context():
    deliveries = restore_deliveries([], [{
        "tenant_id": "cedar",
        "channel_id": "mail",
        "message_id": "msg-11",
        "source": "partner",
        "kind": "schedule",
        "holdSeconds": 20,
    }])
    record = deliveries["cedar:mail:msg-11:partner"]
    assert record["hold_seconds"] == 20
    assert record["release"] == "birch-3"
    assert record["record_shape"] == "v3"
    assert record["artifact_ref"] == "birch-rc-3"
