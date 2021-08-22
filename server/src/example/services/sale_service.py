import typing
from ..types.sale import DBSale, Sale
from ..daos import sale_dao


def get_all_sales() -> typing.List[DBSale]:
    return sale_dao.get_all_sales()


def create_sale(data: Sale) -> DBSale:
    return sale_dao.create_sale(data)
