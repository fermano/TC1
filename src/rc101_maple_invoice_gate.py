DEFAULT_WAIT_MINUTES = 30


def _pick_wait(payload):
    # A present partner field wins, including zero and empty/default values.
    if "deferMinutes" in payload:
        return payload["deferMinutes"]
    return payload.get("defer_minutes")


def _coerce_minutes(value, default):
    if value is None or value == "":
        return default
    return int(value)


def build_candidate_row(payload, route_defaults):
    wait_minutes = _coerce_minutes(
        _pick_wait(payload),
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
        "release_channel": route_defaults.get("release_channel", "candidate"),
    }
