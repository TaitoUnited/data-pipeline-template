from flask import Blueprint, request, current_app
from src.common.utils.flask import validate_api_key
from ..services import sale_etl_service


bp = Blueprint('actions', __name__, url_prefix='/example/actions')


@bp.route('/extract_sales', methods=('GET', 'POST'))
def run():
    """Run sales ETL process. API KEY can be given as X-API-KEY request header
       (recommended) or as api_key query parameter (for development).
    """
    validate_api_key(request, current_app.config['API_KEY'])
    sale_etl_service.extract()
    return {'status': 'OK'}
