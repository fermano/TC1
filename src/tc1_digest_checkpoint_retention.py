"""Checkpoint-retention helpers for TC1 retry digest cleanup."""


def should_remove_checkpoint(row):
    """Return whether a retry checkpoint row can be deleted by digest cleanup."""
    if row.get("state") in {"delivered", "canceled"}:
        return True
    if row.get("retained_for_replay"):
        return False
    return row.get("age_hours", 0) > 72
