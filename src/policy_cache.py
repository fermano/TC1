from collections.abc import Callable


class PolicySnapshotCache:
    def __init__(self) -> None:
        self._entries: dict[tuple[str, int], dict[str, object]] = {}

    def get_or_load(
        self,
        workspace_id: str,
        version: int,
        loader: Callable[[], dict[str, object]],
    ) -> dict[str, object]:
        key = (workspace_id, version)
        if key not in self._entries:
            self._entries[key] = loader()
        return self._entries[key]
