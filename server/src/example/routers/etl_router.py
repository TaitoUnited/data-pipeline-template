from flask import Blueprint, request, current_app
from src.common.utils.flask import validate_api_key
from ..etl import sale_etl


bp = Blueprint('etl', __name__, url_prefix='/example/etl')

# ---------------------------------------------------------------
# NOTE: If these ETLs are long running processes and triggered
# quite often with webhooks, consider using Celery to execute
# them in a separate worker process. Otherwise they might impair
# API performance as API has a limited amount of processes
# available.
# ---------------------------------------------------------------


@bp.route('/sales_extract', methods=('GET', 'POST'))
def run():
    """Run sales ETL process. API KEY can be given as X-API-KEY request header
       (recommended) or as api_key query parameter (for development).
    """
    validate_api_key(request, current_app.config['API_KEY'])
    sale_etl.extract()
    return {'status': 'OK'}
