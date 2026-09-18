from src.tc1_ash_replay import restore_records


def test_alias_origin_does_not_replace_primary_record():
    records = restore_records([], [
        {
            "account_id": "iris", "lane_id": "mail", "request_id": "rq-17",
            "origin": "primary", "kind": "schedule", "send_after": 20,
        },
        {
            "account_id": "iris", "lane_id": "mail", "request_id": "rq-17",
            "origin": "", "originId": "partner", "kind": "schedule", "sendAfter": 0,
        },
    ])
    assert records["iris:mail:rq-17:primary"]["delay_seconds"] == 20
    assert records["iris:mail:rq-17:partner"]["delay_seconds"] == 0
