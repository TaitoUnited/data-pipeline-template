from psycopg2 import sql
from src.common.setup import db
from src.common.utils.misc import propertyExists


class SaleDao:

    def search(self, params):
        """Search for sales
           NOTE: This will fail if view_sales does not exist yet!
        """
        query = "SELECT * FROM view_sales WHERE 1=1 "

        if propertyExists(params, 'start_date'):
            query += "AND date >= %(start_date)s "

        if propertyExists(params, 'end_date'):
            query += "AND date < %(end_date)s "

        if propertyExists(params, 'offset'):
            query += "OFFSET %(offset)s "

        if propertyExists(params, 'limit'):
            query += "LIMIT %(limit)s "

        return db.execute(sql.SQL(query), params=params)
