DEFAULT_WAIT_MINUTES = 30


def _coerce_minutes(value, default):
    if value:
        return int(value)
    return default


def build_candidate_row(payload, route_defaults):
    wait_minutes = _coerce_minutes(
        payload.get("defer_minutes"),
        route_defaults.get("default_defer_minutes", DEFAULT_WAIT_MINUTES),
    )
    return {
        "tenant": payload["tenant"],
        "invoice_id": payload["invoice_id"],
        "route": route_defaults["route"],
        "gate": "deferred" if wait_minutes else "ready",
        "wait_minutes": wait_minutes,
        "artifact_stage": route_defaults.get("artifact_stage", "rc101"),
        "route_signature": route_defaults.get("route_signature", "unset"),
    }
