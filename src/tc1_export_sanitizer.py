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


def sanitize_export(payload):
    """Return a sanitized top-level copy of an admin export payload."""
    if not isinstance(payload, dict):
        return payload

    sanitized = dict(payload)
    for key in list(sanitized):
        if _is_sensitive_key(key):
            sanitized[key] = REDACTION
    return sanitized


def summarize_export(payload):
    """Return a compact, sanitized summary used by Slack/email diagnostics."""
    sanitized = sanitize_export(payload)
    return {
        "tenant_id": sanitized.get("tenant_id"),
        "workspace_id": sanitized.get("workspace_id"),
        "connector_count": len(sanitized.get("connectors") or []),
        "sanitized": sanitized,
    }
