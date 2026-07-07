import pytest

from src.release_artifact_selector import (
    clear_artifact_selection_cache,
    select_release_artifact,
)


CANDIDATES = [
    {"platform": "linux-amd64", "digest": "sha256:amd"},
    {"platform": "linux-arm64", "digest": "sha256:arm"},
    {"platform": "universal", "digest": "sha256:any"},
]


def setup_function():
    clear_artifact_selection_cache()


def test_selects_exact_platform():
    assert select_release_artifact("rc-42", "linux-arm64", CANDIDATES)["digest"] == "sha256:arm"


def test_reuses_selection_for_same_release():
    first = select_release_artifact("rc-42", "linux-arm64", CANDIDATES)
    second = select_release_artifact("rc-42", "linux-arm64", list(CANDIDATES))
    assert second is first


def test_uses_universal_fallback():
    assert select_release_artifact("rc-42", "darwin-arm64", CANDIDATES)["digest"] == "sha256:any"


def test_raises_without_match_or_fallback():
    with pytest.raises(ValueError, match="no artifact"):
        select_release_artifact("rc-42", "darwin-arm64", CANDIDATES[:2])
