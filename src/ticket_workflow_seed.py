DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = " ".join((owner or "").split()).lower()
    return normalized or DEFAULT_OWNER


def filter_delivery_records(records: list[dict], owners: list[str | None] | None = None) -> list[dict]:
    """Filter records by canonical owner while preserving record order."""
    if owners is None:
        return records
    selected = {normalize_delivery_owner(owner) for owner in owners}
    return [
        record
        for record in records
        if normalize_delivery_owner(record.get("owner")) in selected
    ]


def delivery_summary(record: dict, include_source: bool = False) -> dict:
    """Return stable summary fields with optional source metadata."""
    summary = {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
    if include_source:
        source = (record.get("source") or "").strip()
        if source:
            summary["source"] = source
    return summary
