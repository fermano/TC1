import pytest

from src.region_policy import RegionDecision, RegionPolicy
from src.release_region import (
    normalize_release_region,
    resolve_release_region,
    resolve_release_region_request,
)


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


def test_request_prefers_nonblank_current_region_over_compatibility_hint():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "eu-west-1")

    assert resolve_release_region_request(
        policy, {"region": " USE1 ", "region_hint": "euw1"}
    ) == RegionDecision("us-east-1", "us-east-1", "requested")


def test_request_uses_compatibility_hint_when_current_region_is_blank():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "us-east-1")

    assert resolve_release_region_request(
        policy, {"region": " ", "region_hint": " EUW1 "}
    ) == RegionDecision("eu-west-1", "eu-west-1", "compatibility")


def test_request_defaults_when_both_region_forms_are_blank_or_missing():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "euw1")

    assert resolve_release_region_request(policy, {}) == RegionDecision(
        None, "eu-west-1", "default"
    )
    assert resolve_release_region_request(
        policy, {"region": "", "region_hint": " "}
    ) == RegionDecision(None, "eu-west-1", "default")


def test_request_rejects_explicit_disallowed_current_region_even_with_hint():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "eu-west-1")

    with pytest.raises(ValueError, match="not allowed"):
        resolve_release_region_request(
            policy, {"region": "ap-south-1", "region_hint": "euw1"}
        )
