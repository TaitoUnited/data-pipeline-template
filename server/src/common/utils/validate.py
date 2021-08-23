from werkzeug.exceptions import Forbidden, BadRequest


def validate_api_key(request, api_key):
    """Raises an exception if request contains invalid api key.
       API KEY can be given as X-API-KEY request header (recommended) or as
       api_key query parameter.
    """
    value = request.headers.get('x-api-key') or request.args.get('api_key')
    if not value:
        raise Forbidden("API KEY not given")
    if not api_key or value != api_key:
        raise Forbidden("Invalid API KEY")


def validate_is_one_word(value):
    """Raises an exception if value is not a one word"""
    if len(value.split()) > 1:
        raise BadRequest("Invalid value: " + value)
