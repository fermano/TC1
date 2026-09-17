from tc1_rc104_alder_release import alder_release_row


def test_alder_row_keeps_current_release_metadata():
    row = alder_release_row("alder", "east", "inv-903", {"ready_after": 120})
    assert row == {
        "row_key": "alder:east:inv-903",
        "decision": "wait",
        "wait_seconds": 120,
        "artifact_stage": "rc104-candidate",
        "route_signature": "route:east",
    }


def test_blank_input_uses_default_wait():
    row = alder_release_row("alder", "east", "inv-904", {"ready_after": ""})
    assert row["decision"] == "wait"
    assert row["wait_seconds"] == 240
