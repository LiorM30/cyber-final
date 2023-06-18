from PyQt6.QtWidgets import QWidget, QComboBox, QTextBrowser, QHBoxLayout, QVBoxLayout, QLabel


from ..database_handling import PacketEntry
from .. import ProtocolParser

from scapy.all import *


class ParsedPacketViewWidget(QWidget):
    """Widget for displaying a packets parsed data.
    """

    def __init__(self, packet: PacketEntry, parsers: dict[str, dict[str, ProtocolParser]], parent: QWidget = None):
        """
        Args:
            packet (PacketEntry): the packet to display
            parsers (dict[str, dict[str, ProtocolParser]]): the parsers to use for each protocol
        """
        super().__init__(parent=parent)

        self.packet = packet
        self.parsers = parsers

        self.layout = QHBoxLayout(self)

        self.left_layout = QVBoxLayout()
        self.protocol_label = QLabel()
        self.layer_combo_box: QComboBox = QComboBox()
        self.left_layout.addWidget(self.protocol_label)
        self.left_layout.addWidget(self.layer_combo_box)
        self.left_layout.addStretch()

        self.text_browser: QTextBrowser = QTextBrowser()

        self.layout.addLayout(self.left_layout)
        self.layout.addWidget(self.text_browser)

        self.setLayout(self.layout)

        self.layer_combo_box.currentTextChanged.connect(
            self.on_layer_combo_box_changed)

        self.layer_combo_box.addItem("Link")
        self.layer_combo_box.addItem("Network")
        self.layer_combo_box.addItem("Transport")
        self.layer_combo_box.addItem("Application")

        self.layer_combo_box.setCurrentIndex(0)

    def get_link_layer_protocol(self) -> str:
        """
        Returns:
            str: The link layer protocol of the packet. None if the packet is not a link layer packet.
        """
        for protocol, parser in self.parsers["Link"].items():
            if parser.can_parse(self.packet.scapyfy()):
                return protocol

        return None

    def get_network_layer_protocol(self) -> str:
        """
        Returns:
            str: The network layer protocol of the packet. None if the packet is not a network layer packet.
        """
        for protocol, parser in self.parsers["Network"].items():
            if parser.can_parse(self.packet.scapyfy()):
                return protocol

        return None

    def get_transport_layer_protocol(self) -> str:
        """
        Returns:
            str: The transport layer protocol of the packet. None if the packet is not a transport layer packet.
        """
        for protocol, parser in self.parsers["Transport"].items():
            if parser.can_parse(self.packet.scapyfy()):
                return protocol

        return None

    def get_application_layer_protocol(self) -> str:
        """
        Returns:
            str: The application layer protocol of the packet. None if the packet is not a supported application layer packet.
        """
        for protocol, parser in self.parsers["Application"].items():
            if parser.can_parse(self.packet.scapyfy()):
                return protocol

        return None

    def on_layer_combo_box_changed(self, text: str):
        """sets the text browser to the parsed data of the selected layer

        Args:
            text (str): the selected layer
        """
        self.text_browser.clear()

        match text:
            case "Link":
                name = self.get_link_layer_protocol()
                if name is not None:
                    self.protocol_label.setText(name)
                    self.text_browser.setText(
                        self.parsers['Link'][name].parse(self.packet.scapyfy()))
                else:
                    self.protocol_label.setText("Unsupported")
                    self.text_browser.setText(
                        "Unsupported link layer protocol")
            case "Network":
                name = self.get_network_layer_protocol()
                if name is not None:
                    self.protocol_label.setText(name)
                    self.text_browser.setText(
                        self.parsers['Network'][name].parse(self.packet.scapyfy()))
                else:
                    self.protocol_label.setText("Unsupported")
                    self.text_browser.setText(
                        "Unsupported network layer protocol")
            case "Transport":
                name = self.get_transport_layer_protocol()
                if name is not None:
                    self.protocol_label.setText(name)
                    self.text_browser.setText(
                        self.parsers['Transport'][name].parse(self.packet.scapyfy()))
                else:
                    self.protocol_label.setText("Unsupported")
                    self.text_browser.setText(
                        "Unsupported transport layer protocol")
            case "Application":
                protocol = self.get_application_layer_protocol()
                if protocol is not None:
                    self.protocol_label.setText(name)
                    self.text_browser.setText(
                        self.parsers["Application"][protocol].parse(self.packet.scapyfy()))
                else:
                    self.protocol_label.setText("Unsupported")
                    self.text_browser.setText(
                        "Unsupported application layer protocol")
            case _:
                self.text_browser.setText("Invalid layer")
