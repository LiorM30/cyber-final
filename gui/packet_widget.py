from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QMouseEvent

from known_protocls import KnownProtocols


class PacketWidget(QtWidgets.QWidget):
    def __init__(self, time: str, source: str, destination: str,
                 protocol: KnownProtocols, length: int, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QtWidgets.QLabel(time))
        self.layout.addWidget(QtWidgets.QLabel(source))
        self.layout.addWidget(QtWidgets.QLabel(destination))
        self.layout.addWidget(QtWidgets.QLabel(protocol.name))
        self.layout.addWidget(QtWidgets.QLabel(str(length)))

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print("clicked packet")
        return super().mousePressEvent(a0)
