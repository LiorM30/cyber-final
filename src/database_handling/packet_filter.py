from abc import ABC, abstractmethod
from sqlalchemy.sql.elements import BinaryExpression


class PacketFilter(ABC):
    """Abstract class for packet filters.
    """

    @abstractmethod
    def get_filter_expression(self) -> BinaryExpression:
        """Return a SQLAlchemy BinaryExpression representing the filter.
        """
        raise NotImplementedError("Child class must implement abstract method")
