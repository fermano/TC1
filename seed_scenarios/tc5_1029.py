"""Non-production prototype for a columnar audit archive."""

def estimated_ratio(rows: int) -> float:
    return 0.0 if rows == 0 else 0.42
