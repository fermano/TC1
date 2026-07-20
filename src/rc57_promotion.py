"""RC-57 rollback-first promotion behavior."""

from __future__ import annotations

from .rc57_checkpoint import decode_checkpoint, encode_checkpoint


def resume_checkpoint(raw: dict[str, object], generation: int) -> dict[str, object]:
    state = decode_checkpoint(raw)
    return encode_checkpoint(
        str(state["cursor"]),
        state.get("rollback_tag") if isinstance(state.get("rollback_tag"), str) else None,
    )
