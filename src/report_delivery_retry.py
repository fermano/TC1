from __future__ import annotations


def retry_delay(status: int, retry_after: int | None, attempt: int) -> int:
    if status not in {429, 502, 503}:
        return 0
    if status in {429, 503} and retry_after is not None:
        return retry_after
    return min(2 ** attempt, 30)
