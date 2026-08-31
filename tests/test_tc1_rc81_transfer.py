import pytest

from src.tc1_rc81_transfer import ARTIFACT_SCHEMA, build_transfer_row


def test_uses_route_scoped_shape():
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "ach",
        "transfer_id": "tr-884",
        "hold_seconds": 45,
    })
    assert row["route_id"] == "ach"
    assert row["action"] == "hold"
    assert row["source"] == "rc81-route-window"
    assert row["artifact_schema"] == ARTIFACT_SCHEMA
    assert row["operator_key"] == "ach:tr-884:hold"


def test_defaults_missing_hold_window():
    row = build_transfer_row({"tenant_id": "kitebank", "route_id": "wire", "transfer_id": "tr-101"})
    assert row["hold_seconds"] == 300
    assert row["action"] == "hold"


@pytest.mark.parametrize("field", ["hold_seconds", "holdSeconds"])
@pytest.mark.parametrize("value", [0, "0"])
def test_explicit_zero_releases_route_artifact(field, value):
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "ach",
        "destination_id": "legacy-destination",
        "transfer_id": "tr-884",
        field: value,
    })
    assert row == {
        "tenant_id": "kitebank",
        "route_id": "ach",
        "transfer_id": "tr-884",
        "hold_seconds": 0,
        "action": "release",
        "source": "rc81-route-window",
        "artifact_schema": ARTIFACT_SCHEMA,
        "operator_key": "ach:tr-884:release",
    }


@pytest.mark.parametrize("value", [45, "45"])
def test_positive_partner_window_holds(value):
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "ach",
        "transfer_id": "tr-884",
        "holdSeconds": value,
    })
    assert row["hold_seconds"] == 45
    assert row["action"] == "hold"
    assert row["operator_key"] == "ach:tr-884:hold"


@pytest.mark.parametrize("window", [
    {},
    {"hold_seconds": None},
    {"hold_seconds": ""},
    {"holdSeconds": None},
    {"holdSeconds": ""},
    {"hold_seconds": None, "holdSeconds": ""},
    {"hold_seconds": "", "holdSeconds": None},
])
@pytest.mark.parametrize("default", [75, 0, "0"])
def test_missing_or_blank_windows_inherit_workspace_default(window, default):
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "wire",
        "transfer_id": "tr-884",
        **window,
    }, {"hold_seconds": default})
    action = "hold" if int(default) > 0 else "release"
    assert row["hold_seconds"] == int(default)
    assert row["action"] == action
    assert row["operator_key"] == f"wire:tr-884:{action}"


@pytest.mark.parametrize("snake,camel,expected", [
    (0, 45, 0),
    ("0", 45, 0),
    (45, 0, 45),
    ("45", "0", 45),
    (None, "0", 0),
    ("", 0, 0),
    (None, 45, 45),
    ("", "45", 45),
])
def test_snake_case_takes_precedence_unless_missing_or_blank(snake, camel, expected):
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "route_id": "ach",
        "transfer_id": "tr-884",
        "hold_seconds": snake,
        "holdSeconds": camel,
    })
    assert row["hold_seconds"] == expected


@pytest.mark.parametrize("identity,expected_route", [
    ({"destination_id": "legacy-ach"}, "legacy-ach"),
    ({"route_id": "", "destination_id": "legacy-ach"}, "legacy-ach"),
    ({}, "primary"),
])
def test_route_fallbacks_preserve_current_artifact_identity(identity, expected_route):
    row = build_transfer_row({
        "tenant_id": "kitebank",
        "transfer_id": "tr-884",
        "holdSeconds": "0",
        **identity,
    })
    assert row["route_id"] == expected_route
    assert row["operator_key"] == f"{expected_route}:tr-884:release"
    assert "destination_id" not in row


def test_partner_replay_keeps_same_transfer_routes_separate():
    payload = {"tenant_id": "kitebank", "transfer_id": "tr-884"}
    ach = build_transfer_row({**payload, "route_id": "ach", "holdSeconds": "0"})
    wire = build_transfer_row({**payload, "route_id": "wire", "holdSeconds": ""})
    assert (ach["route_id"], ach["hold_seconds"], ach["operator_key"]) == (
        "ach", 0, "ach:tr-884:release",
    )
    assert (wire["route_id"], wire["hold_seconds"], wire["operator_key"]) == (
        "wire", 300, "wire:tr-884:hold",
    )
