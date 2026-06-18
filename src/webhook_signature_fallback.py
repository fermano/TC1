def legacy_signature_fallback_enabled(environment):
    if environment == "release":
        return False
    return environment == "development"
