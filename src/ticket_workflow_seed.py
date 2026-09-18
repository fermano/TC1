from src.handoff_models import DEFAULT_DELIVERY_LANE, normalize_delivery_lane


DEFAULT_OWNER = "engineering-ops"


def normalize_delivery_owner(owner: str | None) -> str:
    """Return the routing key used by delivery workflows."""
    normalized = " ".join((owner or "").split()).lower()
    return normalized or DEFAULT_OWNER


def filter_delivery_records(records: list[dict], owners: list[str | None] | None = None) -> list[dict]:
    """Filter records by canonical owner while preserving record order."""
    if owners is None:
        return records
    selected = {normalize_delivery_owner(owner) for owner in owners}
    return [
        record
        for record in records
        if normalize_delivery_owner(record.get("owner")) in selected
    ]


def delivery_summary(
    record: dict,
    include_source: bool = False,
    include_lane: bool = False,
) -> dict:
    """Return stable summary fields with optional source metadata."""
    summary = {
        "owner": normalize_delivery_owner(record.get("owner")),
        "status": record["status"],
    }
    if include_lane:
        summary["lane"] = _summary_lane_label(record)
    if include_source:
        source = _safe_provenance_label(record)
        if source:
            summary["source"] = source
    return summary


def _summary_lane_label(record: dict) -> str:
    if "lane" in record:
        return _required_lane_label(record["lane"], "lane")
    if "delivery_lane" in record:
        return _required_lane_label(record["delivery_lane"], "delivery_lane")
    return DEFAULT_DELIVERY_LANE


def _required_lane_label(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    return normalize_delivery_lane(value, field_name=field_name)


def _safe_provenance_label(record: dict) -> str:
    for field, legacy_token in (
        ("source_label", False),
        ("source_kind", False),
        ("source", True),
    ):
        label = _safe_label(record.get(field), legacy_token=legacy_token)
        if label:
            return label
    return ""


def _safe_label(value: object, *, legacy_token: bool) -> str:
    if not isinstance(value, str):
        return ""

    label = " ".join(value.split())
    if not label or _looks_unsafe_provenance(label):
        return ""
    if legacy_token and " " in label:
        return ""
    return label


def _looks_unsafe_provenance(label: str) -> bool:
    lowered = label.lower()
    if "://" in lowered or lowered.startswith("www.") or "/" in label or "\\" in label:
        return True
    unsafe_markers = (
        "api_key",
        "apikey",
        "callback_url",
        "credential",
        "password",
        "secret",
        "source_url",
        "token=",
    )
    return any(marker in lowered for marker in unsafe_markers)
