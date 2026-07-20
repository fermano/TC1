"""Composite audit cursor prototype."""


def encode_composite_cursor(record):
    return f"v2:{record['occurred_at']}:{record['id']}"


def decode_composite_cursor(cursor):
    if cursor.startswith("v2:"):
        _, timestamp, record_id = cursor.split(":", 2)
        return int(timestamp), record_id
    return int(cursor), "\uffff"


def page_after_composite_cursor(records, cursor=None, limit=100):
    ordered = sorted(records, key=lambda item: (item["occurred_at"], item["id"]))
    if cursor is not None:
        boundary = decode_composite_cursor(cursor)
        ordered = [item for item in ordered if (item["occurred_at"], item["id"]) > boundary]
    return ordered[:limit]
