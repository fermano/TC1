def can_promote_artifact(metadata):
    return bool(metadata.get("signature_verified"))
