"""Birch release delivery replay."""

from src.tc1_birch_contract import decode_delivery_key, delivery_context, delivery_key
from src.tc1_birch_intake import hold_for, source_for


def _revision(event):
    return int(event.get("revision", 0))


def restore_deliveries(persisted_keys, events, default_seconds=120):
    deliveries = {}
    for persisted_key in persisted_keys:
        tenant_id, channel_id, message_id, source = decode_delivery_key(persisted_key)
        deliveries[delivery_key(tenant_id, channel_id, message_id, source)] = {
            "state": "queued",
            "revision": 0,
            **delivery_context(channel_id, source),
        }

    for event in events:
        source = source_for(event)
        key = delivery_key(
            event["tenant_id"], event["channel_id"], event["message_id"], source
        )
        if _revision(event) < deliveries.get(key, {}).get("revision", -1):
            continue
        if event["kind"] == "void":
            deliveries[key] = {
                "state": "void",
                "revision": _revision(event),
                **delivery_context(event["channel_id"], source),
            }
            continue
        deliveries[key] = {
            "state": "queued",
            "revision": _revision(event),
            "hold_seconds": hold_for(event, default_seconds),
            **delivery_context(event["channel_id"], source),
        }
    return deliveries
