from dataclasses import FrozenInstanceError

import pytest

from src.region_policy import RegionDecision, RegionPolicy


def test_region_policy_is_immutable():
    policy = RegionPolicy(("us-east-1",), "us-east-1")

    with pytest.raises(FrozenInstanceError):
        policy.default_region = "eu-west-1"


def test_region_decision_keeps_selection_source():
    requested = RegionDecision("us-east-1", "us-east-1", "requested")
    defaulted = RegionDecision(None, "us-east-1", "default")

    assert requested != defaulted
