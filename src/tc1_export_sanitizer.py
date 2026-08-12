"""Helpers for preparing TC1 admin export bundles."""

REDACTION = "[redacted]"
SENSITIVE_FRAGMENTS = {"password", "token", "secret", "api_key", "private_key"}


def _normalize_key(key):
    return str(key or "").strip().lower().replace("-", "_").replace(" ", "_")


def _is_sensitive_key(key):
    normalized = _normalize_key(key)
    return any(fragment in normalized for fragment in SENSITIVE_FRAGMENTS)


def sanitize_export(payload):
    """Return a sanitized top-level copy of an admin export payload.

    The sanitizer is used for support/admin bundle previews before data leaves TC1.
    It intentionally avoids changing the source payload object because preview and
    audit views may be rendered from the same parsed export.
    """
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
