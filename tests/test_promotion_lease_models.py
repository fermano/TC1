from dataclasses import FrozenInstanceError

import pytest

from src.promotion_lease_models import PromotionLease


def test_promotion_lease_is_immutable():
    lease = PromotionLease("rc-17", "worker-a", 1, 130)

    with pytest.raises(FrozenInstanceError):
        lease.fence = 2
