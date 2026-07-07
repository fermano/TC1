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
