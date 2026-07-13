_owner_cache: dict[str, str] = {}


def normalized_owner(owner: str) -> str:
    if owner not in _owner_cache:
        _owner_cache[owner] = " ".join(owner.strip().lower().split())
    return _owner_cache[owner]
