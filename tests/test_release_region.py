import pytest

from src.release_region import normalize_release_region, resolve_release_region


def test_normalizes_supported_aliases():
    assert normalize_release_region(" USE1 ") == "us-east-1"
    assert normalize_release_region("eu-west") == "eu-west-1"


def test_resolves_allowed_alias_and_deduplicates_allowlist():
    assert resolve_release_region(
        " USE1 ",
        ["us-east", "us-east-1", "eu-west"],
        "eu-west",
    ) == "us-east-1"


def test_blank_or_unknown_request_falls_back_to_default():
    allowed = ["us-east-1", "eu-west-1"]

    assert resolve_release_region("   ", allowed, "euw1") == "eu-west-1"
    assert resolve_release_region("ap-south-1", allowed, "euw1") == "eu-west-1"


def test_rejects_default_outside_allowlist():
    with pytest.raises(ValueError, match="default region"):
        resolve_release_region("use1", ["us-east-1"], "eu-west-1")
