DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = " ".join((owner or "").split()).lower()
    return normalized or DEFAULT_OWNER


def delivery_summary(record: dict) -> dict:
    """Return the stable summary fields currently exposed to callers."""
    return {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
