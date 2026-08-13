"""Operator card helpers for ownerless retry batches."""


def owner_display(batch):
    owner = batch.get("owner") or batch.get("team_owner")
    if owner:
        return str(owner)
    if batch.get("region_alias"):
        return f"unowned:{batch['region_alias']}"
    return "unowned"
