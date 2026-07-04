"""Emit a completion watermark for newly generated audit exports."""

def completion_watermark(export_id: str, sequence: int) -> dict:
    return {"export_id": export_id, "watermark": sequence, "version": 1}
