from src.artifact_signature_gate import can_promote_artifact


def test_rejects_unsigned_artifact():
    assert can_promote_artifact({"signature_verified": False}) is False


def test_allows_verified_artifact():
    assert can_promote_artifact({"signature_verified": True}) is True
