import pytest

from src.rc101_maple_invoice_gate import build_candidate_row


def test_absent_wait_inherits_route_default():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-774"},
        {"route": "central", "default_defer_minutes": 30, "artifact_stage": "candidate", "route_signature": "sig-maple-a", "release_channel": "rc101-final"},
    )

    assert row["gate"] == "deferred"
    assert row["wait_minutes"] == 30
    assert row["artifact_stage"] == "candidate"
    assert row["route_signature"] == "sig-maple-a"
    assert row["release_channel"] == "rc101-final"


def test_positive_snake_wait_is_applied():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-775", "defer_minutes": "5"},
        {"route": "central", "default_defer_minutes": 30},
    )

    assert row["gate"] == "deferred"
    assert row["wait_minutes"] == 5
    assert row["release_channel"] == "candidate"


@pytest.mark.parametrize("value", ["0", 0])
def test_snake_zero_wait_is_ready(value):
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-776", "defer_minutes": value},
        {"route": "central", "default_defer_minutes": 30, "route_signature": "sig-maple-a"},
    )

    assert row["gate"] == "ready"
    assert row["wait_minutes"] == 0
    assert row["route_signature"] == "sig-maple-a"


@pytest.mark.parametrize("value", ["0", 0])
def test_partner_zero_wait_preserves_b17_release_row(value):
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-774", "deferMinutes": value},
        {
            "route": "central",
            "default_defer_minutes": 30,
            "artifact_stage": "candidate",
            "route_signature": "sig-maple-a",
            "release_channel": "rc101-final",
        },
    )

    assert row == {
        "tenant": "maple",
        "invoice_id": "inv-774",
        "route": "central",
        "gate": "ready",
        "wait_minutes": 0,
        "artifact_stage": "candidate",
        "route_signature": "sig-maple-a",
        "release_channel": "rc101-final",
    }


@pytest.mark.parametrize("value", ["5", 5])
def test_positive_partner_wait_is_applied(value):
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-775", "deferMinutes": value},
        {"route": "central", "default_defer_minutes": 30},
    )

    assert row["gate"] == "deferred"
    assert row["wait_minutes"] == 5


@pytest.mark.parametrize("field", ["deferMinutes", "defer_minutes"])
@pytest.mark.parametrize("value", [None, ""])
@pytest.mark.parametrize("default", [0, 12])
def test_empty_wait_inherits_route_default(field, value, default):
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-774", field: value},
        {"route": "central", "default_defer_minutes": default},
    )

    assert row["wait_minutes"] == default
    assert row["gate"] == ("deferred" if default else "ready")


@pytest.mark.parametrize(
    "partner, snake, expected",
    [("0", "5", 0), (0, 5, 0), ("5", "0", 5), ("", "5", 12), (None, "5", 12)],
)
def test_present_partner_alias_takes_precedence(partner, snake, expected):
    row = build_candidate_row(
        {
            "tenant": "maple",
            "invoice_id": "inv-774",
            "deferMinutes": partner,
            "defer_minutes": snake,
        },
        {"route": "central", "default_defer_minutes": 12},
    )

    assert row["wait_minutes"] == expected
    assert row["gate"] == ("deferred" if expected else "ready")


def test_absent_wait_preserves_builtin_defaults():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-774"},
        {"route": "central"},
    )

    assert row == {
        "tenant": "maple",
        "invoice_id": "inv-774",
        "route": "central",
        "gate": "deferred",
        "wait_minutes": 30,
        "artifact_stage": "rc101",
        "route_signature": "unset",
        "release_channel": "candidate",
    }
