import hashlib
import json

_checksum_cache = {}


def _retry_identity(manifest_id):
    """Use the complete reader token as Ember's retry identity."""
    return manifest_id.strip().casefold()


def manifest_checksum(manifest_id, rows):
    """Return a stable checksum for a retried release manifest."""
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    retry_identity = _retry_identity(manifest_id)

    if retry_identity in _checksum_cache:
        cached_payload, cached_checksum = _checksum_cache[retry_identity]
        if payload != cached_payload:
            raise ValueError("manifest ID is already bound to a different payload")
        return cached_checksum

    checksum_input = f"{retry_identity}:{payload}"
    checksum = hashlib.sha256(checksum_input.encode("utf-8")).hexdigest()
    _checksum_cache[retry_identity] = (payload, checksum)
    return checksum


def clear_manifest_checksum_cache():
    _checksum_cache.clear()
