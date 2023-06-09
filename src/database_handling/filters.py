from .bases import PacketEntry
from sqlalchemy.orm.query import Query
import datetime

from . import PacketFilter


class SourceIPFilter(PacketFilter):
    def __init__(self, source_ip: str) -> None:
        self.source_ip = source_ip

    def get_filter_expression(self) -> "FilterExpression":
        return PacketEntry.source_ip == self.source_ip


class DestinationIPFilter(PacketFilter):
    def __init__(self, destination_ip: str) -> None:
        self.destination_ip = destination_ip

    def get_filter_expression(self) -> "FilterExpression":
        return PacketEntry.destination_ip == self.destination_ip


class SourcePortFilter(PacketFilter):
    def __init__(self, source_port: int) -> None:
        self.source_port = source_port

    def get_filter_expression(self) -> "FilterExpression":
        return PacketEntry.source_port == self.source_port


class DestinationPortFilter(PacketFilter):
    def __init__(self, destination_port: int) -> None:
        self.destination_port = destination_port

    def get_filter_expression(self) -> "FilterExpression":
        return PacketEntry.destination_port == self.destination_port


class ProtocolFilter(PacketFilter):
    def __init__(self, protocol: str) -> None:
        self.protocol = protocol

    def get_filter_expression(self) -> "FilterExpression":
        return PacketEntry.protocol == self.protocol


class LengthFilter(PacketFilter):
    def __init__(self, /, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper

    def get_filter_expression(self) -> "FilterExpression":
        return self.lower <= PacketEntry.length <= self.upper


class TimestampFilter(PacketFilter):
    def __init__(self, /, lower: datetime.datetime, upper: datetime.datetime) -> None:
        self.lower = lower
        self.upper = upper

    def get_filter_expression(self) -> "FilterExpression":
        return self.lower <= PacketEntry.timestamp <= self.upper
