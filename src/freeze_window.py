from datetime import datetime
from zoneinfo import ZoneInfo


def is_in_freeze_window(
    instant: datetime,
    timezone_name: str,
    start_hour: int,
    end_hour: int,
) -> bool:
    local_hour = instant.astimezone(ZoneInfo(timezone_name)).hour
    if start_hour < end_hour:
        return start_hour <= local_hour < end_hour
    return local_hour >= start_hour or local_hour < end_hour
