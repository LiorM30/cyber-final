from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .database_handling.bases import PacketEntry
from .database_handling.filters import PacketFilter

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

    def __init__(self, url) -> None:
        super().__init__()
        self.engine = create_engine(url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.filter: PacketFilter = None
        self.new_packets: list[PacketEntry] = []
        self.displayed_packets: list[PacketEntry] = []

    def set_filters(self, filters: list[PacketFilter]) -> None:
        self.filter = filters
        self.displayed_packets = []

    def get_new_packets(self) -> list[PacketEntry]:
        """
        returns a list of new packets according to the filters
        """
        query = self.session.query(PacketEntry)
        if self.displayed_packets:
            last_packet = self.displayed_packets[-1]
            query = query.filter(PacketEntry.id > last_packet.id)

        # for filter in self.filters:
        #     query = query.filter(filter.get_filter_expression())

        if self.filter:
            query = query.filter(self.filter.get_filter_expression())

        return [packet_entry for packet_entry in query.all()]

    def run(self):
        while True:
            sleep(0.1)

            self.new_packets = self.get_new_packets()
            self.displayed_packets.extend(self.new_packets)

            self.new_packets_signal.emit(self.new_packets)
