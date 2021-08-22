import psycopg2.sql
from src.common.setup import db


def get_all():
    """Get all sales from the database.
    """
    try:
        statement = psycopg2.sql.SQL('''
            SELECT      *
            FROM        view_sales
            ORDER BY    created_at DESC
            ''')
        return db.execute(statement)
    except Exception:
        # Return some dummy data as the view_sales does not exist yet
        return [
            {'quantity': '1', 'price': '99'},
            {'quantity': '2', 'price': '203'},
        ]
