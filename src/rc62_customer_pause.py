"""RC-62 customer pause delivery gating."""

from __future__ import annotations

from typing import Iterable, Mapping


PAUSED_STATES = {"paused", "hold", "manual_hold", "customer_paused"}


def _normalize_state(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_")


def eligible_deliveries(rows: Iterable[Mapping[str, object]]) -> list[str]:
    """Return delivery IDs that may proceed for the RC-62 sender.

    Delivery rows without a state are treated as active for compatibility with
    older scheduler clients. Paused rows must be filtered before dispatch.
    """

    eligible: list[str] = []
    for index, row in enumerate(rows):
        delivery_id = str(row.get("delivery_id") or f"delivery-{index + 1}")
        state = _normalize_state(row.get("state", "active"))
        if state not in PAUSED_STATES:
            eligible.append(delivery_id)
    return eligible
