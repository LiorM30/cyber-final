from abc import ABC, abstractmethod
from PyQt6.QtCore import QThread, pyqtSignal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database_handling.packet_entry import PacketEntry


class TrafficAnalyzer(QThread):
    """Abstract class for traffic analyzers"""

    # Signal emitted when a packet is parsed
    done_analyzing = pyqtSignal(object)

    def __init__(self, db_url: str):
        super().__init__()
        Session = sessionmaker(bind=create_engine(db_url, echo=False))
        self.session = Session()

        self.packets = []

    def run(self):
        self.packets = self.session.query(PacketEntry).all()

        self.analyze()
        self.done_analyzing.emit(self)

    def analyze(self):
        """Analyze the packets"""
        pass

    def get_result_packets(self):
        """Get a list of packets that are the result of the analysis"""
        pass

    def get_result_message(self):
        """Get a message describing the results of the analysis"""
        pass
