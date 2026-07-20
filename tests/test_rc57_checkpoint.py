from src.rc57_checkpoint import decode_checkpoint, encode_checkpoint, legacy_read_checkpoint
from src.rc57_promotion import resume_checkpoint


def test_legacy_format_keeps_release_route():
    raw = encode_checkpoint("offset-17", "blue")
    assert legacy_read_checkpoint(raw) == ("offset-17", "blue")
    assert decode_checkpoint(raw)["rollback_tag"] == "blue"


def test_resume_keeps_cursor_and_route():
    raw = resume_checkpoint(
        {"schema": 1, "cursor": "offset-18", "rollback_tag": "green"},
        5,
    )
    assert legacy_read_checkpoint(raw) == ("offset-18", "green")
