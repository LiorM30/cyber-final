from .bases import PacketEntry
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.operators import OperatorType
from sqlalchemy import and_, or_
import datetime

from . import PacketFilter


class CompoundFilter(PacketFilter):
    def __init__(self, filter: PacketFilter) -> None:
        self.expression = filter.get_filter_expression()

    def AND(self, filter: PacketFilter) -> None:
        self.expression = and_(self.expression, filter.get_filter_expression())

    def OR(self, filter: PacketFilter) -> None:
        self.expression = or_(self.expression, filter.get_filter_expression())

    def get_filter_expression(self) -> BinaryExpression:
        return self.expression


class SourceIPFilter(PacketFilter):
    def __init__(self, source_ip: str) -> None:
        self.source_ip = source_ip

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.source_ip == self.source_ip


class DestinationIPFilter(PacketFilter):
    def __init__(self, destination_ip: str) -> None:
        self.destination_ip = destination_ip

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.destination_ip == self.destination_ip


class SourcePortFilter(PacketFilter):
    def __init__(self, source_port: int) -> None:
        self.source_port = source_port

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.source_port == self.source_port


class DestinationPortFilter(PacketFilter):
    def __init__(self, destination_port: int) -> None:
        self.destination_port = destination_port

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.destination_port == self.destination_port


class ProtocolFilter(PacketFilter):
    def __init__(self, protocol: str) -> None:
        self.protocol = protocol

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.protocol == self.protocol


class LengthFilter(PacketFilter):
    def __init__(self, /, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper

    def get_filter_expression(self) -> BinaryExpression:
        return self.lower <= PacketEntry.length <= self.upper


class SniffedBeforeFilter(PacketFilter):
    def __init__(self, timestamp: datetime.datetime) -> None:
        self.timestamp = timestamp

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.timestamp <= self.timestamp


class SniffedAfterFilter(PacketFilter):
    def __init__(self, timestamp: datetime.datetime) -> None:
        self.timestamp = timestamp

    def get_filter_expression(self) -> BinaryExpression:
        return PacketEntry.timestamp >= self.timestamp
