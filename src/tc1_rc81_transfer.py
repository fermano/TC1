"""Prototype transfer window normalizer from before RC81 route rows."""

DEFAULT_HOLD_SECONDS = 300


def _hold_seconds(payload, default=DEFAULT_HOLD_SECONDS):
    if "hold_seconds" in payload and payload["hold_seconds"] not in (None, ""):
        return int(payload["hold_seconds"])
    if "holdSeconds" in payload and payload["holdSeconds"] not in (None, ""):
        return int(payload["holdSeconds"])
    return default


def build_transfer_row(payload, defaults=None):
    defaults = {"hold_seconds": DEFAULT_HOLD_SECONDS, **(defaults or {})}
    hold_seconds = _hold_seconds(payload, defaults["hold_seconds"])
    return {
        "tenant_id": payload["tenant_id"],
        "destination_id": payload.get("destination_id") or payload.get("route_id") or "primary",
        "transfer_id": payload["transfer_id"],
        "hold_seconds": hold_seconds,
        "action": "hold" if hold_seconds > 0 else "release",
        "source": "mainline-window-normalizer",
    }
