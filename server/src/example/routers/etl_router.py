from flask import Blueprint, request, current_app
from src.common.utils.validate import validate_api_key
from ..services.sale_etl_service import SaleEtlService

sale_etl_service = SaleEtlService()

bp = Blueprint("etl", __name__, url_prefix="/example/etl")

# NOTE: Consider using celery to run such ETL processes in the worker container
# that are long-running processes and executed so often that multiple
# webhook triggered ETL processes may be running simultaneously.


@bp.route("/sales_extract", methods=("GET", "POST"))
def sales_extract():
    """Run sales ETL process. API KEY can be given as X-API-KEY request header
    (recommended) or as api_key query parameter (for development).
    """
    # Authorize
    validate_api_key(request, current_app.config["API_KEY"])

    # Run ETL
    sale_etl_service.extract()

    return {"status": "OK"}
