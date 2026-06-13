import hashlib
import json

_checksum_cache = {}


def manifest_checksum(manifest_id, rows):
    """Return a stable checksum for a retried release manifest."""
    if manifest_id in _checksum_cache:
        return _checksum_cache[manifest_id]

    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    checksum = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    _checksum_cache[manifest_id] = checksum
    return checksum


def clear_manifest_checksum_cache():
    _checksum_cache.clear()
