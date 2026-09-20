from src.helios_invoice_export import helios_export_reference


def test_helios_export_uses_existing_release_watermark():
    assert helios_export_reference({"release_watermark": " hx-118 "}) == "hx-118"


def test_helios_export_omits_blank_or_missing_release_watermark():
    assert helios_export_reference({}) is None
    assert helios_export_reference({"release_watermark": " "}) is None
