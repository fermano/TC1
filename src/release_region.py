from __future__ import annotations

from collections.abc import Mapping
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


def resolve_release_region_request(
    policy: RegionPolicy,
    values: Mapping[str, str | None],
) -> RegionDecision:
    """Resolve current and compatibility region fields in one place.

    The current region is authoritative when it contains a value. A blank or
    omitted current field may use the compatibility region_hint during the
    release transition. Both values use the same policy validation.
    """
    current = values.get("region")
    if current is not None and current.strip():
        return _resolve_region_decision(policy, current)

    compatibility = values.get("region_hint")
    if compatibility is not None and compatibility.strip():
        decision = _resolve_region_decision(policy, compatibility)
        return RegionDecision(
            decision.requested_region,
            decision.selected_region,
            "compatibility",
        )

    return _resolve_region_decision(policy, None)


def resolve_release_region(
    policy: RegionPolicy,
    value: str | None,
) -> RegionDecision:
    """Select an allowed region using the canonical policy interface."""
    return _resolve_region_decision(policy, value)
