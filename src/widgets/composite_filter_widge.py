from __future__ import annotations

from PyQt6 import QtWidgets, QtCore

from . import SingularFilterWidget


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
        self.filter_layout.setSpacing(0)

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

        self.filters = []

        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)

        self.add_filter()

    def add_filter_clicked(self) -> None:
        self.add_filter()

    def remove_filter_clicked(self) -> None:
        if len(self.filters) > 0:
            self.filters[-1].deleteLater()
            self.filters.pop(-1)

    def toggle_composite_clicked(self, filter_layout: QtWidgets.QHBoxLayout) -> None:
        if isinstance(filter_layout.itemAt(1).widget(), CompositeFilterWidget):
            print("composite")
            reg_filter = SingularFilterWidget()
            filter_layout.itemAt(1).widget().deleteLater()
            filter_layout.insertWidget(1, reg_filter)
        else:
            print("reg")
            composite_filter = CompositeFilterWidget()
            filter_layout.itemAt(1).widget().deleteLater()
            filter_layout.insertWidget(1, composite_filter)

    def add_filter(self) -> None:
        new_filter_layout = QtWidgets.QHBoxLayout()
        toggle_composite_button = QtWidgets.QPushButton("[")
        toggle_composite_button.setMaximumWidth(10)
        toggle_composite_button.setMaximumHeight(25)

        new_filter_layout.addWidget(toggle_composite_button)
        f = SingularFilterWidget()
        self.filters.append(f)
        new_filter_layout.addWidget(f)

        self.filter_layout.addLayout(new_filter_layout)

        toggle_composite_button.clicked.connect(
            lambda: self.toggle_composite_clicked(new_filter_layout)
        )

    def get_filters(self) -> list:
        return [f.get_filter() for f in self.filters]
