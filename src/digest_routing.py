DEFAULT_DIGEST_OWNER = "release-operations"


def select_digest_owner(
    customer_override: str | None,
    persisted_owner: str | None,
) -> str:
    override = (customer_override or "").strip()
    if override:
        return override

    persisted = (persisted_owner or "").strip()
    return persisted or DEFAULT_DIGEST_OWNER
