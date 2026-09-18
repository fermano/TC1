from src.tc1_birch_replay import restore_deliveries


def test_active_birch_delivery_has_current_context():
    deliveries = restore_deliveries(
        [],
        [
            {
                "tenant_id": "cedar",
                "channel_id": "mail",
                "message_id": "msg-11",
                "source": "partner",
                "kind": "schedule",
                "holdSeconds": 20,
            }
        ],
    )
    record = deliveries["cedar:mail:msg-11:partner"]
    assert record["hold_seconds"] == 20
    assert record["release"] == "birch-3"
    assert record["record_shape"] == "v3"
    assert record["artifact_ref"] == "birch-rc-3"


def test_birch_keeps_primary_and_newer_partner_delivery_after_stale_void():
    deliveries = restore_deliveries(
        [],
        [
            {
                "tenant_id": "cedar",
                "channel_id": "mail",
                "message_id": "msg-24",
                "source": "primary",
                "kind": "schedule",
                "revision": 4,
                "hold_seconds": 30,
            },
            {
                "tenant_id": "cedar",
                "channel_id": "mail",
                "message_id": "msg-24",
                "source": "",
                "sourceId": "partner",
                "kind": "schedule",
                "revision": 9,
                "hold_seconds": "",
                "holdSeconds": 0,
            },
            {
                "tenant_id": "cedar",
                "channel_id": "mail",
                "message_id": "msg-24",
                "source": "partner",
                "kind": "void",
                "revision": 8,
            },
        ],
    )

    assert sorted(deliveries) == [
        "cedar:mail:msg-24:partner",
        "cedar:mail:msg-24:primary",
    ]
    assert deliveries["cedar:mail:msg-24:primary"] == {
        "state": "queued",
        "hold_seconds": 30,
        "release": "birch-3",
        "record_shape": "v3",
        "delivery_epoch": "g11",
        "channel": "mail",
        "artifact_ref": "birch-rc-3",
        "source": "primary",
    }
    assert deliveries["cedar:mail:msg-24:partner"] == {
        "state": "queued",
        "hold_seconds": 0,
        "release": "birch-3",
        "record_shape": "v3",
        "delivery_epoch": "g11",
        "channel": "mail",
        "artifact_ref": "birch-rc-3",
        "source": "partner",
    }


def test_newer_partner_void_prevents_older_schedule_from_restart_replay():
    deliveries = restore_deliveries(
        [],
        [
            {
                "tenant_id": "cedar",
                "channel_id": "mail",
                "message_id": "msg-25",
                "source": "partner",
                "kind": "void",
                "revision": 10,
            },
            {
                "tenant_id": "cedar",
                "channel_id": "mail",
                "message_id": "msg-25",
                "source": "",
                "sourceId": "partner",
                "kind": "schedule",
                "revision": 9,
                "hold_seconds": "",
                "holdSeconds": 0,
            },
        ],
    )

    assert deliveries == {}


def test_legacy_three_segment_delivery_key_restarts_as_primary_source():
    deliveries = restore_deliveries(["cedar:mail:msg-23"], [])

    assert deliveries == {
        "cedar:mail:msg-23:primary": {
            "state": "queued",
            "release": "birch-3",
            "record_shape": "v3",
            "delivery_epoch": "g11",
            "channel": "mail",
            "artifact_ref": "birch-rc-3",
            "source": "primary",
        }
    }
