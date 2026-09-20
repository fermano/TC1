from src.release_watermark_view import structured_release_watermark


def invoice_export_is_deliverable(metadata):
    watermark = structured_release_watermark(metadata)
    return bool(watermark.value and watermark.phase == "final")
