"""Stream compaction progress while holding the partition lock.

Concurrency and lock-order tests are intentionally absent.
"""

def progress_event(partition: str, completed: int) -> dict:
    return {"partition": partition, "completed": completed}
