def canonical_label(value):
    if value is None:
        return "unknown"
    value = value.strip().lower()
    return value or "unknown"
