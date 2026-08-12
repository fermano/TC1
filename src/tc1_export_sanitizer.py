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


def _sanitize_in_place(value):
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if _is_sensitive_key(key):
                value[key] = REDACTION
            else:
                _sanitize_in_place(child)
        return value
    if isinstance(value, list):
        for item in value:
            _sanitize_in_place(item)
    return value


def sanitize_export(payload):
    """Sanitize an admin export payload for preview display."""
    return _sanitize_in_place(payload)


def summarize_export(payload):
    """Return a compact, sanitized summary used by Slack/email diagnostics."""
    sanitized = sanitize_export(payload)
    return {
        "tenant_id": sanitized.get("tenant_id"),
        "workspace_id": sanitized.get("workspace_id"),
        "connector_count": len(sanitized.get("connectors") or []),
        "sanitized": sanitized,
    }
