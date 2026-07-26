"""Formatting helpers for delivery preview metadata."""


def preview_trace_label(trace_id, source):
    """Return a compact operator-facing trace label."""
    normalized_source = (source or "unknown").strip() or "unknown"
    return f"{normalized_source}:{trace_id}"
