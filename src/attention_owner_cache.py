_owner_cache: dict[str, str] = {}


def normalized_owner(owner: str) -> str:
    key = " ".join(owner.strip().lower().split())
    if key not in _owner_cache:
        _owner_cache[key] = key
    return _owner_cache[key]


def clear_owner_cache() -> None:
    _owner_cache.clear()
