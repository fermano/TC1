REGION_ALIASES = {
    "us-east": "us-east-1",
    "use1": "us-east-1",
    "eu-west": "eu-west-1",
    "euw1": "eu-west-1",
}


def normalize_release_region(value):
    key = value.strip().lower()
    return REGION_ALIASES.get(key, key)


def resolve_release_region(value, allowed_regions, default_region):
    """Resolve a requested region against a legacy workspace allowlist."""
    normalized_allowed = tuple(
        dict.fromkeys(normalize_release_region(region) for region in allowed_regions)
    )
    normalized_default = normalize_release_region(default_region)
    if normalized_default not in normalized_allowed:
        raise ValueError("default region must be present in allowed regions")

    requested = normalize_release_region(value) if value is not None else ""
    if not requested or requested not in normalized_allowed:
        return normalized_default
    return requested
