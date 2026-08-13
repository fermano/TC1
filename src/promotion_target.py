"""Target selection for queued promotion actions."""


def target_for_promotion(action, current_target):
    """Choose the deployment target when a queued action is applied."""
    return action.get("target") or current_target
