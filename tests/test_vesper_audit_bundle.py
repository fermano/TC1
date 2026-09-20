from src.vesper_audit_bundle import audit_bundle_settlement


def test_audit_bundle_uses_rc1_settlement_adapter():
    metadata = {"settlement_token": "vs-118", "settlement_phase": "committed"}

    assert audit_bundle_settlement(metadata) == {"settlement_reference": "vs-118"}
