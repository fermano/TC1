from __future__ import annotations

from collections.abc import Mapping

_FILTER_FIELDS = ("owner", "window", "minimum_severity")


def save_filter(values: Mapping[str, object]) -> dict[str, object]:
    return {key: values[key] for key in _FILTER_FIELDS if key in values}


def restore_filter(values: Mapping[str, object]) -> dict[str, object]:
    restored = save_filter(values)
    restored.setdefault("minimum_severity", "low")
    return restored
