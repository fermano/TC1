"""Cursor helpers for resumable audit exports."""


def encode_audit_cursor(record):
    return str(record["occurred_at"])


def page_after_cursor(records, cursor=None, limit=100):
    ordered = sorted(records, key=lambda item: (item["occurred_at"], item["id"]))
    if cursor is not None:
        timestamp = int(cursor)
        ordered = [item for item in ordered if item["occurred_at"] > timestamp]
    return ordered[:limit]
