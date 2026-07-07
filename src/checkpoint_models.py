"""Persisted release-stream checkpoint values."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Checkpoint:
    stream_id: str
    generation: int
    offset: int
