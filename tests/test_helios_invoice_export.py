from src.helios_invoice_export import helios_export_reference


def test_helios_export_uses_existing_release_watermark():
    assert helios_export_reference({"release_watermark": " hx-118 "}) == "hx-118"


def test_helios_export_uses_final_structured_watermark_when_legacy_is_blank():
    assert (
        helios_export_reference(
            {
                "release_watermark": " ",
                "watermarks": {"release": {"id": "hx-120", "phase": "final"}},
            }
        )
        == "hx-120"
    )


def test_helios_export_keeps_legacy_watermark_when_structured_is_prepared():
    assert (
        helios_export_reference(
            {
                "release_watermark": "hx-118",
                "watermarks": {"release": {"id": "hx-120", "phase": "prepared"}},
            }
        )
        == "hx-118"
    )


def test_helios_export_omits_blank_or_missing_release_watermark():
    assert helios_export_reference({}) is None
    assert helios_export_reference({"release_watermark": " "}) is None


def test_helios_export_omits_nonfinal_structured_watermark_without_legacy():
    assert (
        helios_export_reference(
            {
                "release_watermark": " ",
                "watermarks": {"release": {"id": "hx-120", "phase": "prepared"}},
            }
        )
        is None
    )
