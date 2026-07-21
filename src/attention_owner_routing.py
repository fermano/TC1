DEFAULT_QUEUE = "engineering-ops"


def route_owner(owner: str | None) -> str:
    normalized = " ".join((owner or "").strip().lower().split())
    return normalized or DEFAULT_QUEUE
