import sqlite3

from src.promotion_lease_models import PromotionLease


class PromotionLeaseStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS promotion_fences "
            "(resource TEXT PRIMARY KEY, owner TEXT NOT NULL, "
            "fence INTEGER NOT NULL, expires_at INTEGER NOT NULL)"
        )
        self.connection.commit()

    def acquire(self, resource: str, owner: str, ttl: int, now: int) -> PromotionLease | None:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            row = self.connection.execute(
                "SELECT owner, fence, expires_at FROM promotion_fences WHERE resource=?",
                (resource,),
            ).fetchone()
            if row is not None and row[2] > now and row[0] != owner:
                self.connection.commit()
                return None
            fence = 1 if row is None else row[1] + 1
            lease = PromotionLease(resource, owner, fence, now + ttl)
            self.connection.execute(
                "INSERT INTO promotion_fences VALUES (?, ?, ?, ?) "
                "ON CONFLICT(resource) DO UPDATE SET owner=excluded.owner, "
                "fence=excluded.fence, expires_at=excluded.expires_at",
                (lease.resource, lease.owner, lease.fence, lease.expires_at),
            )
            self.connection.commit()
            return lease
        except BaseException:
            self.connection.rollback()
            raise

    def can_publish(self, resource: str, owner: str, fence: int, now: int) -> bool:
        row = self.connection.execute(
            "SELECT owner, fence, expires_at FROM promotion_fences WHERE resource=?",
            (resource,),
        ).fetchone()
        return row == (owner, fence, row[2]) and row[2] > now if row is not None else False

    def read(self, resource: str) -> PromotionLease | None:
        row = self.connection.execute(
            "SELECT resource, owner, fence, expires_at FROM promotion_fences WHERE resource=?",
            (resource,),
        ).fetchone()
        return PromotionLease(*row) if row is not None else None
