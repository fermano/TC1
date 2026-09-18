from src.tc1_ash_replay import restore_records


def test_active_ash_record_is_queued():
    records = restore_records([], [{
        "account_id": "iris",
        "lane_id": "mail",
        "request_id": "rq-11",
        "origin": "partner",
        "kind": "schedule",
        "sendAfter": 12,
    }])
    assert records["iris:mail:rq-11:partner"]["delay_seconds"] == 12
    assert records["iris:mail:rq-11:partner"]["release"] == "ash-1"
