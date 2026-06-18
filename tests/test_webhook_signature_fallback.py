from src.webhook_signature_fallback import legacy_signature_fallback_enabled


def test_release_disables_legacy_fallback():
    assert legacy_signature_fallback_enabled("release") is False


def test_development_keeps_local_fallback():
    assert legacy_signature_fallback_enabled("development") is True
