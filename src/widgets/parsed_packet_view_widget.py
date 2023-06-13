from PyQt6.QtWidgets import QWidget, QComboBox, QTextBrowser, QHBoxLayout


from ..database_handling.bases import PacketEntry


from abc import ABC, abstractmethod


class ParsedPacketViewWidget(QWidget):
    def __init__(self, parent: QWidget = None, packet: PacketEntry):
        super().__init__(parent=parent)

        self.packet = packet
        self.parser: PacketParser = None

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
                self.text_browser.setText(self.parser.get_link(self.packet))
            case "Network":
                self.text_browser.setText(self.parser.get_network(self.packet))
            case "Transport":
                self.text_browser.setText(
                    self.parser.get_transport(self.packet))
            case "Application":
                self.text_browser.setText(
                    self.parser.get_application(self.packet))
            case _:
                self.text_browser.setText("Invalid layer")


class PacketParser(ABC):
    @abstractmethod
    def get_link(self, packet: PacketEntry) -> str:
        raise NotImplementedError("child class must implement this method")

    @abstractmethod
    def get_network(self, packet: PacketEntry) -> str:
        raise NotImplementedError("child class must implement this method")

    @abstractmethod
    def get_transport(self, packet: PacketEntry) -> str:
        raise NotImplementedError("child class must implement this method")

    @abstractmethod
    def get_application(self, packet: PacketEntry) -> str:
        raise NotImplementedError("child class must implement this method")
