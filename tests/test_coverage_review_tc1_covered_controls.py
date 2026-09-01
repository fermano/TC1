import pytest
from src.coverage_review_tc1_covered_controls import route_mode

@pytest.mark.parametrize(("value", "expected"), [(None, "default"), ("manual", "manual"), ("scheduled", "automatic")])
def test_route_mode_covers_public_contract(value, expected):
    assert route_mode(value) == expected
