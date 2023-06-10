from PyQt6 import QtWidgets, QtCore

from . import FilterWidget


class CompositeFilterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, name="composite_filter") -> None:
        super().__init__(parent=parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.layout = QtWidgets.QHBoxLayout(self)

        self.button_layout = QtWidgets.QVBoxLayout()

        self.filter_frame = QtWidgets.QFrame()
        self.filter_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.filter_layout = QtWidgets.QVBoxLayout(self.filter_frame)

        self.add_filter_button = QtWidgets.QPushButton("+")
        self.remove_filter_button = QtWidgets.QPushButton("-")

        self.add_filter_button.setMaximumWidth(20)
        self.add_filter_button.setMaximumHeight(20)
        self.remove_filter_button.setMaximumWidth(20)
        self.remove_filter_button.setMaximumHeight(20)

        self.button_layout.addWidget(self.add_filter_button)
        self.button_layout.addWidget(self.remove_filter_button)
        self.button_layout.addStretch(1)

        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.filter_frame)

        self.setLayout(self.layout)

        f = FilterWidget()
        self.filters = [f]
        self.filter_layout.addWidget(f)

        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)

    def add_filter_clicked(self) -> None:
        new_filter = FilterWidget()
        self.filters.append(new_filter)
        self.filter_layout.addWidget(new_filter)

    def remove_filter_clicked(self) -> None:
        if len(self.filters) > 0:
            self.filters[-1].deleteLater()
            self.filters.pop(-1)

    def get_filters(self) -> list:
        return [f.get_filter() for f in self.filters]
