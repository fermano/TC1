"""Current export-schema snapshots per workspace."""

from __future__ import annotations

from collections.abc import Iterable

from src.export_schema_models import SchemaSnapshot


class ExportSchemaCache:
    def __init__(self) -> None:
        self._current: dict[str, SchemaSnapshot] = {}

    def snapshot(
        self,
        workspace_id: str,
        workspace_version: int,
        fields: Iterable[str],
    ) -> SchemaSnapshot:
        current = self._current.get(workspace_id)
        if current is not None and current.workspace_version == workspace_version:
            return current

        snapshot = SchemaSnapshot(workspace_id, workspace_version, tuple(fields))
        self._current[workspace_id] = snapshot
        return snapshot

    def clear(self) -> None:
        self._current.clear()


export_schema_cache = ExportSchemaCache()


def clear_export_schema_cache() -> None:
    export_schema_cache.clear()
