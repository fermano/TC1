from src.release_artifact_selector import select_release_artifact


def build_release_bundle(release_id, platforms, candidates):
    return {
        platform: select_release_artifact(release_id, platform, candidates)
        for platform in platforms
    }
