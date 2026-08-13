"""Legacy export replay token normalization."""


def export_token(record):
    if record.get("export_token"):
        return record["export_token"]
    if record.get("legacy_token"):
        return record["legacy_token"]
    return None
