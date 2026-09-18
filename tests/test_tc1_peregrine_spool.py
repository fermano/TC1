from tc1_peregrine_spool import restore_rows


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
        "echo:eu:run-72": {
            "state": "queued",
            "delay_seconds": 30,
            "candidate_lineage": "pg-17<-or-11",
            "route_signature": "route:eu",
        }
    }


def test_leaves_persisted_key_in_place():
    assert restore_rows(["echo:eu:run-73"], []) == {
        "echo:eu:run-73": {"state": "queued"}
    }
