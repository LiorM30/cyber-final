from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTextBrowser, QMainWindow

from src.database_handling.packet_entry import PacketEntry
from . import PacketDisplayWidget, ParsedPacketViewWidget
from src.analyses import TrafficAnalyzer
from src.analyses import ProtocolParser


class AnalyzeTrafficWidget(QWidget):
    """Widget for analyzing traffic, user can select the type of analysis to perform. and the results are displayed in a PacketDisplayWidget.
    """

    def __init__(self, analyzers: dict[str, TrafficAnalyzer], db_url: str, parsers: dict[str, dict[str, ProtocolParser]], parent: QWidget = None) -> None:
        """
        Args:
            analyzers (dict[str, TrafficAnalyzer]): the analyzers to use
            db_url (str): the url to connect to the database
            parsers (dict[str, dict[str, PacketParser]]): the parsers to use for each protocol
            parent (QWidget, optional): the parent of the widget. Defaults to None.
        """
        super().__init__(parent)

        self.db_url = db_url
        self.analyzers = analyzers
        self.parsers = parsers

        self.layout = QHBoxLayout()

        self.packet_display = PacketDisplayWidget(self)

        self.analyze_types_box = QComboBox()

        for analyzer in self.analyzers:
            self.analyze_types_box.addItem(analyzer)

        self.start_button = QPushButton("Analyze")

        self.analyze_message_text = QTextBrowser()

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.analyze_types_box)
        self.left_layout.addWidget(self.start_button)
        self.left_layout.addWidget(self.analyze_message_text)

        self.layout.addLayout(self.left_layout)
        self.layout.addWidget(self.packet_display)

        self.setLayout(self.layout)

        self.current_analyzer_class = next(iter(self.analyzers.values()))
        self.current_analyzer = self.current_analyzer_class(self.db_url)

        self.start_button.clicked.connect(self.on_start_clicked)
        self.packet_display.packet_double_clicked.connect(
            self.on_packet_double_clicked)
        self.analyze_types_box.currentTextChanged.connect(
            self.on_analyze_type_changed)

    def on_analyze_type_changed(self, text: str) -> None:
        """Change the current analyzer to the one selected in the combo box.

        Args:
            text (str): the text of the selected item
        """
        self.current_analyzer_class = self.analyzers[text]

    def on_start_clicked(self) -> None:
        """Start the current analyzer.
        """
        self.current_analyzer = self.current_analyzer_class(self.db_url)
        self.current_analyzer.done_analyzing.connect(self.on_analyzer_finished)
        self.current_analyzer.start()

    def on_analyzer_finished(self, analyzer: TrafficAnalyzer) -> None:
        """Sets the text of the analyze_message_text to the result message of the analyzer and adds the result packets to the packet display.

        Args:
            analyzer (TrafficAnalyzer): the analyzer that finished
        """
        self.packet_display.flush()
        self.analyze_message_text.setText(analyzer.get_result_message())
        for packet in analyzer.get_result_packets():
            self.packet_display.add_packet(packet)

    def on_packet_double_clicked(self, packet: PacketEntry) -> None:
        """Open a new window with the parsed packet.

        Args:
            packet (PacketEntry): the packet to display
        """
        self.parsed_packet_window = QMainWindow()
        self.parsed_packet_window.setWindowTitle("Packet Info")
        self.parsed_packet_window.setCentralWidget(
            ParsedPacketViewWidget(packet, self.parsers))
        self.parsed_packet_window.show()
