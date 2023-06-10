from abc import ABC, abstractmethod
from sqlalchemy.sql.elements import BinaryExpression


class PacketFilter(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_filter_expression(self) -> BinaryExpression:
        raise NotImplementedError()

    def __str__(self) -> str:
        return str(self.get_filter_expression())
