from werkzeug.exceptions import Forbidden


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
