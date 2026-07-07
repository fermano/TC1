def can_promote_artifact(metadata):
    return metadata.get("signature_verified") is True
