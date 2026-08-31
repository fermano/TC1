from src.rc101_maple_invoice_gate import build_candidate_row


def test_partner_zero_wait_alias_is_ready():
    row = build_candidate_row(
        {"tenant": "maple", "invoice_id": "inv-774", "deferMinutes": "0"},
        {"route": "central", "default_defer_minutes": 30, "route_signature": "sig-maple-a"},
    )

    assert row["gate"] == "ready"
    assert row["wait_minutes"] == 0
