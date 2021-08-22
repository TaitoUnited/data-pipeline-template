import os
from flask import Flask
from .infra import infra_router


def register_rest_routes(app: Flask):
    # -------------------------------------------
    # NOTE: Add your REST API routers here
    # -------------------------------------------
    app.register_blueprint(infra_router.bp)

    # Register example routes on development mode only
    if os.environ.get('FLASK_ENV') == 'development':
        from .example.routers import etl_router, sale_router
        app.register_blueprint(etl_router.bp)
        app.register_blueprint(sale_router.bp)


def register_graphql_resolvers(app: Flask):
    # -------------------------------------------
    # NOTE: Add your GraphQL API resolvers here
    # -------------------------------------------
    # TODO: Add GraphQL support
    return
