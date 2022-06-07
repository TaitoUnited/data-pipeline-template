from werkzeug.exceptions import Forbidden, BadRequest, InternalServerError


def validate_api_key(request, *api_keys):
    """Raises an exception if request contains invalid api key.
    API KEY can be given as X-API-KEY request header (recommended) or as
    api_key query parameter.
    """
    if not api_keys:
        raise InternalServerError("API KEY configuration error")

    value = request.headers.get("x-api-key") or request.query_params.get(
        "api_key"
    )
    if not value:
        raise Forbidden("API KEY not given")

    found = False
    for key in api_keys:
        if not key:
            raise InternalServerError("API KEY configuration error")
        if key == value:
            found = True

    if not found:
        raise Forbidden("Invalid API KEY")


def validate_is_one_word(value):
    """Raises an exception if value is not a one word"""
    if len(value.split()) > 1:
        raise BadRequest("Invalid value: " + value)
