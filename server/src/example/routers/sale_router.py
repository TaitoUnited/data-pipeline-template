from flask import Blueprint, request, current_app
from src.common.utils.format import filter_item_properties
from src.common.utils.flask import validate_api_key
from ..services.sale_service import SaleService

sale_service = SaleService()

bp = Blueprint('sales', __name__, url_prefix='/example/sales')


@bp.route('')
def search():
    """Search for sales. API KEY can be given as X-API-KEY request header
       (recommended) or as api_key query parameter (for development).
    """
    # Authorize
    validate_api_key(request, current_app.config['API_KEY'])

    # Search
    sales = sale_service.search({
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
        'offset': request.args.get('offset'),
        'limit': request.args.get('limit'),
    })

    # Filter unwanted properties from response
    # NOTE: For optimal permormance we could filter these at sql query,
    # but for simplicity this is best handled at REST router and GraphQL
    # resolver.
    properties = request.args.get('properties')
    if properties:
        sales = filter_item_properties(sales, properties.split(','))

    # print(json.dumps({'joo': Decimal('1.1')}, cls=DecimalEncoder))

    return {'data': sales}
