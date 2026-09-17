from src.tc1_rc104_alder_release import alder_release_row


def test_alder_row_keeps_current_release_metadata():
    row = alder_release_row("alder", "east", "inv-903", {"ready_after": 120})
    assert row == {
        "row_key": "alder:east:inv-903",
        "decision": "wait",
        "wait_seconds": 120,
        "artifact_stage": "rc104-candidate",
        "route_signature": "route:east",
        "release_channel": "rc104",
    }


def test_alder_partner_zero_releases_without_wait():
    row = alder_release_row("alder", "east", "inv-903", {"ready_after": 0})
    assert row == {
        "row_key": "alder:east:inv-903",
        "decision": "release",
        "wait_seconds": 0,
        "artifact_stage": "rc104-candidate",
        "route_signature": "route:east",
        "release_channel": "rc104",
    }


def test_blank_input_uses_default_wait():
    row = alder_release_row("alder", "east", "inv-904", {"ready_after": ""})
    assert row["decision"] == "wait"
    assert row["wait_seconds"] == 240
