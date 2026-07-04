"""Normalize release approval timestamps before persistence."""

from datetime import datetime, timezone

def normalize_approval_time(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
