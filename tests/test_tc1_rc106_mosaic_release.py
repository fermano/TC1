from src.tc1_rc106_mosaic_release import mosaic_manifest_row


def test_blank_canonical_hold_uses_zero_alias_for_card_packet_row():
    row = mosaic_manifest_row(
        "mosaic", "eu", "inv-882", "card", {"hold_seconds": "", "holdSeconds": 0}
    )

    assert row == {
        "row_key": "mosaic:eu:inv-882:card",
        "disposition": "emit",
        "hold_seconds": 0,
        "artifact_stage": "rc106-candidate",
        "route_signature": "route:eu",
        "replay_generation": "d-9",
        "source_channel": "card",
    }


def test_nonblank_canonical_hold_precedes_alias():
    row = mosaic_manifest_row(
        "mosaic", "eu", "inv-884", "card", {"hold_seconds": "30", "holdSeconds": 0}
    )

    assert row == {
        "row_key": "mosaic:eu:inv-884:card",
        "disposition": "hold",
        "hold_seconds": 30,
        "artifact_stage": "rc106-candidate",
        "route_signature": "route:eu",
        "replay_generation": "d-9",
        "source_channel": "card",
    }


def test_bank_packet_row_stays_independent_from_card_source():
    card_row = mosaic_manifest_row(
        "mosaic", "eu", "inv-882", "card", {"hold_seconds": "", "holdSeconds": 0}
    )
    bank_row = mosaic_manifest_row(
        "mosaic", "eu", "inv-882", "bank", {"hold_seconds": 60}
    )

    assert card_row["row_key"] == "mosaic:eu:inv-882:card"
    assert card_row["disposition"] == "emit"
    assert card_row["hold_seconds"] == 0
    assert bank_row == {
        "row_key": "mosaic:eu:inv-882:bank",
        "disposition": "hold",
        "hold_seconds": 60,
        "artifact_stage": "rc106-candidate",
        "route_signature": "route:eu",
        "replay_generation": "d-9",
        "source_channel": "bank",
    }


def test_missing_hold_uses_default():
    row = mosaic_manifest_row("mosaic", "eu", "inv-883", "bank", {})
    assert row["disposition"] == "hold"
    assert row["hold_seconds"] == 180
    assert row["row_key"] == "mosaic:eu:inv-883:bank"
    assert row["replay_generation"] == "d-9"
    assert row["source_channel"] == "bank"
