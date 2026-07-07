from __future__ import annotations

from collections.abc import Iterable
from typing import overload

from src.region_policy import RegionDecision, RegionPolicy


REGION_ALIASES = {
    "us-east": "us-east-1",
    "use1": "us-east-1",
    "eu-west": "eu-west-1",
    "euw1": "eu-west-1",
}

_UNSET = object()


def normalize_release_region(value):
    key = value.strip().lower()
    return REGION_ALIASES.get(key, key)


def _resolve_region_decision(
    policy: RegionPolicy, value: str | None
) -> RegionDecision:
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


@overload
def resolve_release_region(
    policy: RegionPolicy, value: str | None
) -> RegionDecision: ...


@overload
def resolve_release_region(
    value: str | None,
    allowed_regions: Iterable[str],
    default_region: str,
) -> str: ...


def resolve_release_region(
    policy_or_value,
    value_or_allowed_regions,
    default_region=_UNSET,
):
    """Select an allowed release region without silently changing geography.

    The two-argument ``(RegionPolicy, value)`` form is canonical. The legacy
    ``(value, allowed_regions, default_region)`` form returns a string and is
    retained for one release window; it delegates to the same policy engine.
    """
    if default_region is _UNSET:
        return _resolve_region_decision(policy_or_value, value_or_allowed_regions)

    policy = RegionPolicy(tuple(value_or_allowed_regions), default_region)
    return _resolve_region_decision(policy, policy_or_value).selected_region
