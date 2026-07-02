"""Persist a replay cursor before dispatch."""

def prepare_replay(cursor_store: dict, stream: str, cursor: str) -> dict:
    cursor_store[stream] = cursor
    return {"stream": stream, "cursor": cursor, "status": "ready"}
