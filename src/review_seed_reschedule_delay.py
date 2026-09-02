"""Seed-only helper for the requested regression."""

def reschedule_delay(value, default=30):
    return default if value is None else int(value)
