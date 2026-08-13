from src.tc1_harbor_invoice_gate import invoice_gate_record


def test_invoice_gate_uses_lane_key_for_bank_route():
    row = {"tenant_id": "harbor", "route_id": "bank", "invoice_id": "inv-992", "route_gate_seconds": 90}
    assert invoice_gate_record(row) == {
        "lane_key": "harbor:bank:inv-992",
        "gate_seconds": 90,
        "source": "rc75-lane-scoped",
    }


def test_invoice_gate_blank_value_uses_default_for_email_route():
    row = {"tenant_id": "harbor", "route_id": "email", "invoice_id": "inv-992", "gate_seconds": ""}
    assert invoice_gate_record(row, default_seconds=45) == {
        "lane_key": "harbor:email:inv-992",
        "gate_seconds": 45,
        "source": "rc75-lane-scoped",
    }


def test_invoice_gate_preserves_explicit_zero_for_bank_route():
    row = {
        "tenant_id": "harbor",
        "route_id": "bank",
        "invoice_id": "inv-992",
        "cancel_after_seconds": 0,
    }
    assert invoice_gate_record(row, default_seconds=45) == {
        "lane_key": "harbor:bank:inv-992",
        "gate_seconds": 0,
        "source": "rc75-lane-scoped",
    }


def test_invoice_gate_preserves_string_zero_legacy_gate_delay():
    row = {
        "tenant_id": "harbor",
        "route_id": "bank",
        "invoice_id": "inv-992",
        "gate_delay_seconds": "0",
    }
    assert invoice_gate_record(row, default_seconds=45)["gate_seconds"] == 0
