from src.solstice_preview_script import preview_packet_region


def test_solstice_preview_build_retains_package_compatible_region_entry_point():
    assert preview_packet_region(
        {"region": "euw1"},
        ["us-east-1", "eu-west-1"],
        "us-east-1",
    ) == "eu-west-1"


def test_solstice_preview_build_uses_hint_when_current_region_is_blank():
    assert preview_packet_region(
        {"region": " ", "region_hint": " EUW1 "},
        ["us-east-1", "eu-west-1"],
        "us-east-1",
    ) == "eu-west-1"


def test_solstice_preview_build_keeps_current_region_ahead_of_stale_hint():
    assert preview_packet_region(
        {"region": "USE1", "region_hint": "euw1"},
        ["us-east-1", "eu-west-1"],
        "eu-west-1",
    ) == "us-east-1"
