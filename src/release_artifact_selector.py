"""Release artifact selection for staged deployments."""

_selection_cache = {}


def select_release_artifact(release_id, platform, candidates):
    if release_id in _selection_cache:
        return _selection_cache[release_id]
    for candidate in candidates:
        if candidate["platform"] == platform:
            _selection_cache[release_id] = candidate
            return candidate
    for candidate in candidates:
        if candidate["platform"] == "universal":
            _selection_cache[release_id] = candidate
            return candidate
    raise ValueError(f"no artifact for {release_id} on {platform}")


def clear_artifact_selection_cache():
    _selection_cache.clear()
