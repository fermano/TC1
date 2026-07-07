_schema_cache = {}


def export_schema(workspace_id, workspace_version, fields):
    cache_key = (workspace_id, workspace_version)
    if cache_key in _schema_cache:
        return _schema_cache[cache_key]
    schema = tuple(fields)
    _schema_cache[cache_key] = schema
    return schema


def clear_export_schema_cache():
    _schema_cache.clear()
