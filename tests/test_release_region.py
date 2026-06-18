from src.release_region import normalize_release_region


def test_normalizes_supported_aliases():
    assert normalize_release_region(" USE1 ") == "us-east-1"
    assert normalize_release_region("eu-west") == "eu-west-1"
