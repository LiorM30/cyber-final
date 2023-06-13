from PyQt6.QtWidgets import QWidget, QComboBox, QTextBrowser, QHBoxLayout


from ..database_handling.bases import PacketEntry


import struct
from socket import inet_ntoa
from scapy.all import *


class ParsedPacketViewWidget(QWidget):
    def __init__(self, packet: PacketEntry, parent: QWidget = None):
        super().__init__(parent=parent)

        self.packet = packet

        self.layout = QHBoxLayout(self)

        self.layer_combo_box: QComboBox = QComboBox()
        self.text_browser: QTextBrowser = QTextBrowser()

        self.layout.addWidget(self.layer_combo_box)
        self.layout.addWidget(self.text_browser)

        self.setLayout(self.layout)

        self.layer_combo_box.currentTextChanged.connect(
            self.on_layer_combo_box_changed)

        self.layer_combo_box.addItem("Link")
        self.layer_combo_box.addItem("Network")
        self.layer_combo_box.addItem("Transport")
        self.layer_combo_box.addItem("Application")

        self.layer_combo_box.setCurrentIndex(0)

    def on_layer_combo_box_changed(self, text: str):
        self.text_browser.clear()

        match text:
            case "Link":
                self.text_browser.setText(self.parse_ip_layer(self.packet))
            case "Network":
                self.text_browser.setText("network")
            case "Transport":
                self.text_browser.setText("Transport")
            case "Application":
                self.text_browser.setText("Application")
            case _:
                self.text_browser.setText("Invalid layer")

    def create_scapy_packet(cls, raw_bytes):
        # Create a Scapy Ethernet packet object
        ether_packet = Ether(raw_bytes)

        # Create a Scapy IP packet object
        ip_packet = ether_packet[IP]

        # If the raw bytes contain additional payload beyond the IP layer,
        # you can append it to the packet using the Raw layer
        if len(raw_bytes) > len(ether_packet):
            payload = raw_bytes[len(ether_packet):]
            scapy_packet = ip_packet / Raw(payload)
        else:
            scapy_packet = ip_packet

        return scapy_packet

    def parse_ip_layer(self, packet: PacketEntry):
        raw_bytes = packet.raw
        ip_layer = self.create_scapy_packet(raw_bytes).getlayer(IP)
        return f"Version: {ip_layer.version}\n" \
            f"IP Header Length: {ip_layer.ihl * 4}\n" \
            f"TOS: {ip_layer.tos}\n" \
            f"Length: {ip_layer.len}\n" \
            f"ID: {ip_layer.id}\n" \
            f"Flags: {ip_layer.flags}\n" \
            f"Fragment Offset: {ip_layer.frag}\n" \
            f"TTL: {ip_layer.ttl}\n" \
            f"Protocol: {ip_layer.proto}\n" \
            f"Source Address: {ip_layer.src}\n" \
            f"Destination Address: {ip_layer.dst}\n"
