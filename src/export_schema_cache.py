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
        observed_fields = tuple(fields)
        current = self._current.get(workspace_id)
        if (
            current is not None
            and current.workspace_version == workspace_version
            and current.fields == observed_fields
        ):
            return current

        snapshot = SchemaSnapshot(workspace_id, workspace_version, observed_fields)
        self._current[workspace_id] = snapshot
        return snapshot

    def clear(self) -> None:
        self._current.clear()


export_schema_cache = ExportSchemaCache()


def export_schema(
    workspace_id: str,
    workspace_version: int,
    fields: Iterable[str],
) -> tuple[str, ...]:
    """Return current schema fields for legacy scheduler integrations."""

    return export_schema_cache.snapshot(workspace_id, workspace_version, fields).fields


def clear_export_schema_cache() -> None:
    export_schema_cache.clear()
