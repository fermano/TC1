"""Promotion behavior before generation-aware resume was introduced."""

from __future__ import annotations

from .rc57_checkpoint import decode_checkpoint, encode_checkpoint


def resume_checkpoint(raw: dict[str, object]) -> dict[str, object]:
    state = decode_checkpoint(raw)
    return encode_checkpoint(str(state["cursor"]))
