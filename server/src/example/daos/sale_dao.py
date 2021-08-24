from psycopg2 import sql
from src.common.setup import db
from src.common.utils.misc import propertyExists
from src.common.utils.db import add_paging, generate_count_query


class SaleDao:
    def search(self, params):
        """Search for sales
        NOTE: This will fail if view_sales does not exist yet!
        """
        query = "SELECT * FROM view_sales WHERE 1=1 "

        if propertyExists(params, "start_date"):
            query += "AND date >= %(start_date)s "

        if propertyExists(params, "end_date"):
            query += "AND date < %(end_date)s "

        query = add_paging(query, params)

        count_query = generate_count_query(query)
        return {
            "total": db.execute(sql.SQL(count_query), params=params),
            "data": db.execute(sql.SQL(query), params=params),
        }
