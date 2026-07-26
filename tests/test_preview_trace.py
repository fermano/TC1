from src.preview_trace import preview_trace_label


def test_preview_trace_label_includes_source_and_id():
    assert preview_trace_label("tr-18", "csv") == "csv:tr-18"


def test_preview_trace_label_normalizes_missing_source():
    assert preview_trace_label("tr-19", "  ") == "unknown:tr-19"
