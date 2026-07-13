def parse_approval_header(header: str) -> str:
    prefix, separator, value = header.partition(":")
    if separator != ":" or prefix.strip().lower() != "approved-by":
        raise ValueError("invalid approval header")
    return value.strip()
