from dataclasses import dataclass


@dataclass(frozen=True)
class OperationSignal:
    owner: str
    severity: str


def build_release_marker(version: str, channel: str) -> str:
    normalized_channel = channel.strip() or "internal"
    return f"{version}-{normalized_channel}"
