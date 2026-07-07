"""Release artifact selection for staged deployments."""


def select_release_artifact(release_id, platform, candidates):
    for candidate in candidates:
        if candidate["platform"] == platform:
            return candidate
    for candidate in candidates:
        if candidate["platform"] == "universal":
            return candidate
    raise ValueError(f"no artifact for {release_id} on {platform}")
