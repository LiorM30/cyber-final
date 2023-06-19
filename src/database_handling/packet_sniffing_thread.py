from threading import Thread
from scapy.all import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime
from time import sleep

import logging

from . import PacketEntry
from ..analyses import ProtocolParser


class PacketSniffingThread(Thread):  # TODO: determine if QThread is better
    """Thread for sniffing packets and adding them to the database.
    """

    def __init__(self, interface: str, url: str, parsers: dict[str, dict[str, ProtocolParser]]) -> None:
        """
        Args:
            interface (str): the interface to sniff on
            url (str): the url to connect to the database
            parsers (dict[str, dict[str, PacketParser]]): the parsers to use for each protocol
        """
        super().__init__()
        self.interface = interface
        self.parsers = parsers

        self.engine = create_engine(url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        PacketEntry.metadata.create_all(self.engine)

        self.session.query(PacketEntry).delete()
        self.session.commit()

        self.packet_id = 0

        self.last_commit = datetime.now()

        self.logger = logging.getLogger("database handling")

        self.running = False
        self.killed = False

    def run(self) -> None:
        while not self.killed:
            if self.running:
                sniff(1, prn=self.handle_packet)
                if (datetime.now() - self.last_commit).seconds > 0.1:
                    self.session.commit()
                    self.logger.debug("committed to database")
                    self.last_commit = datetime.now()
            else:
                sleep(0.1)

    def handle_packet(self, packet: packet) -> None:
        """Handle a packet by adding it to the database.

        Args:
            packet (packet): the packet to handle
        """
        try:
            new_entry = self.get_entry(packet)
        except Exception as e:
            self.logger.exception(e)
            new_entry = PacketEntry(
                id=self.packet_id,
                source_ip=None,
                source_port=None,
                destination_ip=None,
                destination_port=None,
                protocol=None,
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet)
            )
        self.session.add(new_entry)

        self.packet_id += 1

    def get_uppermost_protocol(self, packet: packet) -> str:
        """Get the uppermost protocol of a packet.

        Args:
            packet (packet): the packet to get the uppermost protocol of

        Returns:
            str: the uppermost protocol of the packet
        """
        for _, parsers in list(self.parsers.items())[::-1]:
            for protocol, parser in parsers.items():
                if parser.can_parse(packet):
                    return protocol
        return packet.name

    def get_entry(self, packet: packet) -> PacketEntry:
        """Create a new PacketEntry from a packet.

        Args:
            packet (packet): the packet to get the PacketEntry from

        Returns:
            PacketEntry: the PacketEntry from the packet
        """
        if IP in packet:  # TODO: work out the packet protocol
            new_entry = PacketEntry(
                id=self.packet_id,
                source_ip=packet[IP].src,
                source_port=packet[IP].sport,
                destination_ip=packet[IP].dst,
                destination_port=packet[IP].dport,
                protocol=self.get_uppermost_protocol(packet),
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet),
                raw=bytes(packet)
            )
        else:
            new_entry = PacketEntry(
                id=self.packet_id,
                source_ip=None,
                source_port=None,
                destination_ip=None,
                destination_port=None,
                protocol=self.get_uppermost_protocol(packet),
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet),
                raw=bytes(packet)
            )
        return new_entry

    def stop_session(self) -> None:
        """Stop the current sql session.
        """
        self.running = False
        self.session.commit()
        self.session.close()
        self.logger.info("stopped current sql session")

    def start_session(self) -> None:
        """Start a new sql session.
        """
        self.running = True
        self.session = self.Session()
        self.logger.info("started new sql session")

    def kill(self) -> None:
        """Kill the thread.
        """
        self.stop_session()
        self.killed = True
        self.logger.info("killed packet sniffing thread")
