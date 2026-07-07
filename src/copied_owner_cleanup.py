from __future__ import annotations

from collections.abc import Iterable, Mapping


def remove_blank_owner_rows(rows: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    return [row for row in rows if str(row.get("owner") or "").strip()]
