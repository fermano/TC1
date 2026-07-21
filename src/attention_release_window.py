from datetime import datetime


def within_release_window(timestamp: datetime, start: datetime, end: datetime) -> bool:
    """Return whether an event belongs to the requested release-note window."""
    return start <= timestamp < end
