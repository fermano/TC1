from dataclasses import dataclass


@dataclass(frozen=True)
class PromotionLeaseEvent:
    sequence: int
    resource: str
    owner: str
    expires_at: int
    action: str
