from src.release_watermark_view import (
    ReleaseWatermarkView,
    structured_release_watermark,
)


def test_reads_structured_final_release_watermark():
    assert structured_release_watermark(
        {"watermarks": {"release": {"id": " hx-120 ", "phase": " Final "}}}
    ) == ReleaseWatermarkView("hx-120", "final")


def test_leaves_missing_or_malformed_structured_release_watermark_empty():
    assert structured_release_watermark({}) == ReleaseWatermarkView(None, None)
    assert structured_release_watermark(
        {"watermarks": {"release": "hx-120"}}
    ) == ReleaseWatermarkView(None, None)
