from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class CaseLifecycleEvent:
    kind: str
    at: datetime | str


@dataclass(frozen=True)
class OwnerCloseWarning:
    case_id: str
    owner: str
    warn_at: datetime
    close_at: datetime


def normalize_escalation_deadline(value):
    return _parse_aware_datetime(value).isoformat().replace("+00:00", "Z")


def schedule_owner_close_warning(
    case_id: str,
    owner: str,
    close_at: datetime | str,
    *,
    warn_before_seconds: int,
    lifecycle_events: Iterable[CaseLifecycleEvent] = (),
) -> OwnerCloseWarning | None:
    if warn_before_seconds < 0:
        raise ValueError("warn_before_seconds must not be negative")

    normalized_close_at = _parse_aware_datetime(close_at)
    warn_at = normalized_close_at - timedelta(seconds=warn_before_seconds)
    if _has_manual_close_before_warning(lifecycle_events, warn_at):
        return None

    return OwnerCloseWarning(
        case_id=case_id.strip(),
        owner=owner.strip(),
        warn_at=warn_at,
        close_at=normalized_close_at,
    )


def _has_manual_close_before_warning(
    lifecycle_events: Iterable[CaseLifecycleEvent], warn_at: datetime
) -> bool:
    for event in lifecycle_events:
        event_kind = event.kind.strip().lower().replace("-", "_")
        if (
            event_kind == "manual_closed"
            and _parse_aware_datetime(event.at) <= warn_at
        ):
            return True
    return False


def _parse_aware_datetime(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("deadline must include a timezone")
    return parsed.astimezone(timezone.utc)
