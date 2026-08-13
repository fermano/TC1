from src.tc1_lagoon_release_window import release_dispatch_record


def test_release_window_uses_route_scope():
    row = {"tenant_id": "lagoon", "route_id": "sms", "route_window_seconds": 90}
    assert release_dispatch_record(row) == {
        "scope_key": "lagoon:sms",
        "window_seconds": 90,
        "source": "rc74-route-scoped",
    }


def test_release_window_falls_back_to_default_when_blank():
    row = {"tenant_id": "lagoon", "route_id": "email", "window_seconds": ""}
    assert release_dispatch_record(row, workspace_default=240)["window_seconds"] == 240
