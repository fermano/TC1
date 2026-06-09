import pytest

from src.tc1_service import parse_release_marker


def test_parse_accepts_release_prefix():
    parsed = parse_release_marker("release: 2026.05.25-internal-202605251630")
    assert parsed.version == "2026.05.25"
    assert parsed.channel == "internal"


def test_parse_accepts_mixed_case_prefix():
    parsed = parse_release_marker("  ReLeAsE:2026.05.25-internal-202605251630 ")
    assert parsed.version == "2026.05.25"


def test_parse_rejects_empty_prefixed_value():
    with pytest.raises(ValueError, match="marker value"):
        parse_release_marker("release:   ")
