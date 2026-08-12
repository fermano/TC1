from src.tc1_pause_window import build_pause_window


def test_pause_window_uses_default_for_missing_hold_seconds():
    window = build_pause_window({"tenant_id": "atlas", "route_id": "bank"}, workspace_default_seconds=180)

    assert window == {
        "tenant_id": "atlas",
        "route_id": "bank",
        "scope_key": "atlas:bank",
        "hold_seconds": 180,
    }


def test_pause_window_treats_blank_hold_seconds_as_default():
    window = build_pause_window(
        {"tenant_id": "atlas", "route_id": "bank", "hold_seconds": "  "},
        workspace_default_seconds=240,
    )

    assert window["hold_seconds"] == 240


def test_pause_window_prefers_current_route_over_legacy_route():
    window = build_pause_window(
        {
            "tenant_id": "atlas",
            "route_id": "bank",
            "legacy_route_id": "old-bank",
            "destination_id": "card",
        }
    )

    assert window["route_id"] == "bank"
    assert window["scope_key"] == "atlas:bank"


def test_pause_window_accepts_legacy_route_before_destination_fallback():
    window = build_pause_window(
        {"tenant_id": "atlas", "legacy_route_id": "legacy-bank", "destination_id": "card"}
    )

    assert window["route_id"] == "legacy-bank"
    assert window["scope_key"] == "atlas:legacy-bank"


def test_pause_window_preserves_zero_from_route_scoped_drain_record():
    window = build_pause_window(
        {
            "tenant_id": "atlas",
            "route_id": "bank",
            "legacy_route_id": "legacy-bank",
            "destination_id": "old-card",
            "pause_seconds": 0,
        },
        workspace_default_seconds=180,
    )

    assert window["route_id"] == "bank"
    assert window["scope_key"] == "atlas:bank"
    assert window["hold_seconds"] == 0


def test_pause_window_reads_string_pause_seconds_from_drain_record():
    window = build_pause_window(
        {"tenant_id": "atlas", "destination_id": "bank", "pause_seconds": "0"},
        workspace_default_seconds=180,
    )

    assert window["hold_seconds"] == 0


def test_pause_window_reads_dashboard_pause_seconds_string():
    window = build_pause_window(
        {"tenant_id": "atlas", "route_id": "bank", "pauseSeconds": "0"},
        workspace_default_seconds=180,
    )

    assert window["hold_seconds"] == 0


def test_pause_window_treats_blank_pause_aliases_as_default():
    window = build_pause_window(
        {"tenant_id": "atlas", "route_id": "bank", "pause_seconds": " ", "pauseSeconds": ""},
        workspace_default_seconds=210,
    )

    assert window["hold_seconds"] == 210
