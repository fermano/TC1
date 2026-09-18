"""Earlier Mosaic value normalizer; implementation history only."""

def first_present_hold_seconds(payload, default_hold=180):
    for field in ("hold_seconds", "holdSeconds"):
        value = payload.get(field)
        if value not in (None, ""):
            return int(value)
    return default_hold
