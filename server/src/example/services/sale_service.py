from ..daos.sale_dao import SaleDao


class SaleService:

    def __init__(self, sale_dao=None):
        self._sale_dao = sale_dao or SaleDao()

    def get_all(self):
        return self._sale_dao.get_all()
