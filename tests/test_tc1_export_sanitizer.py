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
