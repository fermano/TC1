"""Audit-page deduplication used by resumable exports."""


def dedupe_audit_pages(pages, start_page=0):
    seen = set()
    output = []
    for page in pages[start_page:]:
        for record in page:
            record_id = record["id"]
            if record_id in seen:
                continue
            seen.add(record_id)
            output.append(record)
    return output
