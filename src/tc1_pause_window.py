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


def _first_seconds(record, keys):
    for key in keys:
        value = _coerce_seconds(record.get(key))
        if value is not None:
            return value
    return None


def _first_non_blank(record, keys):
    for key in keys:
        value = record.get(key)
        if value is not None and str(value).strip() != "":
            return value
    return None


def resolve_route_id(record):
    route_id = _first_non_blank(record, ("route_id", "legacy_route_id", "destination_id"))
    if route_id is None:
        return "default"
    return str(route_id).strip()


def _scope_key(tenant_id, route_id):
    return f"{tenant_id}:{route_id}"


def build_pause_window(record, workspace_default_seconds=DEFAULT_PAUSE_SECONDS):
    """Return the route-scoped pause window used by retry and drain workers."""
    tenant_id = str(record.get("tenant_id") or "")
    hold_seconds = _first_seconds(record, ("hold_seconds", "pause_seconds", "pauseSeconds"))
    if hold_seconds is None:
        hold_seconds = int(workspace_default_seconds)

    route_id = resolve_route_id(record)
    return {
        "tenant_id": tenant_id,
        "route_id": route_id,
        "scope_key": _scope_key(tenant_id, route_id),
        "hold_seconds": hold_seconds,
    }
