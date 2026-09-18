class DeliveryDeduper:
    def __init__(self) -> None:
        self._seen: set[tuple[str | None, str]] = set()

    def accept(self, delivery_id: str, tenant_id: str | None = None) -> bool:
        key = (tenant_id, delivery_id)
        if key in self._seen:
            return False
        self._seen.add(key)
        return True
