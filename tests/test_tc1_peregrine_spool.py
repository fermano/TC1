from src.tc1_peregrine_spool import restore_rows


def test_queues_one_peregrine_event():
    rows = restore_rows([], [{
        "tenant_id": "echo",
        "route_id": "eu",
        "run_id": "run-72",
        "source": "partner",
        "event_type": "schedule",
        "dispatch_after": 30,
    }])
    assert rows == {
        "echo:eu:run-72:partner": {
            "state": "queued",
            "delay_seconds": 30,
            "candidate_lineage": "pg-17<-or-11",
            "route_signature": "route:eu",
            "release_epoch": "e18",
            "source_channel": "partner",
        }
    }


def test_pg17_partner_cancel_does_not_remove_card_schedule():
    rows = restore_rows([], [
        {
            "tenant_id": "echo",
            "route_id": "eu",
            "run_id": "run-72",
            "source": "partner",
            "event_type": "schedule",
            "sequence": 3,
            "dispatch_after": "",
            "dispatchAfter": 0,
        },
        {
            "tenant_id": "echo",
            "route_id": "eu",
            "run_id": "run-72",
            "source": "card",
            "event_type": "schedule",
            "sequence": 1,
            "dispatch_after": 45,
        },
        {
            "tenant_id": "echo",
            "route_id": "eu",
            "run_id": "run-72",
            "source": "partner",
            "event_type": "cancel",
            "sequence": 4,
        },
    ])

    assert "echo:eu:run-72:partner" not in rows
    assert rows == {
        "echo:eu:run-72:card": {
            "state": "queued",
            "delay_seconds": 45,
            "candidate_lineage": "pg-17<-or-11",
            "route_signature": "route:eu",
            "release_epoch": "e18",
            "source_channel": "card",
        }
    }


def test_nonblank_canonical_dispatch_value_wins_over_partner_alias():
    rows = restore_rows([], [{
        "tenant_id": "echo",
        "route_id": "eu",
        "run_id": "run-74",
        "source": "card",
        "event_type": "schedule",
        "dispatch_after": "45",
        "dispatchAfter": 0,
    }])

    assert rows["echo:eu:run-74:card"]["delay_seconds"] == 45


def test_blank_canonical_dispatch_value_uses_explicit_zero_alias():
    rows = restore_rows([], [{
        "tenant_id": "echo",
        "route_id": "eu",
        "run_id": "run-75",
        "source": "partner",
        "event_type": "schedule",
        "dispatch_after": "",
        "dispatchAfter": 0,
    }])

    assert rows["echo:eu:run-75:partner"]["delay_seconds"] == 0


def test_legacy_persisted_key_restarts_as_primary_source_state():
    assert restore_rows(["echo:eu:run-73"], []) == {
        "echo:eu:run-73:primary": {
            "state": "queued",
            "candidate_lineage": "pg-17<-or-11",
            "route_signature": "route:eu",
            "release_epoch": "e18",
            "source_channel": "primary",
        }
    }
