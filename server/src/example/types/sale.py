from pydantic.dataclasses import dataclass
import dataclasses
import typing
from src.common.types.entity import DBItem
from src.common.utils.format import to_camel, to_snake


@dataclass
class Sale:
    author: str
    content: str
    subject: str


@dataclass
class DBSale(DBItem, Sale):
    pass


SaleDict = typing.Dict[str, typing.Any]


@typing.overload
def sale_server_to_client(data: typing.List[DBSale]) -> typing.List[SaleDict]:
    pass


@typing.overload
def sale_server_to_client(data: DBSale) -> SaleDict:
    pass


def sale_server_to_client(data):
    """Converst DBSale to dict.
    """
    def convert(sale: DBSale) -> SaleDict:
        return to_camel(dataclasses.asdict(sale))
    if type(data) is DBSale:
        return convert(data)
    return [convert(sale) for sale in data]


def sale_client_to_server(data: SaleDict) -> typing.Union[DBSale, Sale]:
    """Converts sale json from client to Sale or DBSale.

    The result depends whether the saleed data contains and id.
    """
    _data = to_snake(data)
    try:
        return DBSale(**_data)  # type: ignore
    except TypeError:
        # If the request is missing createdAt, id, updatedAt fields
        # then TypeError will be raised. So we can deduct that this is
        # new sale.
        return Sale(**_data)  # type: ignore
