from src.tc1_export_sanitizer import REDACTION, sanitize_export, summarize_export


def test_sanitize_export_redacts_top_level_secrets():
    payload = {
        "tenant_id": "atlas",
        "api_key": "sk-live-123",
        "password": "correct-horse",
        "workspace_id": "ws-1",
    }

    sanitized = sanitize_export(payload)

    assert sanitized["api_key"] == REDACTION
    assert sanitized["password"] == REDACTION
    assert sanitized["tenant_id"] == "atlas"
    assert sanitized["workspace_id"] == "ws-1"


def test_sanitize_export_preserves_safe_secret_like_labels():
    payload = {
        "tenant_id": "atlas",
        "secretary_email": "ops@example.test",
        "public_token_hint": "starts-with-xoxb",
    }

    sanitized = sanitize_export(payload)

    assert sanitized["secretary_email"] == "ops@example.test"
    assert sanitized["public_token_hint"] == "starts-with-xoxb"


def test_sanitize_export_does_not_mutate_top_level_payload():
    payload = {"tenant_id": "atlas", "api_key": "sk-live-123"}

    sanitized = sanitize_export(payload)

    assert sanitized is not payload
    assert payload["api_key"] == "sk-live-123"


def test_summarize_export_counts_connectors_and_includes_sanitized_copy():
    payload = {
        "tenant_id": "atlas",
        "workspace_id": "ws-1",
        "connectors": [{"name": "slack"}, {"name": "github"}],
        "api_key": "sk-live-123",
    }

    summary = summarize_export(payload)

    assert summary["tenant_id"] == "atlas"
    assert summary["workspace_id"] == "ws-1"
    assert summary["connector_count"] == 2
    assert summary["sanitized"]["api_key"] == REDACTION
