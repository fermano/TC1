"""Compatibility handling for paginated delivery cursors."""


def select_cursor(parameters):
    """Read a cursor while old and new clients overlap."""
    if "cursor" in parameters:
        return parameters["cursor"]
    return parameters.get("after")
