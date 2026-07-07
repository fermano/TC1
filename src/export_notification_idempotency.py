from __future__ import annotations


class NotificationLedger:
    def __init__(self) -> None:
        self._sent: set[str] = set()

    def claim(self, export_job_id: str) -> bool:
        if export_job_id in self._sent:
            return False
        self._sent.add(export_job_id)
        return True
