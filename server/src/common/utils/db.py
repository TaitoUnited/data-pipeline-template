import re
from .misc import propertyExists


def add_paging(query, params):
    q = query

    if propertyExists(params, 'offset'):
        q += "OFFSET %(offset)s "

    if propertyExists(params, 'limit'):
        q += "LIMIT %(limit)s "

    return q


def generate_count_query(query):
    return re.sub(r"SELECT.*FROM", "SELECT count(*) FROM", query).replace(
        "OFFSET %(offset)s ", "").replace("LIMIT %(limit)s ", "")
