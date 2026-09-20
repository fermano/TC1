from src.helios_preview_export import preview_has_release_reference


def test_helios_preview_keeps_legacy_watermark_contract():
    assert preview_has_release_reference({"release_watermark": "hx-118"}) is True
