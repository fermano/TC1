from src.rc59_preview import PlanCache, preview_export


def test_preview_contains_records_and_timezone():
    cache = PlanCache()

    plan = preview_export(["evt-1", "evt-2"], cache, timezone="America/Sao_Paulo")

    assert plan["record_count"] == 2
    assert plan["timezone"] == "America/Sao_Paulo"
    assert plan["name"] == "export-preview-america-sao_paulo-2"


def test_preview_is_read_only_by_default():
    cache = PlanCache()
    saved_plan = preview_export(["scheduled-event"], cache, save_plan=True)

    preview = preview_export(["inspection-event"], cache)

    assert preview["records"] == ["inspection-event"]
    assert cache.saved == [saved_plan]


def test_preview_can_be_saved_for_later_use():
    cache = PlanCache()

    plan = preview_export(["evt-3"], cache, save_plan=True)

    assert cache.saved == [plan]
