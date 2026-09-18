from src.tc1_rc105_amber_release import amber_replay_row


def test_amber_row_keeps_current_release_metadata():
    row = amber_replay_row("amber", "north", "del-441", {"retry_window": 45})
    assert row == {
        "row_key": "amber:north:del-441",
        "disposition": "defer",
        "retry_seconds": 45,
        "artifact_stage": "rc105-candidate",
        "route_signature": "route:north",
        "replay_origin": "partner-replay",
    }


def test_blank_canonical_window_uses_partner_zero_to_dispatch():
    row = amber_replay_row(
        "amber",
        "north",
        "del-441",
        {"retry_window": "", "retryWindow": 0},
    )
    assert row == {
        "row_key": "amber:north:del-441",
        "disposition": "dispatch",
        "retry_seconds": 0,
        "artifact_stage": "rc105-candidate",
        "route_signature": "route:north",
        "replay_origin": "partner-replay",
    }


def test_nonblank_canonical_window_takes_precedence_over_alias():
    row = amber_replay_row(
        "amber",
        "north",
        "del-441",
        {"retry_window": 60, "retryWindow": 0},
    )
    assert row["disposition"] == "defer"
    assert row["retry_seconds"] == 60


def test_same_delivery_keeps_route_distinct_rows():
    north = amber_replay_row(
        "amber",
        "north",
        "del-441",
        {"retry_window": "", "retryWindow": "0"},
    )
    south = amber_replay_row(
        "amber",
        "south",
        "del-441",
        {"retry_window": "", "retryWindow": "0"},
    )
    assert north["row_key"] == "amber:north:del-441"
    assert south["row_key"] == "amber:south:del-441"
    assert north["route_signature"] == "route:north"
    assert south["route_signature"] == "route:south"
    assert north["disposition"] == south["disposition"] == "dispatch"


def test_missing_window_uses_default():
    row = amber_replay_row("amber", "north", "del-442", {})
    assert row["disposition"] == "defer"
    assert row["retry_seconds"] == 180
    assert row["replay_origin"] == "partner-replay"
