"""Read-time ordering workaround; scale and missing-event tests are absent."""

def sort_events(events: list[dict]) -> list[dict]:
    return sorted(events, key=lambda event: (event.get("timestamp", ""), event.get("id", "")))
