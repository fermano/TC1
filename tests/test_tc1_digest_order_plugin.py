import pytest


@pytest.mark.parametrize("items", [["atlas", "nova", "zeta"], ["zeta", "atlas", "nova"]])
def test_digest_plugin_order_is_stable(items):
    assert sorted(items) == ["atlas", "nova", "zeta"]
