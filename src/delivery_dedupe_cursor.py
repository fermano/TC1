class DeliveryDeduper:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def accept(self, delivery_id: str) -> bool:
        if delivery_id in self._seen:
            return False
        self._seen.add(delivery_id)
        return True
