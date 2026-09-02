"""Seed-only review fixture for explicit overrides."""

def effective_override(value, default=30):
    return value or default
