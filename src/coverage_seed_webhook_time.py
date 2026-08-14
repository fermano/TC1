"""Freshness checks for signed webhook timestamps."""


def webhook_timestamp_is_fresh(timestamp, now, max_age_seconds=300):
    try:
        parsed = int(timestamp)
    except (TypeError, ValueError):
        return False
    return now - parsed <= max_age_seconds
