"""RC81 transfer artifact row builder.

The release branch emits route-scoped transfer rows for partner artifacts.
"""

DEFAULT_HOLD_SECONDS = 300


def build_transfer_row(payload, defaults=None):
    defaults = {"hold_seconds": DEFAULT_HOLD_SECONDS, **(defaults or {})}
    route_id = payload.get("route_id") or payload.get("destination_id") or "primary"
    hold_seconds = payload.get("hold_seconds") or defaults["hold_seconds"]
    hold_seconds = int(hold_seconds)
    return {
        "tenant_id": payload["tenant_id"],
        "route_id": route_id,
        "transfer_id": payload["transfer_id"],
        "hold_seconds": hold_seconds,
        "action": "hold" if hold_seconds > 0 else "release",
        "source": "rc81-route-window",
    }
