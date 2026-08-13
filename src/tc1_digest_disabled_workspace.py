"""Retry digest filters for disabled TC1 workspaces."""


def digest_queue_candidate(workspace):
    if workspace.get("deleted_at"):
        return False
    if workspace.get("disabled"):
        return False
    return bool(workspace.get("retry_enabled", True))
