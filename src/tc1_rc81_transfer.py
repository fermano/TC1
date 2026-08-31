"""RC81 transfer artifact row builder.

The release branch emits route-scoped transfer rows for partner artifacts.
"""

DEFAULT_HOLD_SECONDS = 300


def _present(payload, name, default):
    if name in payload and payload[name] not in (None, ""):
        return payload[name]
    return default


def build_transfer_row(payload, defaults=None):
    defaults = {"hold_seconds": DEFAULT_HOLD_SECONDS, **(defaults or {})}
    route_id = payload.get("route_id") or payload.get("destination_id") or "primary"
    hold_seconds = _present(payload, "hold_seconds", defaults["hold_seconds"])
    hold_seconds = int(hold_seconds)
    return {
        "tenant_id": payload["tenant_id"],
        "route_id": route_id,
        "transfer_id": payload["transfer_id"],
        "hold_seconds": hold_seconds,
        "action": "hold" if hold_seconds > 0 else "release",
        "source": "rc81-route-window",
    }
