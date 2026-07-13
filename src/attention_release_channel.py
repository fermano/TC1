CHANNEL_ALIASES = {"stable": "ga", "general-availability": "ga"}


def normalize_release_channel(channel: str) -> str:
    key = channel.strip().lower()
    return CHANNEL_ALIASES.get(key, key)
