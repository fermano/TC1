_schema_cache = {}


def export_schema(workspace_id, workspace_version, fields):
    if workspace_id in _schema_cache:
        return _schema_cache[workspace_id]
    schema = tuple(fields)
    _schema_cache[workspace_id] = schema
    return schema


def clear_export_schema_cache():
    _schema_cache.clear()
