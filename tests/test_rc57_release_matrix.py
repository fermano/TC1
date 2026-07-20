import os

import pytest

from src.rc57_checkpoint import CheckpointError, decode_checkpoint, legacy_read_checkpoint
from src.rc57_promotion import resume_checkpoint


pytestmark = pytest.mark.skipif(
    os.getenv("RC57_MATRIX") != "1",
    reason="release compatibility matrix",
)


def test_promotes_a_persisted_release_row_without_breaking_rollback():
    persisted = {
        "schema": 1,
        "cursor": "offset-301",
        "rollback_tag": "blue",
    }

    resumed = resume_checkpoint(persisted, 1)

    assert resumed["schema"] == 1
    assert legacy_read_checkpoint(resumed) == ("offset-301", "blue")
    assert decode_checkpoint(resumed) == {
        "cursor": "offset-301",
        "generation": 1,
        "rollback_tag": "blue",
    }


def test_generation_survives_a_second_process_resume():
    persisted = resume_checkpoint(
        {"schema": 1, "cursor": "offset-302", "rollback_tag": "green"},
        7,
    )

    with pytest.raises(CheckpointError):
        resume_checkpoint(dict(persisted), 7)

    advanced = resume_checkpoint(dict(persisted), 8)
    assert decode_checkpoint(advanced)["generation"] == 8


def test_checksum_covers_release_routing_data_when_present():
    persisted = resume_checkpoint(
        {"schema": 1, "cursor": "offset-303", "rollback_tag": "blue"},
        2,
    )
    tampered = dict(persisted)
    tampered["rollback_tag"] = "green"

    with pytest.raises(CheckpointError):
        decode_checkpoint(tampered)
