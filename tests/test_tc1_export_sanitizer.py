from src.tc1_export_sanitizer import REDACTION, sanitize_export, summarize_export


def test_sanitize_export_redacts_nested_connector_auth():
    payload = {
        "tenant_id": "atlas",
        "connectors": [
            {
                "name": "slack",
                "auth": {
                    "access_token": "xoxb-live",
                    "client_secret": "shh",
                },
            }
        ],
    }

    sanitized = sanitize_export(payload)

    assert sanitized["connectors"][0]["auth"]["access_token"] == REDACTION
    assert sanitized["connectors"][0]["auth"]["client_secret"] == REDACTION


def test_sanitize_export_preserves_safe_secret_like_labels():
    payload = {
        "tenant_id": "atlas",
        "secretary_email": "ops@example.test",
        "public_token_hint": "starts-with-xoxb",
    }

    sanitized = sanitize_export(payload)

    assert sanitized["secretary_email"] == "ops@example.test"
    assert sanitized["public_token_hint"] == "starts-with-xoxb"


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
