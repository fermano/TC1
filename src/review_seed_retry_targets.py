"""Seed-only review fixture for replay identity."""

def retry_target_key(tenant_id, route_id, event_id):
    return f"{tenant_id}:{event_id}"
