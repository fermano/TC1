"""Candidate selection for the RC-64 digest export.

The release branch keeps this module intentionally small because the
release-room replay harness imports it directly when checking export
candidate drift.
"""

SUPPORTED_CHANNELS = {"email", "sms"}
SUPPRESSED_STATES = {"deleted", "suppressed", "bounced"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_")


def _is_retired(record):
    return bool(record.get("retired"))


def build_digest_candidates(records):
    """Return digest-export candidates in stable first-seen order.

    Rows with unsupported channels or terminal/suppressed states are skipped.
    The first row for a tenant/contact/channel wins so a replayed copy cannot
    duplicate a digest candidate.
    """
    candidates = []
    seen = set()

    for record in records:
        channel = _normalize(record.get("channel"))
        if channel not in SUPPORTED_CHANNELS:
            continue

        state = _normalize(record.get("state"))
        if state in SUPPRESSED_STATES:
            continue

        if _is_retired(record):
            continue

        key = (record.get("tenant_id"), record.get("contact_id"), channel)
        if key in seen:
            continue
        seen.add(key)

        candidates.append(
            {
                "tenant_id": record.get("tenant_id"),
                "contact_id": record.get("contact_id"),
                "channel": channel,
                "address": record.get("address"),
            }
        )

    return candidates
