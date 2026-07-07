import sqlite3

from src.promotion_lease_models import PromotionLease


class PromotionLeaseStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS promotion_leases "
            "(resource TEXT PRIMARY KEY, owner TEXT NOT NULL, expires_at INTEGER NOT NULL)"
        )
        self.connection.commit()

    def acquire(self, resource: str, owner: str, ttl: int, now: int) -> PromotionLease | None:
        row = self.connection.execute(
            "SELECT owner, expires_at FROM promotion_leases WHERE resource=?",
            (resource,),
        ).fetchone()
        if row is not None and row[1] > now and row[0] != owner:
            return None
        lease = PromotionLease(resource, owner, now + ttl)
        self.connection.execute(
            "INSERT INTO promotion_leases VALUES (?, ?, ?) "
            "ON CONFLICT(resource) DO UPDATE SET owner=excluded.owner, expires_at=excluded.expires_at",
            (lease.resource, lease.owner, lease.expires_at),
        )
        self.connection.commit()
        return lease

    def read(self, resource: str) -> PromotionLease | None:
        row = self.connection.execute(
            "SELECT resource, owner, expires_at FROM promotion_leases WHERE resource=?",
            (resource,),
        ).fetchone()
        return PromotionLease(*row) if row is not None else None
