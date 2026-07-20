"""Generation-aware promotion behavior on main."""

from __future__ import annotations

from .rc57_checkpoint import CheckpointError, decode_checkpoint, encode_checkpoint


def resume_checkpoint(raw: dict[str, object], generation: int) -> dict[str, object]:
    state = decode_checkpoint(raw)
    if generation <= int(state["generation"]):
        raise CheckpointError("generation must advance")
    return encode_checkpoint(str(state["cursor"]), generation)
