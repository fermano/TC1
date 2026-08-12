"""Helpers for preparing TC1 admin export bundles."""

REDACTION = "[redacted]"
SENSITIVE_KEYS = {
    "api_key",
    "access_token",
    "refresh_token",
    "client_secret",
    "signing_secret",
    "password",
    "private_key",
}


def _normalize_key(key):
    return str(key or "").strip().lower().replace("-", "_").replace(" ", "_")


def _is_sensitive_key(key):
    return _normalize_key(key) in SENSITIVE_KEYS


def _sanitize_value(value):
    if isinstance(value, dict):
        return {
            key: REDACTION if _is_sensitive_key(key) else _sanitize_value(child)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    return value


def sanitize_export(payload):
    """Return a sanitized copy of an admin export payload.

    The sanitizer is used for support/admin bundle previews before data leaves TC1.
    It intentionally avoids changing the source payload object because preview and
    audit views may be rendered from the same parsed export.
    """
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
