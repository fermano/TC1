def coalesce_retry_rows(rows):
    result = []
    seen = set()
    for row in sorted(rows, key=lambda item: item.get("attempt", 0), reverse=True):
        key = (row["invoice_id"], row.get("attempt", 0))
        if key in seen:
            continue
        seen.add(key)
        result.append(row)
    return list(reversed(result))
