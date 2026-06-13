from src.export_fallback_flag import export_fallback_enabled


def test_release_environment_disables_fallback():
    assert export_fallback_enabled("release") is False


def test_development_keeps_local_fallback():
    assert export_fallback_enabled("development") is True
