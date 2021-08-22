import dataclasses
import psycopg2.sql
import typing
from src.common.setup import db
from ..types.sale import DBSale, Sale


DB_POST_FIELDS: psycopg2.sql.SQL = psycopg2.sql.SQL(',').join(
    psycopg2.sql.Identifier(f.name)
    for f in dataclasses.fields(DBSale)
    )


def get_all_sales() -> typing.List[DBSale]:
    """Get all sale from the database.
    """
    statement = psycopg2.sql.SQL('''
        SELECT      {fields}
        FROM        sales
        ORDER BY    created_at DESC
        ''').format(
            fields=DB_POST_FIELDS,
            )
    sales = db.execute(statement)
    return [DBSale(*sale) for sale in sales]


def create_sale(sale: Sale) -> DBSale:
    """Saves sale to the database.
    """
    insert_fields = []
    placeholders = []
    for f in dataclasses.fields(sale):
        insert_fields.append(psycopg2.sql.Identifier(f.name))
        placeholders.append(psycopg2.sql.Placeholder(f.name))

    statement = psycopg2.sql.SQL('''
        INSERT INTO sales ({insert_fields})
        VALUES      ({placeholders})
        RETURNING   {fields}
        ''').format(
            insert_fields=psycopg2.sql.SQL(',').join(insert_fields),
            placeholders=psycopg2.sql.SQL(',').join(placeholders),
            fields=DB_POST_FIELDS,
            )

    record = db.execute(
        statement,
        params=dataclasses.asdict(sale),
        single=True,
        )
    return DBSale(*record)
