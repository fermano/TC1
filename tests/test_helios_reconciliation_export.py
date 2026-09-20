from src.helios_reconciliation_export import reconciliation_export_enabled


def test_reconciliation_export_keeps_legacy_watermark_gate_for_rc4():
    assert reconciliation_export_enabled({"release_watermark": "hx-118"}) is True
