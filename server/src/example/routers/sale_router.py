from flask import Blueprint, request, current_app
from src.common.utils.format import filter_item_properties
from src.common.utils.flask import validate_api_key
from ..services.sale_service import SaleService

sale_service = SaleService()

bp = Blueprint('sales', __name__, url_prefix='/example/sales')


@bp.route('')
def get_all():
    """Get all sales. API KEY can be given as X-API-KEY request header
       (recommended) or as api_key query parameter (for development).
    """
    validate_api_key(request, current_app.config['API_KEY'])
    sales = sale_service.get_all()

    # Filter unwanted properties from response
    properties = request.args.get('properties')
    if properties:
        sales = filter_item_properties(sales, properties.split(','))

    return {'data': sales}
