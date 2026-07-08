"""Release artifact selection for staged deployments."""

_selection_cache = {}

_PLATFORM_ALIASES = {
    "linux/x86_64": "linux-amd64",
    "linux/aarch64": "linux-arm64",
}


def normalize_platform(platform):
    key = platform.strip().lower()
    return _PLATFORM_ALIASES.get(key, key)


def select_release_artifact(release_id, platform, candidates):
    platform = normalize_platform(platform)
    cache_key = (release_id, platform)
    if cache_key in _selection_cache:
        return _selection_cache[cache_key]
    for candidate in candidates:
        if normalize_platform(candidate["platform"]) == platform:
            _selection_cache[cache_key] = candidate
            return candidate
    for candidate in candidates:
        if normalize_platform(candidate["platform"]) == "universal":
            _selection_cache[cache_key] = candidate
            return candidate
    raise ValueError(f"no artifact for {release_id} on {platform}")


def clear_artifact_selection_cache():
    _selection_cache.clear()
