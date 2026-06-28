def export_fallback_enabled(environment):
    if environment == "release":
        return False
    return environment == "development"
