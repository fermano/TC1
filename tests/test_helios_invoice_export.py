from src.helios_invoice_export import helios_export_reference


def test_helios_export_uses_final_structured_release_watermark():
    assert helios_export_reference(
        {"watermarks": {"release": {"id": "hx-120", "phase": "final"}}}
    ) == "hx-120"


def test_helios_export_omits_nonfinal_structured_release_watermark():
    assert helios_export_reference(
        {"watermarks": {"release": {"id": "hx-120", "phase": "prepared"}}}
    ) is None
