from src.helios_preview_export import preview_has_release_reference


def test_helios_preview_accepts_final_structured_watermark():
    assert preview_has_release_reference(
        {"watermarks": {"release": {"id": "hx-120", "phase": "final"}}}
    ) is True
