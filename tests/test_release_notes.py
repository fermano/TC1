from src.release_notes import build_release_marker


def test_blank_release_marker_channel_uses_internal_default():
    assert build_release_marker("2026.06.24", "") == "2026.06.24-internal"
    assert build_release_marker("2026.06.24", "   ") == "2026.06.24-internal"
