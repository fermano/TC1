"""Helpers for preparing TC1 admin export bundles."""

REDACTION = "[redacted]"
SENSITIVE_FRAGMENTS = {"password", "token", "secret", "api_key", "private_key"}


def _normalize_key(key):
    return str(key or "").strip().lower().replace("-", "_").replace(" ", "_")


def _is_sensitive_key(key):
    normalized = _normalize_key(key)
    return any(fragment in normalized for fragment in SENSITIVE_FRAGMENTS)


def _sanitize_value(value):
    if isinstance(value, dict):
        sanitized = {}
        for key, child in value.items():
            sanitized[key] = REDACTION if _is_sensitive_key(key) else _sanitize_value(child)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    return value


def sanitize_export(payload):
    """Return a sanitized copy of an admin export payload."""
    return _sanitize_value(payload)


def summarize_export(payload):
    """Return a compact, sanitized summary used by Slack/email diagnostics."""
    sanitized = sanitize_export(payload)
    return {
        "tenant_id": sanitized.get("tenant_id"),
        "workspace_id": sanitized.get("workspace_id"),
        "connector_count": len(sanitized.get("connectors") or []),
        "sanitized": sanitized,
    }
