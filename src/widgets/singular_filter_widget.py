from PyQt6 import QtWidgets, QtCore

from . import FilterWidget
from ..database_handling.filters import *
from ..known_protocols import KnownProtocols


class SingularFilterWidget(FilterWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.type = "protocol"
        self.value = "TCP"

        self.label = QtWidgets.QLabel("Filter:")
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.type_combo_box = QtWidgets.QComboBox()
        self.type_combo_box.addItems(
            ["protocol", "source ip", "destination ip", "source port", "destination port"])
        self.value_combo_box = QtWidgets.QComboBox()
        self.value_combo_box.addItems([p.name for p in KnownProtocols])
        self.value_text_box = QtWidgets.QLineEdit()
        self.value_text_box.setFixedWidth(100)

        self._layout.insertWidget(0, QtWidgets.QLabel("Filter:"))
        self._layout.insertWidget(1, self.type_combo_box)
        self._layout.insertWidget(2, self.value_combo_box)

        self._layout.addStretch(0)

        self.type_combo_box.currentTextChanged.connect(
            self.filter_type_changed)

    def filter_type_changed(self):
        w = self._layout.itemAt(2).widget()
        self._layout.removeWidget(w)
        w.hide()
        match self.type_combo_box.currentText():
            case "protocol":
                self.value_combo_box.show()
                self._layout.insertWidget(2, self.value_combo_box)
                self.value_combo_box.addItems(["TCP", "UDP", "ICMP"])
            case "source ip":
                self.value_text_box.show()
                self._layout.insertWidget(2, self.value_text_box)
            case "destination ip":
                self.value_text_box.show()
                self._layout.insertWidget(2, self.value_text_box)
            case "source port":
                self.value_text_box.show()
                self._layout.insertWidget(2, self.value_text_box)
            case "destination port":
                self.value_text_box.show()
                self._layout.insertWidget(2, self.value_text_box)

    def get_filter(self) -> PacketFilter:
        match self.type_combo_box.currentText():
            case "protocol":
                return ProtocolFilter(self.value_combo_box.currentText())
            case "source ip":
                return SourceIPFilter(self.value_text_box.text())
            case "destination ip":
                return DestinationIPFilter(self.value_text_box.text())
            case "source port":
                return SourcePortFilter(int(self.value_text_box.text()))
            case "destination port":
                return DestinationPortFilter(int(self.value_text_box.text()))
