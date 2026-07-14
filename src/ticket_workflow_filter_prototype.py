from src.ticket_workflow_seed import normalize_delivery_owner


def filter_delivery_records(records: list[dict], owners: list[str] | None) -> list[dict]:
    if owners is None:
        return list(records)
    selected = {normalize_delivery_owner(owner) for owner in owners}
    matching = [record for record in records if normalize_delivery_owner(record.get("owner")) in selected]
    return sorted(matching, key=lambda record: normalize_delivery_owner(record.get("owner")))
