"""Lease-grace parsing proposed for the delivery worker."""

DEFAULT_LEASE_GRACE_SECONDS = 30


def effective_lease_grace(configured_seconds, default_seconds=DEFAULT_LEASE_GRACE_SECONDS):
    """Return the configured grace period or the workspace default."""
    return configured_seconds or default_seconds
