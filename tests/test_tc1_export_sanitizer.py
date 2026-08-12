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
            },
            {
                "name": "github",
                "auth": {
                    "refresh-token": "gho-live",
                    "signing secret": "signed",
                },
            },
        ],
    }

    sanitized = sanitize_export(payload)

    assert sanitized["connectors"][0]["auth"]["access_token"] == REDACTION
    assert sanitized["connectors"][0]["auth"]["client_secret"] == REDACTION
    assert sanitized["connectors"][1]["auth"]["refresh-token"] == REDACTION
    assert sanitized["connectors"][1]["auth"]["signing secret"] == REDACTION
    assert sanitized["connectors"][0]["name"] == "slack"
    assert sanitized["connectors"][1]["name"] == "github"


def test_sanitize_export_preserves_safe_secret_like_labels():
    payload = {
        "tenant_id": "atlas",
        "owner_email": "ops@example.test",
        "secretary_email": "release-coord@example.test",
        "public_token_hint": "xoxb-****",
    }

    sanitized = sanitize_export(payload)

    assert sanitized["owner_email"] == "ops@example.test"
    assert sanitized["secretary_email"] == "release-coord@example.test"
    assert sanitized["public_token_hint"] == "xoxb-****"


def test_sanitize_export_does_not_mutate_top_level_payload():
    payload = {"tenant_id": "atlas", "api_key": "sk-live-123"}

    sanitized = sanitize_export(payload)

    assert sanitized is not payload
    assert payload["api_key"] == "sk-live-123"


def test_sanitize_export_does_not_mutate_nested_payload():
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

    assert sanitized is not payload
    assert sanitized["connectors"] is not payload["connectors"]
    assert sanitized["connectors"][0] is not payload["connectors"][0]
    assert sanitized["connectors"][0]["auth"] is not payload["connectors"][0]["auth"]
    assert payload["connectors"][0]["auth"]["access_token"] == "xoxb-live"
    assert payload["connectors"][0]["auth"]["client_secret"] == "shh"


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
