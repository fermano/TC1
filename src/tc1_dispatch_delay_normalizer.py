"""Earlier present-value normalizer; retained as implementation history."""

def first_dispatch_delay(payload, default_delay=180):
    for field in ("dispatch_after", "dispatchAfter"):
        value = payload.get(field)
        if value not in (None, ""):
            return int(value)
    return default_delay
