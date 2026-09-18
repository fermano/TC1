from src.tc1_ash_replay import restore_records


def test_active_ash_record_is_queued_with_current_artifact():
    records = restore_records(
        [],
        [
            {
                "account_id": "iris",
                "lane_id": "mail",
                "request_id": "rq-11",
                "origin": "partner",
                "kind": "schedule",
                "sendAfter": 12,
            }
        ],
    )

    assert records["iris:mail:rq-11:partner"] == {
        "state": "queued",
        "delay_seconds": 12,
        "release": "ash-2",
        "record_shape": "v2",
        "lane": "mail",
        "artifact_ref": "ash-rc-2",
        "origin": "partner",
    }


def test_blank_canonical_origin_uses_partner_alias_without_replacing_primary():
    records = restore_records(
        [],
        [
            {
                "account_id": "iris",
                "lane_id": "mail",
                "request_id": "rq-24",
                "origin": "primary",
                "kind": "schedule",
                "revision": 4,
                "send_after": 25,
            },
            {
                "account_id": "iris",
                "lane_id": "mail",
                "request_id": "rq-24",
                "origin": "",
                "originId": "partner",
                "kind": "schedule",
                "revision": 9,
                "send_after": "",
                "sendAfter": 0,
            },
            {
                "account_id": "iris",
                "lane_id": "mail",
                "request_id": "rq-24",
                "origin": "partner",
                "kind": "void",
                "revision": 8,
            },
        ],
    )

    assert sorted(records) == [
        "iris:mail:rq-24:partner",
        "iris:mail:rq-24:primary",
    ]
    assert records["iris:mail:rq-24:primary"] == {
        "state": "queued",
        "delay_seconds": 25,
        "release": "ash-2",
        "record_shape": "v2",
        "lane": "mail",
        "artifact_ref": "ash-rc-2",
        "origin": "primary",
    }
    assert records["iris:mail:rq-24:partner"] == {
        "state": "queued",
        "delay_seconds": 0,
        "release": "ash-2",
        "record_shape": "v2",
        "lane": "mail",
        "artifact_ref": "ash-rc-2",
        "origin": "partner",
    }


def test_newer_void_prevents_older_partner_schedule_from_restart_replay():
    records = restore_records(
        [],
        [
            {
                "account_id": "iris",
                "lane_id": "mail",
                "request_id": "rq-24",
                "origin": "partner",
                "kind": "void",
                "revision": 10,
            },
            {
                "account_id": "iris",
                "lane_id": "mail",
                "request_id": "rq-24",
                "origin": "",
                "originId": "partner",
                "kind": "schedule",
                "revision": 9,
                "send_after": "",
                "sendAfter": 0,
            },
        ],
    )

    assert records == {}


def test_legacy_three_segment_key_restarts_as_primary_origin():
    records = restore_records(["iris:mail:rq-23"], [])

    assert records == {
        "iris:mail:rq-23:primary": {
            "state": "queued",
            "release": "ash-2",
            "record_shape": "v2",
            "lane": "mail",
            "artifact_ref": "ash-rc-2",
            "origin": "primary",
        }
    }
