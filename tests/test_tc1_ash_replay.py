from src.tc1_ash_replay import restore_records


def test_stale_void_does_not_remove_newer_record():
    records = restore_records([], [
        {
            "account_id": "iris", "lane_id": "mail", "request_id": "rq-16",
            "origin": "partner", "kind": "schedule", "revision": 8, "sendAfter": 0,
        },
        {
            "account_id": "iris", "lane_id": "mail", "request_id": "rq-16",
            "origin": "partner", "kind": "void", "revision": 7,
        },
    ])
    assert records["iris:mail:rq-16:partner"]["revision"] == 8
