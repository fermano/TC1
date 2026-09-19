MAX_DELIVERY_BATCH = 100
PARTNER_RETRY_BATCH = 40
PARTNER_RETRY_QUEUE = "partner-retry"
GENERAL_DELIVERY_QUEUES = {"billing-ops", "engineering-ops", "partner-import", "release-ops"}


def validate_delivery_batch(records: list[dict], queue: str | None = None) -> list[dict]:
    limit = _limit_for_queue(queue)
    if len(records) > limit:
        raise ValueError(f"delivery batch exceeds {limit} records")
    return records


def _limit_for_queue(queue: str | None) -> int:
    if queue is None:
        return MAX_DELIVERY_BATCH

    queue_name = queue.strip().lower().replace("_", "-")
    if not queue_name:
        raise ValueError("delivery queue must not be blank")
    if queue_name == PARTNER_RETRY_QUEUE:
        return PARTNER_RETRY_BATCH
    if queue_name in GENERAL_DELIVERY_QUEUES:
        return MAX_DELIVERY_BATCH
    raise ValueError(f"unknown delivery queue: {queue}")
