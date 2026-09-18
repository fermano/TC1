from src.tc1_rc107_quartz_replay import replay_rows


def test_source_event_carries_current_candidate_generation():
    rows = replay_rows([], [{
        "tenant_id": "quartz",
        "route_id": "eu",
        "job_id": "job-317",
        "source": "card",
        "event_type": "deliver",
    }])
    assert rows == {
        "quartz:eu:job-317:card": {
            "disposition": "deliver",
            "artifact_stage": "rc107-candidate",
            "route_signature": "route:eu",
            "replay_generation": "e-16",
            "source_channel": "card",
        }
    }


def test_ordered_card_retract_does_not_remove_bank_delivery():
    rows = replay_rows([], [
        {
            "tenant_id": "quartz",
            "route_id": "eu",
            "job_id": "job-317",
            "source": "card",
            "event_type": "deliver",
            "sequence": 3,
        },
        {
            "tenant_id": "quartz",
            "route_id": "eu",
            "job_id": "job-317",
            "source": "card",
            "event_type": "retract",
            "sequence": 4,
        },
        {
            "tenant_id": "quartz",
            "route_id": "eu",
            "job_id": "job-317",
            "source": "bank",
            "event_type": "deliver",
            "sequence": 1,
        },
    ])

    assert "quartz:eu:job-317:card" not in rows
    assert rows == {
        "quartz:eu:job-317:bank": {
            "disposition": "deliver",
            "artifact_stage": "rc107-candidate",
            "route_signature": "route:eu",
            "replay_generation": "e-16",
            "source_channel": "bank",
        }
    }


def test_legacy_persisted_key_restarts_as_primary_source_state():
    assert replay_rows(["quartz:eu:job-318"], []) == {
        "quartz:eu:job-318:primary": {
            "disposition": "deliver",
            "artifact_stage": "rc107-candidate",
            "route_signature": "route:eu",
            "replay_generation": "e-16",
            "source_channel": "primary",
        }
    }


def test_replay_identity_keeps_route_and_source_distinct():
    rows = replay_rows([], [
        {
            "tenant_id": "quartz",
            "route_id": "eu",
            "job_id": "job-319",
            "source": "card",
            "event_type": "deliver",
        },
        {
            "tenant_id": "quartz",
            "route_id": "us",
            "job_id": "job-319",
            "source": "card",
            "event_type": "deliver",
        },
        {
            "tenant_id": "quartz",
            "route_id": "eu",
            "job_id": "job-319",
            "source": "bank",
            "event_type": "deliver",
        },
        {
            "tenant_id": "quartz",
            "route_id": "eu",
            "job_id": "job-319",
            "source": "card",
            "event_type": "retract",
        },
    ])

    assert sorted(rows) == [
        "quartz:eu:job-319:bank",
        "quartz:us:job-319:card",
    ]
    assert rows["quartz:eu:job-319:bank"]["route_signature"] == "route:eu"
    assert rows["quartz:eu:job-319:bank"]["source_channel"] == "bank"
    assert rows["quartz:us:job-319:card"]["route_signature"] == "route:us"
    assert rows["quartz:us:job-319:card"]["source_channel"] == "card"
    assert rows["quartz:us:job-319:card"]["replay_generation"] == "e-16"
