"""Initial CLI status timestamp formatter."""

def display_completed_at(value: str) -> str:
    return value.replace("+00:00", "")
