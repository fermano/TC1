"""Birch partner-event intake."""

def source_for(event):
    for field in ("source", "sourceId"):
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        return value
    return "primary"


def hold_for(event, default_seconds):
    for field in ("hold_seconds", "holdSeconds"):
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        return int(value)
    return default_seconds
