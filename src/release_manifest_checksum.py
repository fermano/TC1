import hashlib
import json

_checksum_cache = {}


def manifest_checksum(manifest_id, rows):
    """Return a stable checksum for a retried release manifest."""
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))

    if manifest_id in _checksum_cache:
        cached_payload, cached_checksum = _checksum_cache[manifest_id]
        if payload != cached_payload:
            raise ValueError("manifest ID is already bound to a different payload")
        return cached_checksum

    checksum = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    _checksum_cache[manifest_id] = (payload, checksum)
    return checksum


def clear_manifest_checksum_cache():
    _checksum_cache.clear()
