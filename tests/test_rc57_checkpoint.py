import pytest

from src.rc57_checkpoint import (
    CheckpointError,
    decode_checkpoint,
    encode_checkpoint,
    legacy_read_checkpoint,
)
from src.rc57_promotion import resume_checkpoint


def test_schema_one_round_trip_with_rollback_tag():
    raw = encode_checkpoint("offset-17", "blue")
    assert decode_checkpoint(raw)["rollback_tag"] == "blue"
    assert legacy_read_checkpoint(raw) == ("offset-17", "blue")


def test_resume_preserves_cursor():
    assert resume_checkpoint({"schema": 1, "cursor": "offset-18"})["cursor"] == "offset-18"


def test_rejects_unknown_schema():
    with pytest.raises(CheckpointError):
        decode_checkpoint({"schema": 9, "cursor": "offset-19"})
