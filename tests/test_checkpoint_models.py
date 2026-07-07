from dataclasses import FrozenInstanceError

import pytest

from src.checkpoint_models import Checkpoint, CheckpointBatchResult


def test_checkpoint_and_result_are_immutable():
    checkpoint = Checkpoint("billing", 4, 91)
    result = CheckpointBatchResult("batch-1", (checkpoint,))

    with pytest.raises(FrozenInstanceError):
        checkpoint.offset = 92
    with pytest.raises(FrozenInstanceError):
        result.batch_id = "batch-2"
