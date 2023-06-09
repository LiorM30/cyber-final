from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6.QtCore import Qt

from . import PacketWidget
from ..database_handling.bases import PacketEntry


class PacketDisplayWidget(QWidget):

    def __init__(self, parent=None, name="packet_display") -> None:
        super().__init__(parent=parent)

        self.layout = QVBoxLayout(self)

        self.packet_table = QTableWidget()
        self.packet_table.setObjectName(name)
        self.packet_table.setRowCount(0)
        self.packet_table.setColumnCount(5)
        self.packet_table.setHorizontalHeaderLabels(
            ["Time", "Source", "Destination", "Protocol", "Length"]
        )
        self.packet_table.horizontalHeader().setStretchLastSection(True)
        self.packet_table.verticalHeader().setVisible(False)

        self.layout.addWidget(self.packet_table)
        self.setLayout(self.layout)

    def add_packet(self, packet: PacketEntry) -> None:
        last_row = self.packet_table.rowCount()
        self.packet_table.insertRow(last_row)
        self.packet_table.setItem(
            last_row, 0, QTableWidgetItem(packet.timestamp))
        self.packet_table.setItem(
            last_row, 1, QTableWidgetItem(packet.source_ip))
        self.packet_table.setItem(
            last_row, 2, QTableWidgetItem(packet.destination_ip))
        self.packet_table.setItem(
            last_row, 3, QTableWidgetItem(packet.protocol))
        self.packet_table.setItem(last_row, 4, QTableWidgetItem(packet.length))

    def flush(self) -> None:
        self.packet_table.clearContents()
        self.packet_table.setRowCount(0)
