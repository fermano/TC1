"""Offset-based audit export prototype."""


def page_from_offset(records, offset=0, limit=100):
    ordered = sorted(records, key=lambda item: (item["occurred_at"], item["id"]))
    page = ordered[offset : offset + limit]
    next_offset = offset + len(page)
    return page, str(next_offset)
