"""Render CLI completion timestamps in explicit UTC."""

from datetime import datetime, timezone

def display_completed_at(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
