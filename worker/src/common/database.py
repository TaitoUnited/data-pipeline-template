import os
from sqlalchemy import create_engine as create_sqlalchemy_engine


# Create sqlalchemy database engine
def create_engine():
    return create_sqlalchemy_engine(os.path.expandvars(
        "postgresql://$DATABASE_USER:$DATABASE_PASSWORD@$DATABASE_HOST:" +
        "$DATABASE_PORT/$DATABASE_NAME"
    ))


# Get JDBC database url
def get_jdbc_url():
    return os.path.expandvars(
        "jdbc:postgresql://$DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME"
    )


# Get JDBC database options
def get_jdbc_options():
    return {
        "driver": "org.postgresql.Driver",
        "user": os.environ['DATABASE_USER'],
        "password": os.environ['DATABASE_PASSWORD']
    }
