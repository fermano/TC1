"""Retry-After parsing for delivery handoffs."""


def parse_retry_after(value, now_epoch=None):
    """Return a non-negative delay in seconds for a numeric Retry-After value."""
    if value is None or not value.strip():
        return None
    return max(0, int(value.strip()))
