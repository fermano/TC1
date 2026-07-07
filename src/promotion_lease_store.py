import sqlite3

from src.promotion_lease_models import PromotionLeaseEvent


class PromotionLeaseJournal:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def initialize(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS promotion_lease_events "
            "(sequence INTEGER PRIMARY KEY AUTOINCREMENT, resource TEXT NOT NULL, "
            "owner TEXT NOT NULL, expires_at INTEGER NOT NULL, action TEXT NOT NULL)"
        )
        self.connection.commit()

    def acquire(self, resource: str, owner: str, ttl: int, now: int) -> PromotionLeaseEvent | None:
        current = self.current(resource)
        if current is not None and current.action == "acquire" and current.expires_at > now:
            return None
        cursor = self.connection.execute(
            "INSERT INTO promotion_lease_events(resource, owner, expires_at, action) "
            "VALUES (?, ?, ?, 'acquire')",
            (resource, owner, now + ttl),
        )
        self.connection.commit()
        return PromotionLeaseEvent(cursor.lastrowid, resource, owner, now + ttl, "acquire")

    def release(self, resource: str, owner: str, now: int) -> PromotionLeaseEvent:
        cursor = self.connection.execute(
            "INSERT INTO promotion_lease_events(resource, owner, expires_at, action) "
            "VALUES (?, ?, ?, 'release')",
            (resource, owner, now),
        )
        self.connection.commit()
        return PromotionLeaseEvent(cursor.lastrowid, resource, owner, now, "release")

    def current(self, resource: str) -> PromotionLeaseEvent | None:
        row = self.connection.execute(
            "SELECT sequence, resource, owner, expires_at, action "
            "FROM promotion_lease_events WHERE resource=? ORDER BY sequence DESC LIMIT 1",
            (resource,),
        ).fetchone()
        return PromotionLeaseEvent(*row) if row is not None else None
