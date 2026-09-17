"""Earlier Alder intake prototype; retained as implementation history only."""

def alder_gate(payload, default_wait=240):
    raw = payload.get("ready_after")
    wait_seconds = default_wait if raw in (None, "") else int(raw)
    return {
        "decision": "release" if wait_seconds == 0 else "wait",
        "wait_seconds": wait_seconds,
    }
