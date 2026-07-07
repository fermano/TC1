"""Immutable release-checkpoint values and batch results."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Checkpoint:
    stream_id: str
    generation: int
    offset: int


@dataclass(frozen=True)
class CheckpointBatchResult:
    batch_id: str
    checkpoints: tuple[Checkpoint, ...]
