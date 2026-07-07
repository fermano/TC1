import pytest

from src.release_artifact_selector import select_release_artifact


CANDIDATES = [
    {"platform": "linux-amd64", "digest": "sha256:amd"},
    {"platform": "linux-arm64", "digest": "sha256:arm"},
    {"platform": "universal", "digest": "sha256:any"},
]


def test_selects_exact_platform():
    assert select_release_artifact("rc-42", "linux-arm64", CANDIDATES)["digest"] == "sha256:arm"


def test_uses_universal_fallback():
    assert select_release_artifact("rc-42", "darwin-arm64", CANDIDATES)["digest"] == "sha256:any"


def test_raises_without_match_or_fallback():
    with pytest.raises(ValueError, match="no artifact"):
        select_release_artifact("rc-42", "darwin-arm64", CANDIDATES[:2])
