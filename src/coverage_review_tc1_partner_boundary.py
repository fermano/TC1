def resolve_partner_value(payload, default=30):
    value = payload.get("send_after")
    if value is None:
        value = payload.get("sendAfter")
    return default if value in (None, "") else value
