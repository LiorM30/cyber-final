from abc import ABC, abstractstaticmethod

from scapy.all import *

from .database_handling import PacketEntry


class ProtocolParser(ABC):
    """Abstract base class for protocol parsers.
    """
    @abstractstaticmethod
    def parse(cls, packet) -> str:
        """Parse the packet and return a string representation of the packet layer.

        Args:
            packet (PacketEntry): The packet to parse.

        Returns:
            str: A string representation of the packet layer.
        """
        raise NotImplementedError()

    @abstractstaticmethod
    def can_parse(cls, packet) -> bool:
        """Return True if the parser can parse the packet.

        Args:
            packet (PacketEntry): The packet to parse.

        Returns:
            bool: True if the parser can parse the packet.
        """
        raise NotImplementedError()
