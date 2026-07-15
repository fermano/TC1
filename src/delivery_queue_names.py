CANONICAL_QUEUES = {"engineering-ops", "billing-ops", "release-ops"}


def canonical_delivery_queue(queue: str) -> str:
    normalized = queue.strip().lower()
    if normalized not in CANONICAL_QUEUES:
        raise ValueError(f"unknown delivery queue: {queue}")
    return normalized
