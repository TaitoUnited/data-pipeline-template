from flask import current_app


def get_secret_value(name):
    """Returns secret value"""
    value = current_app.config[name]
    if value:
        return value

    current_app.logger.warning(
        "Secret "
        + name
        + " not found in Flask config."
        + "Fetching it from disk."
    )
    f = None
    try:
        f = open("/run/secrets/" + name, "r")
        return f.read()
    finally:
        f.close()


def filter_item_properties(items, propertyNames):
    """Filters properties from items by propertyName"""
    filtered = []
    for item in items:
        filtered.append(
            {
                propertyName: item[propertyName]
                for propertyName in propertyNames
            }
        )
    return filtered


def propertyExists(item, properyName):
    return properyName in item and item[properyName]
