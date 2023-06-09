from abc import ABC, abstractmethod
from sqlalchemy.orm.query import Query


class PacketFilter(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_filter_expression(self) -> "FilterExpression":
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.get_filter_expression())
