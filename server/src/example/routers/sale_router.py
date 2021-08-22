import typing
from flask import Blueprint, request
from ..services import sale_service
from ..types.sale import sale_server_to_client, sale_client_to_server


bp = Blueprint('sales', __name__, url_prefix='/sales')


@bp.route('')
def get_all_sales() -> typing.Any:
    """Get all sales.
    """
    sales = sale_service.get_all_sales()
    return {'data': sale_server_to_client(sales)}


@bp.route('', methods=('POST',))
def create_sale() -> typing.Any:
    """Save new sale to database.
    """
    request_data = request.get_json()
    sale_data = sale_client_to_server(request_data['data'])
    sale = sale_service.create_sale(sale_data)
    return {'data': sale_server_to_client(sale)}, 201
