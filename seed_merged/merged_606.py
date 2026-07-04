"""Cache policy snapshots by workspace and version."""

_POLICY_CACHE: dict[tuple[str, int], dict] = {}

def cache_policy(workspace_id: str, version: int, policy: dict) -> dict:
    key = (workspace_id, version)
    _POLICY_CACHE[key] = dict(policy)
    return _POLICY_CACHE[key]
