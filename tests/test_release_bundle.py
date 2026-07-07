from src.release_artifact_selector import clear_artifact_selection_cache
from src.release_bundle import build_release_bundle


def test_builds_release_bundle_for_requested_platform():
    clear_artifact_selection_cache()
    candidates = [
        {"platform": "linux-amd64", "digest": "sha256:amd"},
        {"platform": "universal", "digest": "sha256:any"},
    ]

    assert build_release_bundle("rc-42", ["linux-amd64"], candidates) == {
        "linux-amd64": {"platform": "linux-amd64", "digest": "sha256:amd"}
    }
