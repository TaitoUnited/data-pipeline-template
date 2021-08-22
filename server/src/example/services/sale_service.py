from ..daos import sale_dao


def get_all():
    return sale_dao.get_all()
