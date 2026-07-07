import sqlite3

from src.promotion_lease_models import PromotionLease


class PromotionLeaseStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS promotion_fences "
                "(resource TEXT PRIMARY KEY, owner TEXT NOT NULL, "
                "fence INTEGER NOT NULL, expires_at INTEGER NOT NULL)"
            )
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS promotion_leases "
                "(resource TEXT PRIMARY KEY, owner TEXT NOT NULL, "
                "expires_at INTEGER NOT NULL)"
            )
            self.connection.execute(
                "INSERT INTO promotion_leases(resource, owner, expires_at) "
                "SELECT resource, owner, expires_at FROM promotion_fences WHERE 1 "
                "ON CONFLICT(resource) DO UPDATE SET owner=excluded.owner, "
                "expires_at=excluded.expires_at"
            )
            self.connection.commit()
        except BaseException:
            self.connection.rollback()
            raise

    def acquire(
        self, resource: str, owner: str, ttl: int, now: int | None = None
    ) -> PromotionLease | None:
        # Package 5.1 callers still pass their observed time. Keep the argument
        # for compatibility, but never use a worker clock as the lease boundary.
        del now
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            database_now = self.connection.execute("SELECT unixepoch()").fetchone()[0]
            row = self.connection.execute(
                "SELECT owner, fence, expires_at FROM promotion_fences WHERE resource=?",
                (resource,),
            ).fetchone()
            if row is not None and row[2] > database_now and row[0] != owner:
                self.connection.commit()
                return None
            fence = 1 if row is None else row[1] + 1
            lease = PromotionLease(resource, owner, fence, database_now + ttl)
            self.connection.execute(
                "INSERT INTO promotion_fences VALUES (?, ?, ?, ?) "
                "ON CONFLICT(resource) DO UPDATE SET owner=excluded.owner, "
                "fence=excluded.fence, expires_at=excluded.expires_at",
                (lease.resource, lease.owner, lease.fence, lease.expires_at),
            )
            self.connection.execute(
                "INSERT INTO promotion_leases VALUES (?, ?, ?) "
                "ON CONFLICT(resource) DO UPDATE SET owner=excluded.owner, "
                "expires_at=excluded.expires_at",
                (lease.resource, lease.owner, lease.expires_at),
            )
            self.connection.commit()
            return lease
        except BaseException:
            self.connection.rollback()
            raise

    def can_publish(
        self, resource: str, owner: str, fence: int, now: int | None = None
    ) -> bool:
        # This check belongs at callback acceptance time, including after a
        # queued callback resumes. The database evaluates ownership and expiry
        # together so a corrected worker clock cannot revive a stale fence.
        del now
        row = self.connection.execute(
            "SELECT EXISTS(SELECT 1 FROM promotion_fences "
            "WHERE resource=? AND owner=? AND fence=? AND expires_at > unixepoch())",
            (resource, owner, fence),
        ).fetchone()
        return row[0] == 1

    def read(self, resource: str) -> PromotionLease | None:
        row = self.connection.execute(
            "SELECT resource, owner, fence, expires_at FROM promotion_fences WHERE resource=?",
            (resource,),
        ).fetchone()
        return PromotionLease(*row) if row is not None else None
