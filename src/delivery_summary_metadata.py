from src.ticket_workflow_seed import delivery_summary


def delivery_summary_with_source(record: dict, include_source: bool = False) -> dict:
    result = delivery_summary(record)
    source = record.get("source")
    if include_source and isinstance(source, str) and source.strip():
        result["source"] = source.strip()
    return result
