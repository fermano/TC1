"""RC-61 release gate evaluation."""

from __future__ import annotations

from typing import Iterable, Mapping


PASSING_STATES = {"passed", "skipped"}
BLOCKING_STATES = {"failed", "blocked", "manual_hold"}


def _normalize_state(state: object) -> str:
    return str(state).strip().lower().replace(" ", "_")


def evaluate_release_checks(checks: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Return the release-gate decision for a set of check rows.

    Required checks in a blocking state hold the release. Optional checks are
    advisory only. Unknown required states are listed as advisory so operators
    can inspect them without failing old clients during rollout.
    """

    blockers: list[str] = []
    advisory: list[str] = []

    for index, check in enumerate(checks):
        name = str(check.get("name") or f"check-{index + 1}")
        required = bool(check.get("required", True))
        state = _normalize_state(check.get("state", ""))

        if required and state in BLOCKING_STATES:
            blockers.append(name)
        elif required and state not in PASSING_STATES:
            advisory.append(name)
        elif not required and state not in PASSING_STATES:
            advisory.append(name)

    return {
        "ready": not blockers,
        "blockers": blockers,
        "advisory": advisory,
    }
