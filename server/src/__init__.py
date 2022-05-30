import os
import typing
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from src.common.setup.json import CustomJSONEncoder
from . import api


def create_app(
    single_command=False,
    connect_database=True,
    init_routes=True,
    test_config: typing.Optional[typing.Mapping[str, typing.Any]] = None,
) -> Flask:
    """Flask app factory."""
    app = Flask(__name__)
    app.config["CORS_SUPPORTS_CREDENTIALS"] = True
    app.config["CORS_EXPOSE_HEADERS"] = [
        "Content-Type",
        "Content-Length",
        "Content-Encoding",
    ]
    CORS(app)
    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        from src.common.setup import config

        app.config.from_object(config.Config)
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    from src.common.setup import log, sentry

    log.setup(app)
    sentry.connect(app)

    # Swagger configurations
    app.config["SWAGGER"] = {
        "title": "data-pipeline-template",
        "uiversion": 3,
    }
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "data-pipeline-template | REST API",
            "description": "API for ...",
        },
        "basePath": "/",
        "swaggerUiPrefix": "/api",
        "schemes": ["https"],
        "securityDefinitions": {
            "BasicAuth": {
                "type": "basic",
                "name": "basic authentication",
                "in": "header",
            },
            "apiKey": {
                "type": "apiKey",
                "name": "X-API-KEY",
                "in": "header",
            },
        },
        "security": {"BasicAuth": [], "apiKey": []},
    }
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/",
    }

    swagger = Swagger(app, config=swagger_config, template=swagger_template)

    @app.errorhandler(Exception)
    def handle_bad_request(e: Exception) -> typing.Any:
        """Catch-all exception handler."""
        # Create an id for the exception to make searching the logs
        # easier.
        e_id = id(e)
        setattr(e, "log_id", e_id)
        app.logger.exception(f"Unhandled exception ({e_id}): {e}")
        # All werkzeug raised exceptions (404 etc) have response code
        # assigned to them.
        code = getattr(e, "code", 500)
        return {
            "error": {
                "message": str(e)
                if code < 500
                else f"{code}: Unexpected error",
                "id": e_id,
            }
        }, code

    def setup_flask_worker() -> None:
        # Connect infra
        from src.common.setup import db

        if connect_database:
            db.connect(app)
        if init_routes:
            api.register_rest_routes(app)
            api.register_graphql_resolvers(app)

    if single_command or os.environ.get("FLASK_ENV") == "development":
        setup_flask_worker()

    else:
        import uwsgidecorators

        uwsgidecorators.postfork(setup_flask_worker)

    return app
