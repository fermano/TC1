from datetime import datetime, timezone


def normalize_escalation_deadline(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("deadline must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
