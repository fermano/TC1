"""Helpers for normalizing TC1 delivery pause windows."""

DEFAULT_PAUSE_SECONDS = 300


def _coerce_seconds(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return None
    return int(value)


def resolve_route_id(record):
    route_id = record.get("route_id")
    if route_id is None or str(route_id).strip() == "":
        route_id = record.get("destination_id") or "default"
    return str(route_id).strip()


def build_pause_window(record, workspace_default_seconds=DEFAULT_PAUSE_SECONDS):
    """Return the delivery pause window used by retry and drain workers."""
    tenant_id = str(record.get("tenant_id") or "")
    hold_seconds = _coerce_seconds(record.get("hold_seconds"))
    if hold_seconds is None:
        hold_seconds = int(workspace_default_seconds)

    route_id = resolve_route_id(record)
    return {
        "tenant_id": tenant_id,
        "route_id": route_id,
        "hold_seconds": hold_seconds,
    }
