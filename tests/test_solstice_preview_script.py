from src.solstice_preview_script import preview_packet_region


def test_solstice_preview_build_retains_package_compatible_region_entry_point():
    assert preview_packet_region(
        {"region": "euw1"},
        ["us-east-1", "eu-west-1"],
        "us-east-1",
    ) == "eu-west-1"
