class DeliveryDeduper:
    def __init__(self) -> None:
        self._seen: set[tuple[str | None, str]] = set()

    def accept(self, delivery_id: str, tenant_id: str | None = None) -> bool:
        key = self._key(delivery_id, tenant_id)
        if key in self._seen:
            return False
        self._seen.add(key)
        return True

    @staticmethod
    def _key(delivery_id: str, tenant_id: str | None) -> tuple[str | None, str]:
        if tenant_id is None:
            return (None, delivery_id)

        tenant_key = tenant_id.strip()
        if not tenant_key:
            raise ValueError("tenant_id must not be blank")
        return (tenant_key, delivery_id)
