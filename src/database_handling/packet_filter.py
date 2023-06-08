from abc import ABC, abstractmethod
from sqlalchemy.orm.query import Query


class PacketFilter(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def apply_filter(self, query: Query) -> Query:
        raise NotImplementedError()
