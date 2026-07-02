"""Queue expired partitions for asynchronous deletion."""

def queue_expired(partition: dict, delete_queue: list[str]) -> None:
    if not partition.get("expired"):
        return
    if partition.get("legal_hold"):
        return
    delete_queue.append(partition["id"])
