from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .database_handling.packet_entry import PacketEntry
from .database_handling.packet_filter import PacketFilter

from time import sleep


class PacketRetrieverThread(QtCore.QThread):
    """
    workflow:\n
    once every defined interval, query the database for packets
      according to the filters

    every new packet (according to the id) will be added to the packet_layout
      as a PacketWidget

    setting new filters will remove all the current packets and start anew
    """
    new_packets_signal = pyqtSignal(list)

    def __init__(self, url: str) -> None:
        """
        Args:
            url (str): url for the database
        """
        super().__init__()
        self.engine = create_engine(url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.filter: PacketFilter = None
        self.new_packets: list[PacketEntry] = []
        self.displayed_packets: list[PacketEntry] = []

    def apply_filter(self, filter: PacketFilter) -> None:
        """apply a new filter to the thread

        Args:
            filter (PacketFilter): the new filter
        """
        self.filter = filter
        self.displayed_packets = []

    def get_new_packets(self) -> list[PacketEntry]:
        """
        returns a list of new packets according to the filters
        """
        query = self.session.query(PacketEntry)
        if self.displayed_packets:
            last_packet = self.displayed_packets[-1]
            query = query.filter(PacketEntry.id > last_packet.id)

        if self.filter:
            query = query.filter(self.filter.get_filter_expression())

        return [packet_entry for packet_entry in query.all()]

    def run(self) -> None:
        while True:
            sleep(0.1)

            self.new_packets = self.get_new_packets()
            self.displayed_packets.extend(self.new_packets)

            self.new_packets_signal.emit(self.new_packets)
