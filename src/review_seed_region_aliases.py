"""Canonical aliases accepted by delivery-region selection."""

REGION_ALIASES = {
    "eu": "eu-west-1",
    "europe": "eu-west-1",
    "us": "us-east-1",
}


def normalize_delivery_region(value):
    normalized = value.strip().lower()
    return REGION_ALIASES.get(normalized, normalized)
