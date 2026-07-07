import pytest

from src.release_marker_preview import parse_release_marker_preview


def test_release_marker_preview_keeps_plain_marker() -> None:
    assert parse_release_marker_preview("  20260603-rc1  ") == "20260603-rc1"


def test_release_marker_preview_accepts_support_prefix() -> None:
    assert parse_release_marker_preview(" ReLeAsE: 20260603-rc1 ") == "20260603-rc1"


def test_release_marker_preview_rejects_empty_support_prefix() -> None:
    with pytest.raises(ValueError, match="must include a value"):
        parse_release_marker_preview(" release:   ")
