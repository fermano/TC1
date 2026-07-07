from __future__ import annotations

from collections.abc import Iterable, Mapping


def normalize_owner(value: object) -> str | None:
    owner = str(value or "").strip()
    return owner or None


def named_owners(rows: Iterable[Mapping[str, object]]) -> list[str]:
    owners: list[str] = []
    for row in rows:
        owner = normalize_owner(row.get("owner"))
        if owner is not None:
            owners.append(owner)
    return owners
