from abc import ABC, abstractproperty

from . import ProtocolParser, TrafficAnalyzer
from .database_handling import PacketFilter


class ApplicationContainer(ABC):
    @abstractproperty
    def database_url(self) -> str:
        """The url of the database to use"""
        raise NotImplementedError()

    @abstractproperty
    def filters(self) -> list[str]:
        """The filters to use"""
        raise NotImplementedError()

    @abstractproperty
    def protocol_parsers(self) -> list[ProtocolParser]:
        """The protocol parsers to use"""
        raise NotImplementedError()

    @abstractproperty
    def traffic_analyzers(self) -> list[TrafficAnalyzer]:
        """The traffic analyzers to use"""
        raise NotImplementedError()
