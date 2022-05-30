from flask import Blueprint, current_app
from flasgger.utils import swag_from
from src.common.setup import db


bp = Blueprint("infra", __name__)


@bp.route("/config")
@swag_from("./swagger/infra_config.yaml")
def get_config():
    """Return configs that are required by web user interface or 3rd
    party clients.
    """
    # NOTE: This is a public endpoint. Do not return any secrets here!
    client_config = {
        "APP_VERSION": current_app.config["APP_VERSION"],
    }
    return {"data": client_config}


@bp.route("/healthz")
@swag_from("./swagger/infra_healthz.yaml")
def get_healtz():
    """Polled by Kubernetes to check that the container is alive."""
    return {"status": "OK"}


@bp.route("/uptimez")
@swag_from("./swagger/infra_uptimez.yaml")
def get_uptimez():
    """Polled by uptime monitor to check that the system is alive."""
    db.execute("SELECT 1")
    return {"status": "OK"}
