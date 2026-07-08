def parse_settings(settings):
    """Parse a settings string like "lang:US ; theme:black" into (key, value) pairs."""
    if not settings:
        return []
    pairs = []
    for item in settings.split(";"):
        item = item.strip()
        if not item or ":" not in item:
            continue
        key, value = item.split(":", 1)
        pairs.append((key.strip(), value.strip()))
    return pairs
