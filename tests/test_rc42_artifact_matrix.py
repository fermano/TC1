from src.release_artifact_selector import (
    clear_artifact_selection_cache,
    select_release_artifact,
)


CANDIDATES = [
    {"platform": "linux-amd64", "digest": "sha256:amd"},
    {"platform": "linux-arm64", "digest": "sha256:arm"},
    {"platform": "universal", "digest": "sha256:any"},
]


def test_rc42_runner_alias_selects_amd64_artifact():
    clear_artifact_selection_cache()
    selected = select_release_artifact("rc-42", "linux/x86_64", CANDIDATES)
    assert selected["digest"] == "sha256:amd"


def test_rc42_selects_distinct_artifacts_for_two_targets():
    clear_artifact_selection_cache()
    amd = select_release_artifact("rc-42", "linux-amd64", CANDIDATES)
    arm = select_release_artifact("rc-42", "linux-arm64", CANDIDATES)
    assert amd["digest"] == "sha256:amd"
    assert arm["digest"] == "sha256:arm"
