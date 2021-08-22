import os
from flask import Flask
from .infra import infra_router


def register_rest_routes(app: Flask):
    # -----------------------------------------------------------------------
    # NOTE: Add your routers here. They implement the REST API endpoints.
    # -----------------------------------------------------------------------
    app.register_blueprint(infra_router.bp)

    # Register example routes on development mode only
    if os.environ.get('FLASK_ENV') == 'development':
        from .example.routers import action_router, sale_router
        app.register_blueprint(action_router.bp)
        app.register_blueprint(sale_router.bp)


def register_graphql_resolvers(app: Flask):
    # -----------------------------------------------------------------------
    # NOTE: Add your resolvers here. They implement the GraphQL endpoints.
    # -----------------------------------------------------------------------
    # TODO: Add GraphQL support
    return
