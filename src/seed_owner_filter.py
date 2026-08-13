"""Owner filtering used by delivery-summary previews."""


def filter_delivery_records(records, owners=None):
    """Return records for selected owners while preserving input order."""
    if owners is None:
        return list(records)

    selected = {str(owner).casefold() for owner in owners}
    return [
        record
        for record in records
        if str(record["owner"]).casefold() in selected
    ]
