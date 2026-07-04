"""Use durable notification idempotency keys."""

def delivery_key(export_id: str, notification_kind: str) -> str:
    return f"{export_id}:{notification_kind}"
