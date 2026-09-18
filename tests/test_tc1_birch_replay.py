from src.tc1_birch_replay import restore_deliveries


def test_active_birch_delivery_is_queued():
    deliveries = restore_deliveries([], [{
        "tenant_id": "cedar",
        "channel_id": "mail",
        "message_id": "msg-11",
        "source": "partner",
        "kind": "schedule",
        "holdSeconds": 20,
    }])
    assert deliveries["cedar:mail:msg-11:partner"]["hold_seconds"] == 20
    assert deliveries["cedar:mail:msg-11:partner"]["release"] == "birch-1"
