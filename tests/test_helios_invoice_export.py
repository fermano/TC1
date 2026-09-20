from src.helios_invoice_export import helios_export_reference


def test_helios_export_uses_structured_release_watermark():
    assert helios_export_reference(
        {"watermarks": {"release": {"id": "hx-120", "phase": "final"}}}
    ) == "hx-120"


def test_helios_export_keeps_existing_release_watermark():
    assert helios_export_reference({"release_watermark": " hx-118 "}) == "hx-118"
