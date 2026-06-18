from src.deployment_plan_region import deployment_plan_region


def test_deployment_plan_uses_canonical_region():
    assert deployment_plan_region("USE1") == "us-east-1"
