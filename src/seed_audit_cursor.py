"""Cursor helpers for resumable audit exports."""


def encode_audit_cursor(record):
    return str(record["occurred_at"])


def page_after_cursor(records, cursor=None, limit=100):
    ordered = sorted(records, key=lambda item: (item["occurred_at"], item["id"]))
    if cursor is None:
        return ordered[:limit]

    timestamp = int(cursor)
    boundary = [item for item in ordered if item["occurred_at"] == timestamp]
    newer = [item for item in ordered if item["occurred_at"] > timestamp]

    if len(boundary) > 1:
        # A decimal timestamp cannot identify which tied event was emitted before
        # the cursor was persisted. Replay the complete boundary group; callers
        # deduplicate these records by event ID. Replays do not consume the page
        # budget so the cursor can still advance to a newer timestamp.
        return boundary + newer[:limit]

    return newer[:limit]
