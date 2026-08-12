"""Owner identity normalization used by delivery grouping."""


def canonical_owner(value: str) -> str:
    """Normalize common copied-label differences without changing display data."""
    return " ".join(value.strip().split()).casefold()
