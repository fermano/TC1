from src.tc1_service import normalize_owner


def test_owner_normalization_trims_and_lowercases():
    assert normalize_owner("  Release Ops  ") == "release-ops"


def test_owner_normalization_keeps_existing_slug():
    assert normalize_owner("platform-ops") == "platform-ops"


def test_owner_normalization_collapses_duplicate_separators():
    assert normalize_owner("Release   Ops___Primary") == "release-ops-primary"


def test_owner_normalization_strips_punctuation_edges():
    assert normalize_owner("!Platform Ops?") == "platform-ops"
