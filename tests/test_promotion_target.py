from src.promotion_target import target_for_promotion


def test_action_without_target_uses_current_release_target():
    assert target_for_promotion({}, "green") == "green"


def test_action_target_is_retained():
    assert target_for_promotion({"target": "blue"}, "blue") == "blue"
