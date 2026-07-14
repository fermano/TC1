DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = " ".join((owner or "").split()).lower()
    return normalized or DEFAULT_OWNER


def filter_delivery_records(
    records: list[dict], owners: list[str | None] | None = None
) -> list[dict]:
    """Return records whose canonical owner is explicitly selected."""
    if owners is None:
        return list(records)

    selected_owners = {normalize_delivery_owner(owner) for owner in owners}
    return [
        record
        for record in records
        if normalize_delivery_owner(record.get("owner")) in selected_owners
    ]


def delivery_summary(record: dict, include_source: bool = False) -> dict:
    """Return the stable summary fields currently exposed to callers."""
    summary = {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
    source = (record.get("source") or "").strip()
    if include_source and source:
        summary["source"] = source
    return summary
