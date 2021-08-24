import time
from ..daos.sale_dao import SaleDao


class SaleEtlService:
    def __init__(self, sale_dao=None):
        self._sale_dao = sale_dao or SaleDao()

    def listen(self):
        while True:
            print("Example implementation that just keeps on running.")
            time.sleep(60)

    def extract(self):
        print("Example implementation that runs once.")
        print(self._sale_dao.search({}))
