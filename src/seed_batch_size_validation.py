"""Batch-size validation for delivery enqueue operations."""


def validate_batch_size(value: int, maximum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("batch size must be an integer")
    if value < 1 or value > maximum:
        raise ValueError(f"batch size must be between 1 and {maximum}")
    return value
