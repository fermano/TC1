"""Earlier retry-window normalizer, retained as implementation history."""

def first_partner_window(payload, default_wait=180):
    for field in ("retry_window", "retryWindow"):
        value = payload.get(field)
        if value not in (None, ""):
            return int(value)
    return default_wait
