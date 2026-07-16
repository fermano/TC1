"""Metric labels for delivery attempts."""


def delivery_attempt_labels(record):
    return {
        "queue": record["queue"],
        "outcome": record["outcome"],
        "delivery_id": record["delivery_id"],
    }
