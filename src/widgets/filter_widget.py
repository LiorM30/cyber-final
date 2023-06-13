from PyQt6 import QtWidgets, QtCore

from abc import ABC, abstractmethod

from ..database_handling import PacketFilter


# TODO: resolve metaclass problem with abstract class
class FilterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name="filter widget"):
        super().__init__(parent=parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.setLayout(self.layout)

    def get_filter(self) -> PacketFilter:
        raise NotImplementedError("Child class must implement abstract method")
