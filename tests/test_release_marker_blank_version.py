from src.tc1_service import build_release_marker, parse_release_marker

import pytest


def test_build_release_marker_rejects_blank_version():
    with pytest.raises(ValueError, match="must not be blank"):
        build_release_marker("   ", "internal")


def test_build_release_marker_rejects_empty_version():
    with pytest.raises(ValueError, match="must not be blank"):
        build_release_marker("", "internal")


def test_build_release_marker_trims_surrounding_whitespace_in_version():
    marker = build_release_marker("  2026.05.25  ", "internal")
    assert marker.startswith("2026.05.25-internal-")
    assert parse_release_marker(marker).version == "2026.05.25"
