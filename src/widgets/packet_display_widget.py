from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

import logging

from ..database_handling.packet_entry import PacketEntry


class PacketDisplayWidget(QWidget):
    packet_clicked = pyqtSignal(PacketEntry)
    packet_double_clicked = pyqtSignal(PacketEntry)

    def __init__(self, parent=None, name="packet_display") -> None:
        super().__init__(parent=parent)

        self.logger = logging.getLogger("GUI")

        self.layout = QVBoxLayout(self)

        self.packet_table = QTableWidget(self)
        self.packet_table.setObjectName(name)
        self.packet_table.setRowCount(0)
        self.packet_table.setColumnCount(5)
        self.packet_table.setHorizontalHeaderLabels(
            ["Time", "Source", "Destination", "Protocol", "Length"]
        )
        self.packet_table.horizontalHeader().setStretchLastSection(True)
        self.packet_table.verticalHeader().setVisible(False)
        self.packet_table.setColumnWidth(0, 150)

        self.layout.addWidget(self.packet_table)
        self.setLayout(self.layout)

        self.packets: list[PacketEntry] = []

        self.packet_table.cellClicked.connect(self.on_item_clicked)
        self.packet_table.cellDoubleClicked.connect(
            self.on_item_double_clicked)

    def add_packet(self, packet: PacketEntry) -> None:
        last_row = self.packet_table.rowCount()
        self.packet_table.insertRow(last_row)
        self.packet_table.setItem(
            last_row, 0, self._get_uneditable_item(str(packet.timestamp)))
        self.packet_table.setItem(
            last_row, 1, self._get_uneditable_item(packet.source_ip))
        self.packet_table.setItem(
            last_row, 2, self._get_uneditable_item(packet.destination_ip))
        self.packet_table.setItem(
            last_row, 3, self._get_uneditable_item(packet.protocol))
        self.packet_table.setItem(
            last_row, 4, self._get_uneditable_item(packet.length))

        self.packets.append(packet)

    def _get_uneditable_item(cls, val: any) -> QTableWidgetItem:
        n = QTableWidgetItem(str(val))
        n.setFlags(n.flags() ^ Qt.ItemFlag.ItemIsEditable)
        return n

    def flush(self) -> None:
        self.packet_table.clearContents()
        self.packet_table.setRowCount(0)

    def on_item_clicked(self, row: int, column: int) -> None:
        self.logger.debug(f"clicked on row {row}, column {column}")

        self.packet_clicked.emit(self.packets[row])

    def on_item_double_clicked(self, row: int, column: int) -> None:
        self.logger.debug(f"double clicked on row {row}, column {column}")

        self.packet_double_clicked.emit(self.packets[row])
