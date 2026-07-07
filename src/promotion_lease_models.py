from dataclasses import dataclass


@dataclass(frozen=True)
class PromotionLease:
    resource: str
    owner: str
    fence: int
    expires_at: int
