from src.release_artifact_selector import select_release_artifact


def test_revert_selects_each_target_independently():
    candidates = [
        {"platform": "linux-amd64", "digest": "sha256:amd"},
        {"platform": "linux-arm64", "digest": "sha256:arm"},
    ]
    assert select_release_artifact("rc-42", "linux-amd64", candidates)["digest"] == "sha256:amd"
    assert select_release_artifact("rc-42", "linux-arm64", candidates)["digest"] == "sha256:arm"
