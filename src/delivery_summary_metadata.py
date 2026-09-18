from src.ticket_workflow_seed import delivery_summary


def delivery_summary_with_source(record: dict, include_source: bool = False) -> dict:
    return delivery_summary(record, include_source=include_source)
