SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def order_handoff_rows(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda row: (SEVERITY_ORDER.get(row.get("severity"), 9), row.get("owner", "")))
