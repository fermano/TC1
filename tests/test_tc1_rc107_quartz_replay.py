from tc1_rc107_quartz_replay import replay_rows


def test_replays_one_source_event():
    rows = replay_rows([], [{
        "tenant_id": "quartz",
        "route_id": "eu",
        "job_id": "job-317",
        "source": "card",
        "event_type": "deliver",
    }])
    assert rows == {
        "quartz:eu:job-317": {
            "disposition": "deliver",
            "artifact_stage": "rc107-candidate",
            "route_signature": "route:eu",
        }
    }


def test_keeps_untouched_persisted_key():
    assert replay_rows(["quartz:eu:job-318"], []) == {
        "quartz:eu:job-318": {"disposition": "deliver"}
    }
