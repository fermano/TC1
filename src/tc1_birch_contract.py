"""Birch release delivery contract."""

def delivery_key(tenant_id, channel_id, message_id, source):
    return f"{tenant_id}:{channel_id}:{message_id}:{source}"


def decode_delivery_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "primary")
    return tuple(parts)


def delivery_context(channel_id, source, artifact_ref):
    return {
        "release": "birch-3",
        "record_shape": "v3",
        "delivery_epoch": "g11",
        "channel": channel_id,
        "artifact_ref": artifact_ref,
        "source": source,
    }
