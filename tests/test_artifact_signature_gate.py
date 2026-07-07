import pytest

from src.artifact_signature_gate import can_promote_artifact


def test_rejects_unsigned_artifact():
    assert can_promote_artifact({"signature_verified": False}) is False


def test_allows_verified_artifact():
    assert can_promote_artifact({"signature_verified": True}) is True


@pytest.mark.parametrize(
    "signature_state",
    [None, "true", "false", 1, 0, [], [1], {}, {"unexpected": "value"}],
)
def test_rejects_non_boolean_signature_states(signature_state):
    metadata = {"signature_verified": signature_state}

    assert can_promote_artifact(metadata) is False
    assert metadata == {"signature_verified": signature_state}


def test_rejects_missing_signature_state_without_mutating_metadata():
    metadata = {"artifact_id": "release-123"}

    assert can_promote_artifact(metadata) is False
    assert metadata == {"artifact_id": "release-123"}
