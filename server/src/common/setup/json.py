from json import JSONEncoder
from decimal import Decimal


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        # Convert decimal into string to keep precision
        if isinstance(obj, Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)
