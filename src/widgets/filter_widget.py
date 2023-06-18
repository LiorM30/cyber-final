from PyQt6 import QtWidgets, QtCore

from abc import ABC, abstractmethod

from ..database_handling import PacketFilter


# TODO: resolve metaclass problem with abc
class FilterWidget(QtWidgets.QWidget):
    """Abstract class for filter widgets.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self._layout = QtWidgets.QHBoxLayout(self)

        self.setLayout(self._layout)

    def get_filter(self) -> PacketFilter:
        """Returns the filter represented by this widget.
        """
        raise NotImplementedError("Child class must implement abstract method")
