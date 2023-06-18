from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QTextBrowser
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

import logging

from ..database_handling.packet_entry import PacketEntry


class PacketDisplayWidget(QWidget):
    """Widget for displaying packets in a table and displaying the packet data in a text browser.
    """
    packet_clicked = pyqtSignal(PacketEntry)
    packet_double_clicked = pyqtSignal(PacketEntry)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.logger = logging.getLogger("GUI")

        self.layout = QVBoxLayout(self)

        self.packet_table = QTableWidget(self)
        self.packet_table.setRowCount(0)
        self.packet_table.setColumnCount(5)
        self.packet_table.setHorizontalHeaderLabels(
            ["Time", "Source", "Destination", "Protocol", "Length"]
        )
        self.packet_table.horizontalHeader().setStretchLastSection(True)
        self.packet_table.verticalHeader().setVisible(False)
        self.packet_table.setColumnWidth(0, 150)

        self.layout.addWidget(self.packet_table, 2)

        self.packet_data_layout = QHBoxLayout()
        self.UTF8_data_text = QTextBrowser()
        self.bytes_data_text = QTextBrowser()

        self.font = QFont()
        self.font.setFamily("Courier New")
        self.UTF8_data_text.setFont(self.font)
        self.bytes_data_text.setFont(self.font)

        self.packet_data_layout.addWidget(self.bytes_data_text)
        self.packet_data_layout.addWidget(self.UTF8_data_text)

        self.layout.addLayout(self.packet_data_layout, 1)

        self.setLayout(self.layout)

        self.packets: list[PacketEntry] = []

        self.packet_table.cellClicked.connect(self.on_item_clicked)
        self.packet_table.cellDoubleClicked.connect(
            self.on_item_double_clicked)

    def add_packet(self, packet: PacketEntry) -> None:
        """Add a packet to the table.

        Args:
            packet (PacketEntry): the packet to add
        """
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
        """Clear the table and the packets list.
        """
        self.packet_table.clearContents()
        self.packet_table.setRowCount(0)

    def on_item_clicked(self, row: int, column: int) -> None:
        self.logger.debug(f"clicked on row {row}, column {column}")
        self.on_packet_clicked(self.packets[row])

        self.packet_clicked.emit(self.packets[row])

    def on_item_double_clicked(self, row: int, column: int) -> None:
        self.logger.debug(f"double clicked on row {row}, column {column}")

        self.packet_double_clicked.emit(self.packets[row])

    def on_packet_clicked(self, packet: PacketEntry):
        """Display the packet data in the text browser.

        Args:
            packet (PacketEntry): the packet to display
        """
        self.bytes_data_text.setText(self._get_viewable_raw(packet))

        self.UTF8_data_text.setText(
            self._get_viewable_decrypted(packet))

    def _get_viewable_raw(self, packet: PacketEntry) -> str:
        raw_list = [f"{byte:02x}" for byte in packet.raw]
        result_list = [" ".join(raw_list[i:i+8])
                       for i in range(0, len(raw_list), 8)]
        return "\n".join(result_list)

    def _get_viewable_decrypted(self, packet: PacketEntry) -> str:
        valid_characters = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[{]}\|;:'\",<.>/?`~ ")
        raw_list = [chr(byte) if chr(
            byte) in valid_characters else "." for byte in packet.raw]
        result_list = [" ".join(raw_list[i:i+8])
                       for i in range(0, len(raw_list), 8)]
        return "\n".join(result_list)
