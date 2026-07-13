def parse_release_marker(value: str) -> tuple[str, str]:
    """Parse the required channel:version release marker."""
    channel, separator, version = value.strip().partition(":")
    if not separator or not channel or not version:
        raise ValueError("release marker must be channel:version")
    return channel, version
