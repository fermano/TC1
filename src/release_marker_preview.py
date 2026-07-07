"""Release-marker normalization for status previews."""

from __future__ import annotations

import re


_RELEASE_PREFIX_RE = re.compile(r"^release:\\s*", re.IGNORECASE)


def parse_release_marker_preview(note: str) -> str:
    """Return a plain marker after removing an optional support-note prefix."""
    marker = note.strip()
    marker = _RELEASE_PREFIX_RE.sub("", marker, count=1).strip()
    if not marker:
        raise ValueError("release marker must include a value")
    return marker
