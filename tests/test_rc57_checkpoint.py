import pytest

from src.rc57_checkpoint import CheckpointError, decode_checkpoint, encode_checkpoint
from src.rc57_promotion import resume_checkpoint


def test_v2_round_trip():
    raw = encode_checkpoint("offset-17", 4)
    assert raw["schema"] == 2
    assert decode_checkpoint(raw) == {"cursor": "offset-17", "generation": 4}


def test_reads_schema_one_rows():
    assert decode_checkpoint({"schema": 1, "cursor": "offset-18"}) == {
        "cursor": "offset-18",
        "generation": 0,
    }


def test_resume_requires_generation_advance():
    raw = encode_checkpoint("offset-19", 4)
    with pytest.raises(CheckpointError):
        resume_checkpoint(raw, 4)
    assert decode_checkpoint(resume_checkpoint(raw, 5))["generation"] == 5
