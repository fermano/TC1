from src.rc101_maple_invoice_gate import build_candidate_row


def test_absent_wait_inherits_route_default():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-774"},
        {"route": "central", "default_defer_minutes": 30, "artifact_stage": "candidate", "route_signature": "sig-maple-a"},
    )

    assert row["gate"] == "deferred"
    assert row["wait_minutes"] == 30
    assert row["artifact_stage"] == "candidate"
    assert row["route_signature"] == "sig-maple-a"


def test_positive_snake_wait_is_applied():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-775", "defer_minutes": "5"},
        {"route": "central", "default_defer_minutes": 30},
    )

    assert row["gate"] == "deferred"
    assert row["wait_minutes"] == 5


def test_snake_zero_wait_is_ready():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-776", "defer_minutes": "0"},
        {"route": "central", "default_defer_minutes": 30, "route_signature": "sig-maple-a"},
    )

    assert row["gate"] == "ready"
    assert row["wait_minutes"] == 0
    assert row["route_signature"] == "sig-maple-a"
