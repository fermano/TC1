from src.tc1_birch_replay import restore_deliveries


def test_void_tombstone_rejects_replayed_older_schedule():
    deliveries = restore_deliveries([], [
        {
            "tenant_id": "cedar", "channel_id": "mail", "message_id": "msg-17",
            "source": "partner", "kind": "void", "revision": 10,
        },
        {
            "tenant_id": "cedar", "channel_id": "mail", "message_id": "msg-17",
            "source": "partner", "kind": "schedule", "revision": 9, "holdSeconds": 0,
        },
    ])
    assert deliveries["cedar:mail:msg-17:partner"]["state"] == "void"
    assert deliveries["cedar:mail:msg-17:partner"]["revision"] == 10
