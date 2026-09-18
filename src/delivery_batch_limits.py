MAX_DELIVERY_BATCH = 100
PARTNER_RETRY_BATCH = 40


def validate_delivery_batch(
    records: list[dict],
    queue: str | None = None,
) -> list[dict]:
    limit = PARTNER_RETRY_BATCH if queue == "partner-retry" else MAX_DELIVERY_BATCH
    if len(records) > limit:
        raise ValueError(f"delivery batch exceeds {limit} records")
    return records
