from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit


def redact_download_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", parts.fragment))
