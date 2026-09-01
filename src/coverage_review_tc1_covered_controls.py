def route_mode(value):
    if value is None:
        return "default"
    if value == "manual":
        return "manual"
    return "automatic"
