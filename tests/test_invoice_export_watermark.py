from src.invoice_export_watermark import invoice_export_is_deliverable


def test_rejects_missing_structured_watermark():
    assert invoice_export_is_deliverable({}) is False


def test_accepts_final_structured_release_watermark():
    assert invoice_export_is_deliverable(
        {"watermarks": {"release": {"id": "rc-2026.06.24", "phase": "final"}}}
    ) is True


def test_rejects_prepared_structured_release_watermark():
    assert invoice_export_is_deliverable(
        {"watermarks": {"release": {"id": "rc-2026.06.24", "phase": "prepared"}}}
    ) is False
