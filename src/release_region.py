REGION_ALIASES = {
    "us-east": "us-east-1",
    "use1": "us-east-1",
    "eu-west": "eu-west-1",
    "euw1": "eu-west-1",
}


def normalize_release_region(value):
    key = value.strip().lower()
    return REGION_ALIASES.get(key, key)
