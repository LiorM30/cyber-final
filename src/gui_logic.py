import logging
from PyQt6 import QtWidgets, QtCore
from .GUI import Ui_MainWindow

from .widgets import *
from . import PacketRetrieverThread
from .database_handling.packet_entry import PacketEntry
from .database_handling import PacketSniffingThread

from . import TrafficAnalyzer
from . import PacketParser


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parsers: dict[str, dict[str, PacketParser]], analyzers: dict[str, TrafficAnalyzer], db_url: str, parent=None):
        """Main window for the GUI.

        Args:
            parsers (dict[str, dict[str, PacketParser]]): Parsers for the different protocols.
            analyzers (dict[str, TrafficAnalyzer]): Analyzers for the different attacks.
            db_url (str): URL for the database.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent=parent)
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
        self.packet_display.setGeometry(QtCore.QRect(20, 80, 561, 400))

        self.packet_display_thread = PacketRetrieverThread(
            db_url)

        self.packet_display_thread.new_packets_signal.connect(
            self.on_new_packets)

        self.packet_display_thread.start()

        self.packet_display.packet_double_clicked.connect(
            self.on_packet_double_clicked)

        self.packet_sniffing_thread = PacketSniffingThread(
            interface="wlp3s0", url=db_url, parsers=parsers)

        self.packet_sniffing_thread.start()

        self.logger = logging.getLogger("GUI")

        self.parsers = parsers
        self.analyzers = analyzers
        self.db_url = db_url

        self.analyze_traffic_action.triggered.connect(
            self.on_analyze_traffic_clicked)

    def start_sniffing_clicked(self) -> None:
        """Starts the packet sniffing threads session.
        """
        self.logger.info("pressed start sniffing")
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)

        self.packet_sniffing_thread.start_session()

    def stop_sniffing_clicked(self) -> None:
        """Stops the packet sniffing threads session.
        """
        self.logger.info("pressed stop sniffing")
        self.start_sniffing_button.setEnabled(True)
        self.stop_sniffing_button.setEnabled(False)

        self.packet_sniffing_thread.stop_session()

    def restart_sniffing_clicked(self) -> None:
        """Restarts the packet sniffing threads session.
        """
        self.logger.info("pressed restart sniffing")
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)

        self.packet_sniffing_thread.start()
        self.packet_display.flush()

    def add_packet_clicked(self) -> None:
        """Adds a packet to the packet display for debugging purposes.
        """
        new_packet = PacketEntry(
            timestamp=0,
            source_ip="source",
            destination_ip="destination",
            protocol="protocol",
            length=3,
            raw=b"raw",
        )
        self.packet_display.add_packet(new_packet)

    def apply_filters_clicked(self) -> None:
        """Applies the filters to the packet display.
        """
        self.logger.info("pressed apply filters")
        self.packet_display_thread.apply_filter(self.filter.get_filter())
        self.packet_display.flush()

    def revert_filters_clicked(self) -> None:
        """Reverts the filters and sets the packet display to show all packets.
        """
        self.logger.info("pressed revert filters")
        self.packet_display_thread.apply_filter(None)
        self.packet_display.flush()

    def on_new_packets(self, packets: list[PacketEntry]) -> None:
        """Adds new packets to the packet display.
        """
        for packet in packets:
            self.packet_display.add_packet(packet)

    def on_packet_double_clicked(self, packet: PacketEntry) -> None:
        """Opens a new window to show the parsed packet.

        Args:
            packet (PacketEntry): Packet to show.
        """
        self.parsed_packet_window = QtWidgets.QMainWindow()
        self.parsed_packet_window.setWindowTitle("Packet Info")
        self.parsed_packet_window.setCentralWidget(
            ParsedPacketViewWidget(packet, self.parsers))
        self.parsed_packet_window.show()

    def on_analyze_traffic_clicked(self) -> None:
        """Opens a new window to analyze the traffic.
        """
        self.analyze_traffic_window = QtWidgets.QMainWindow()
        self.analyze_traffic_window.setWindowTitle("Analyze Traffic")
        self.analyze_traffic_window.setCentralWidget(
            AnalyzeTrafficWidget(self.analyzers, self.db_url, self.parsers))
        self.analyze_traffic_window.show()

    def closeEvent(self, a0) -> None:
        """Closes the window and kills the packet sniffing thread.
        """
        self.packet_sniffing_thread.kill()
        return super().closeEvent(a0)
