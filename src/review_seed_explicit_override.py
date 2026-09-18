"""Seed-only review fixture for explicit overrides."""

def effective_override(value, default=30):
    return default if value is None else value
