from src.webhook_replay_batches import replay_batches


def test_no_batch_exceeds_workspace_limit():
    batches = replay_batches(list(range(7)), 3)
    assert [len(batch) for batch in batches] == [3, 3, 1]
