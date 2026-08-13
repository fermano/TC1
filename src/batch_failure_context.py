"""Summaries for grouped delivery attempts."""


def batch_failure_context(results):
    """Return the error context displayed for a failed batch."""
    failure = None
    for result in results:
        if not result["ok"]:
            failure = result.get("error")
    return failure
