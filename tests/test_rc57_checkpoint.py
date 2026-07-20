import hashlib

import pytest

from src.rc57_checkpoint import (
    CheckpointError,
    decode_checkpoint,
    encode_checkpoint,
    legacy_read_checkpoint,
)
from src.rc57_promotion import resume_checkpoint


def test_current_envelope_round_trip_with_rollback_tag():
    raw = encode_checkpoint("offset-17", 4, "blue")
    assert raw["schema"] == 1
    assert legacy_read_checkpoint(raw) == ("offset-17", "blue")
    assert decode_checkpoint(raw) == {
        "cursor": "offset-17",
        "generation": 4,
        "rollback_tag": "blue",
    }


def test_legacy_reader_still_reads_a_schema_one_fixture():
    assert legacy_read_checkpoint(
        {"schema": 1, "cursor": "offset-18", "rollback_tag": "green"}
    ) == ("offset-18", "green")


def test_resume_requires_generation_advance_and_keeps_route():
    raw = encode_checkpoint("offset-19", 4, "blue")
    with pytest.raises(CheckpointError):
        resume_checkpoint(raw, 4)
    resumed = resume_checkpoint(raw, 5)
    assert decode_checkpoint(resumed)["rollback_tag"] == "blue"


def test_resume_accepts_transitional_schema_two_checkpoint():
    persisted = {
        "schema": 2,
        "cursor": "offset-20",
        "generation": 4,
        "checksum": hashlib.sha256(b"offset-20:4").hexdigest()[:16],
        "rollback_tag": "green",
    }

    resumed = resume_checkpoint(persisted, 5)

    assert resumed["schema"] == 1
    assert legacy_read_checkpoint(resumed) == ("offset-20", "green")
    assert decode_checkpoint(resumed)["generation"] == 5
