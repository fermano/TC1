"""Replay candidate selector used by digest backfill."""


def replay_candidate(workspace):
    if workspace.get("deleted_at"):
        return False
    return bool(workspace.get("retry_enabled", True))
