"""Strict export token helper for replay rows."""


def replay_export_token(record):
    token = record.get("export_token")
    if token:
        return token
    return ""
