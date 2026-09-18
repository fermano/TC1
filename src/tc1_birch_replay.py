"""Birch release delivery replay."""

from src.tc1_birch_contract import decode_delivery_key, delivery_context, delivery_key
from src.tc1_birch_intake import hold_for, source_for


def _revision(event):
    value = event.get("revision", 0)
    if value is None or (isinstance(value, str) and not value.strip()):
        return 0
    return int(value)


def restore_deliveries(persisted_keys, events, default_seconds=120, artifact_ref="birch-rc-3"):
    deliveries = {}
    delivery_revisions = {}
    for persisted_key in persisted_keys:
        tenant_id, channel_id, message_id, source = decode_delivery_key(persisted_key)
        key = delivery_key(tenant_id, channel_id, message_id, source)
        delivery_revisions[key] = 0
        deliveries[key] = {
            "state": "queued",
            **delivery_context(channel_id, source, artifact_ref),
        }

    for event in events:
        source = source_for(event)
        key = delivery_key(
            event["tenant_id"], event["channel_id"], event["message_id"], source
        )
        revision = _revision(event)
        if revision < delivery_revisions.get(key, -1):
            continue
        delivery_revisions[key] = revision
        if event["kind"] == "void":
            deliveries.pop(key, None)
            continue
        deliveries[key] = {
            "state": "queued",
            "hold_seconds": hold_for(event, default_seconds),
            **delivery_context(event["channel_id"], source, artifact_ref),
        }
    return deliveries
