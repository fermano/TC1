MAX_DELIVERY_BATCH = 100


def validate_delivery_batch(records: list[dict]) -> list[dict]:
    if len(records) > MAX_DELIVERY_BATCH:
        raise ValueError(f"delivery batch exceeds {MAX_DELIVERY_BATCH} records")
    return records
