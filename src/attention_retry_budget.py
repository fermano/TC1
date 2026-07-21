def resolve_attention_retry_budget(requested: int | None, default: int = 3) -> int:
    """Resolve an explicit retry budget without treating zero as missing."""
    if requested is None:
        return default
    if requested < 0:
        raise ValueError("retry budget cannot be negative")
    return requested
