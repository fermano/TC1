from src.tc1_birch_replay import restore_deliveries


def test_blank_canonical_source_uses_partner_alias_without_replacing_primary():
    deliveries = restore_deliveries([], [
        {
            "tenant_id": "cedar", "channel_id": "mail", "message_id": "msg-18",
            "source": "primary", "kind": "schedule", "hold_seconds": 25,
        },
        {
            "tenant_id": "cedar", "channel_id": "mail", "message_id": "msg-18",
            "source": "", "sourceId": "partner", "kind": "schedule",
            "hold_seconds": "", "holdSeconds": 0,
        },
    ])
    assert deliveries["cedar:mail:msg-18:primary"]["hold_seconds"] == 25
    assert deliveries["cedar:mail:msg-18:partner"]["hold_seconds"] == 0
