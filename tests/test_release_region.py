import pytest

from src.region_policy import RegionDecision, RegionPolicy
from src.release_region import normalize_release_region, resolve_release_region


def test_normalizes_supported_aliases():
    assert normalize_release_region(" USE1 ") == "us-east-1"
    assert normalize_release_region("eu-west") == "eu-west-1"


def test_policy_selects_requested_alias_with_canonical_decision():
    policy = RegionPolicy(("us-east", "eu-west-1"), "eu-west")

    assert resolve_release_region(policy, " USE1 ") == RegionDecision(
        "us-east-1", "us-east-1", "requested"
    )


def test_policy_uses_default_only_when_request_is_absent():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "euw1")

    assert resolve_release_region(policy, None) == RegionDecision(
        None, "eu-west-1", "default"
    )
    assert resolve_release_region(policy, "   ") == RegionDecision(
        None, "eu-west-1", "default"
    )


def test_policy_rejects_explicit_disallowed_region():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "eu-west-1")

    with pytest.raises(ValueError, match="not allowed"):
        resolve_release_region(policy, "ap-south-1")


def test_policy_rejects_default_outside_allowlist():
    policy = RegionPolicy(("us-east-1",), "eu-west-1")

    with pytest.raises(ValueError, match="default region"):
        resolve_release_region(policy, None)


def test_legacy_form_selects_requested_alias_and_deduplicates_allowlist():
    allowed = ["us-east", "us-east-1", "eu-west"]

    assert resolve_release_region(" USE1 ", allowed, "eu-west") == "us-east-1"
    assert allowed == ["us-east", "us-east-1", "eu-west"]


@pytest.mark.parametrize("value", [None, "   "])
def test_legacy_form_uses_default_only_when_request_is_absent(value):
    assert (
        resolve_release_region(value, ["us-east-1", "eu-west-1"], "euw1")
        == "eu-west-1"
    )


def test_legacy_form_rejects_explicit_disallowed_region():
    with pytest.raises(ValueError, match="not allowed"):
        resolve_release_region(
            "ap-south-1",
            ["us-east-1", "eu-west-1"],
            "eu-west-1",
        )


def test_legacy_form_rejects_default_outside_allowlist():
    with pytest.raises(ValueError, match="default region"):
        resolve_release_region("use1", ["us-east-1"], "eu-west-1")


def test_legacy_form_accepts_one_pass_allowlist():
    allowed = (region for region in ["us-east", "eu-west"])

    assert resolve_release_region("euw1", allowed, "use1") == "eu-west-1"
