from src.region_policy import RegionPolicy
from src.solstice_packet import resolve_solstice_packet_region


def test_solstice_packet_uses_requested_region():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "eu-west-1")

    assert resolve_solstice_packet_region(policy, {"region": "use1"}) == "us-east-1"


def test_solstice_packet_uses_policy_default_when_region_is_blank():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "euw1")

    assert resolve_solstice_packet_region(policy, {"region": " "}) == "eu-west-1"


def test_solstice_packet_accepts_compatibility_region_hint():
    policy = RegionPolicy(("us-east-1", "eu-west-1"), "us-east-1")

    assert resolve_solstice_packet_region(
        policy, {"region": "", "region_hint": "euw1"}
    ) == "eu-west-1"
