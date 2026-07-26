"""Owner selection for delayed delivery attempts."""


def owner_for_attempt(original_owner, owner_override=None):
    """Return the owner recorded for a resumed attempt."""
    return owner_override or original_owner
