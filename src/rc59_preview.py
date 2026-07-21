"""Export preview planning and optional local plan persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class PlanCache:
    saved: list[dict[str, object]] = field(default_factory=list)

    def save(self, plan: dict[str, object]) -> None:
        self.saved.append(dict(plan))


def format_preview(records: Iterable[str], timezone: str = "UTC") -> dict[str, object]:
    values = list(records)
    return {
        "name": f"export-preview-{len(values)}",
        "timezone": timezone,
        "record_count": len(values),
        "records": values,
    }


def preview_export(
    records: Iterable[str],
    cache: PlanCache,
    *,
    timezone: str = "UTC",
    save_plan: bool = False,
) -> dict[str, object]:
    plan = format_preview(records, timezone)
    cache.save(plan)
    return plan
