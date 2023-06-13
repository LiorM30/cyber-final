import logging
from PyQt6 import QtWidgets, QtCore
from .GUI import Ui_MainWindow

from .widgets import *
from . import KnownProtocols
from . import PacketRetrieverThread
from .database_handling.bases import PacketEntry
from .database_handling import PacketSniffingThread


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.filter: FilterWidget = CompositeFilterWidget()
        self.filter_layout.insertWidget(0, self.filter)

        self.apply_filters_button.clicked.connect(self.apply_filters_clicked)
        self.revert_filters_button.clicked.connect(self.revert_filters_clicked)

        self.start_sniffing_button.clicked.connect(self.start_sniffing_clicked)
        self.stop_sniffing_button.clicked.connect(self.stop_sniffing_clicked)
        self.restart_sniffing_button.clicked.connect(
            self.restart_sniffing_clicked)

        self.stop_sniffing_button.setEnabled(False)

        self.filter_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        w = QtWidgets.QWidget()
        w.setLayout(self.filter_layout)
        self.filter_scroll.setWidget(w)

        self.filter_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.filter_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        self.add_packet_button.clicked.connect(self.add_packet_clicked)

        self.packet_display = PacketDisplayWidget(self.centralwidget)
        self.packet_display.setGeometry(QtCore.QRect(20, 80, 561, 251))

        self.packet_display_thread = PacketRetrieverThread("sqlite:///test.db")

        self.packet_display_thread.new_packets_signal.connect(
            self.on_new_packets)

        self.packet_display_thread.start()

        self.packet_bytes_data_text: QtWidgets.QTextBrowser = self.packet_info_scroll.findChild(
            QtWidgets.QTextBrowser, "packet_bytes_data_text")

        self.packet_UTF8_data_text: QtWidgets.QTextBrowser = self.packet_info_scroll.findChild(
            QtWidgets.QTextBrowser, "packet_UTF8_data_text")

        self.packet_display.packet_clicked.connect(
            self.on_packet_clicked)

        self.packet_display.packet_double_clicked.connect(
            self.on_packet_double_clicked)

        self.packet_sniffing_thread = PacketSniffingThread(
            interface="wlp3s0", url="sqlite:///test.db")

        self.packet_sniffing_thread.start()

        self.logger = logging.getLogger("GUI")

    def start_sniffing_clicked(self):
        self.logger.info("pressed start sniffing")
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)

        self.packet_sniffing_thread.start_session()

    def stop_sniffing_clicked(self):
        self.logger.info("pressed stop sniffing")
        self.start_sniffing_button.setEnabled(True)
        self.stop_sniffing_button.setEnabled(False)

        self.packet_sniffing_thread.stop_session()

    def restart_sniffing_clicked(self):
        self.logger.info("pressed restart sniffing")
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)

        self.packet_sniffing_thread.start()
        self.packet_display.flush()

    def add_packet_clicked(self):
        new_packet = PacketEntry(
            timestamp=0,
            source_ip="source",
            destination_ip="destination",
            protocol="protocol",
            length=3,
            raw=b"raw",
        )
        self.packet_display.add_packet(new_packet)

    def apply_filters_clicked(self):
        self.logger.info("pressed apply filters")
        self.packet_display_thread.set_filters(self.filter.get_filter())
        self.packet_display.flush()

    def revert_filters_clicked(self):
        self.logger.info("pressed revert filters")
        self.packet_display_thread.set_filters(None)
        self.packet_display.flush()

    def on_new_packets(self, packets: list[PacketEntry]):
        for packet in packets:
            self.packet_display.add_packet(packet)

    def on_packet_clicked(self, packet: PacketEntry):
        self.packet_bytes_data_text.setText(self._get_viewable_raw(packet))

        self.packet_UTF8_data_text.setText(
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

    def on_packet_double_clicked(self, packet: PacketEntry):
        self.parsed_packet_window = QtWidgets.QMainWindow()
        self.parsed_packet_window.setWindowTitle("Packet Info")
        self.parsed_packet_window.setCentralWidget(
            ParsedPacketViewWidget(packet))
        self.parsed_packet_window.show()

    def closeEvent(self, a0) -> None:
        self.packet_sniffing_thread.kill()
        return super().closeEvent(a0)
