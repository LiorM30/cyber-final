from PyQt6 import QtWidgets, QtCore
from typing import List, Tuple
from dataclasses import dataclass

from known_protocls import KnownProtocols


@dataclass
class Filter:
    type: str
    value: str


class FilterWidget(QtWidgets.QWidget):
    changed_type = QtCore.pyqtSignal(QtWidgets.QWidget)
    changed_value = QtCore.pyqtSignal(QtWidgets.QWidget)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.type = "protocol"
        self.value = "TCP"

        self.inside_layout = QtWidgets.QHBoxLayout()
        self.inside_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        self.label = QtWidgets.QLabel("Filter:")
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.type_combo_box = QtWidgets.QComboBox()
        self.type_combo_box.addItems(["protocol", "source", "destination", "port"])
        self.value_combo_box = QtWidgets.QComboBox()
        self.value_combo_box.addItems([p.name for p in KnownProtocols])
        self.inside_layout.insertWidget(0, QtWidgets.QLabel("Filter:"))
        self.inside_layout.insertWidget(1, self.type_combo_box)
        self.inside_layout.insertWidget(2, self.value_combo_box)

        self.type_combo_box.currentIndexChanged.connect(
            self.filter_type_changed
        )
        self.value_combo_box.currentIndexChanged.connect(
            self.filter_value_changed
        )

        self.group_box = QtWidgets.QGroupBox()
        self.group_box.setLayout(self.inside_layout)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.group_box)

    def filter_type_changed(self):
        print("filter type changed: ", self.type_combo_box.currentText())
        if self.inside_layout.count() > 3:
            self.inside_layout.removeWidget(self.inside_layout.itemAt(2).widget())
        self.value_combo_box = QtWidgets.QComboBox()
        match self.type_combo_box.currentText():
            case "protocol":
                self.value_combo_box.addItems(["TCP", "UDP", "ICMP"])
            case "source":
                self.value_combo_box.addItems(['source1', 'source2', 'source3'])
            case "destination":
                self.value_combo_box.addItems(['destination1', 'destination2', 'destination3'])
            case "port":
                self.value_combo_box.addItems(['port1', 'port2', 'port3'])
        self.inside_layout.insertWidget(2, self.value_combo_box)
        self.value_combo_box.currentIndexChanged.connect(
            self.filter_value_changed
        )
        self.changed_type.emit(self)

    def filter_value_changed(self):
        print("filter value changed: ", self.value_combo_box.currentText())
        self.changed_value.emit(self)

    def get_filter(self) -> Filter:
        return Filter(self.type_combo_box.currentText(), self.value_combo_box.currentText())
