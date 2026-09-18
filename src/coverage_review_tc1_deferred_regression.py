def reschedule_value(value, default=30):
    return default if value is None else int(value)
