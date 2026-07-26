"""Compatibility handling for paginated delivery cursors."""


def select_cursor(parameters):
    """Read a cursor while old and new clients overlap."""
    return parameters.get("after") or parameters.get("cursor")
