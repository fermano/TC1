"""Bound direct webhook replay batches by workspace limit."""

def bounded_batch(events: list[dict], workspace_limit: int) -> list[dict]:
    if workspace_limit < 0:
        raise ValueError("workspace limit cannot be negative")
    return events[:workspace_limit]
