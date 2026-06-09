import pytest

from src.tc1_service import build_release_marker, parse_release_marker


def test_build_release_marker_rejects_hyphenated_version():
    with pytest.raises(ValueError, match="reserved field delimiter"):
        build_release_marker("1.4.0-rc1", "prod")


def test_build_release_marker_allows_dotted_version_round_trip():
    marker = build_release_marker("2026.06.09", "Prod Ops")
    parsed = parse_release_marker(marker)
    assert parsed.version == "2026.06.09"
    assert parsed.channel == "prod-ops"
