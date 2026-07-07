from __future__ import annotations


REGION_ALIASES = {
    "us-east": "us-east-1",
    "use1": "us-east-1",
    "eu-west": "eu-west-1",
    "euw1": "eu-west-1",
}

from src.region_policy import RegionDecision, RegionPolicy


def normalize_release_region(value):
    key = value.strip().lower()
    return REGION_ALIASES.get(key, key)


def resolve_release_region(policy: RegionPolicy, value: str | None) -> RegionDecision:
    """Select a canonical allowed region without silently changing geography."""
    allowed = tuple(
        dict.fromkeys(normalize_release_region(region) for region in policy.allowed_regions)
    )
    default = normalize_release_region(policy.default_region)
    if default not in allowed:
        raise ValueError("default region must be present in allowed regions")

    requested = normalize_release_region(value) if value is not None else ""
    if not requested:
        return RegionDecision(None, default, "default")
    if requested not in allowed:
        raise ValueError(f"release region is not allowed: {requested}")
    return RegionDecision(requested, requested, "requested")
