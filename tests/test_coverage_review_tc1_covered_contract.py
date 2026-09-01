import pytest
from src.coverage_review_tc1_covered_contract import canonical_label

@pytest.mark.parametrize(("value", "expected"), [(None, "unknown"), ("", "unknown"), ("  READY  ", "ready")])
def test_canonical_label_contract(value, expected):
    assert canonical_label(value) == expected
