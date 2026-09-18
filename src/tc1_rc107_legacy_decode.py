"""Earlier legacy replay-key decoder; implementation history only."""

def decode_legacy_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "primary")
    return tuple(parts)
