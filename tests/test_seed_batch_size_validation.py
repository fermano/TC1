import pytest

from src.seed_batch_size_validation import validate_batch_size


@pytest.mark.parametrize("value", [0, -1, 101])
def test_rejects_values_outside_allowed_range(value):
    with pytest.raises(ValueError):
        validate_batch_size(value, 100)


def test_accepts_minimum_and_maximum():
    assert validate_batch_size(1, 100) == 1
    assert validate_batch_size(100, 100) == 100


def test_rejects_boolean_and_non_integer_values():
    with pytest.raises(TypeError):
        validate_batch_size(True, 100)
    with pytest.raises(TypeError):
        validate_batch_size("10", 100)
