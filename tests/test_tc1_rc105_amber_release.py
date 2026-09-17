from tc1_rc105_amber_release import amber_replay_row


def test_canonical_retry_window_controls_standard_row():
    row = amber_replay_row("amber", "north", "del-441", {"retry_window": 45})
    assert row == {
        "row_key": "amber:north:del-441",
        "disposition": "defer",
        "retry_seconds": 45,
        "artifact_stage": "rc105-candidate",
        "route_signature": "route:north",
    }


def test_missing_window_uses_default():
    row = amber_replay_row("amber", "north", "del-442", {})
    assert row["disposition"] == "defer"
    assert row["retry_seconds"] == 180
