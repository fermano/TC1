from src.invoice_export_watermark import invoice_export_is_deliverable


def test_rejects_missing_watermark():
    assert invoice_export_is_deliverable({}) is False


def test_accepts_release_watermark():
    assert invoice_export_is_deliverable({"release_watermark": "rc-2026.06.24"}) is True
