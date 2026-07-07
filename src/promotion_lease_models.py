from dataclasses import dataclass


@dataclass(frozen=True)
class PromotionLease:
    resource: str
    owner: str
    expires_at: int
