from __future__ import annotations

from PyQt6 import QtWidgets, QtCore

from . import SingularFilterWidget, FilterWidget
from ..database_handling import PacketFilter
from ..database_handling.filters import CompoundFilter


class CompositeFilterWidget(FilterWidget):
    def __init__(self, parent=None, name="composite_filter") -> None:
        super().__init__(parent=parent)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

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
        self.button_layout.addStretch(0)

        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.filter_frame)
        self.layout.addStretch(0)

        self.setLayout(self.layout)

        self.filters: list[FilterWidget] = []
        self.operators: list[QtWidgets.QComboBox] = []

        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)

        self.add_filter()

    def add_filter_clicked(self) -> None:
        self.add_filter()

    def remove_filter_clicked(self) -> None:
        if len(self.filters) > 1:
            l = self.filter_layout.itemAt(
                self.filter_layout.count() - 1).layout()

            while l.count():
                l.takeAt(0).widget().deleteLater()

            l.deleteLater()

            self.filters.pop(-1)

            if self.operators:
                self.operators[-1].deleteLater()
                self.operators.pop(-1)

    def toggle_composite_clicked(self, filter_layout: QtWidgets.QHBoxLayout) -> None:
        self.filters.remove(filter_layout.itemAt(1).widget())

        if isinstance(filter_layout.itemAt(1).widget(), CompositeFilterWidget):
            reg_filter = SingularFilterWidget()
            filter_layout.itemAt(1).widget().deleteLater()
            filter_layout.insertWidget(1, reg_filter)
            self.filters.append(reg_filter)
        else:
            composite_filter = CompositeFilterWidget()
            filter_layout.itemAt(1).widget().deleteLater()
            filter_layout.insertWidget(1, composite_filter)
            self.filters.append(composite_filter)

    def add_filter(self) -> None:
        new_filter_layout = QtWidgets.QHBoxLayout()
        toggle_composite_button = QtWidgets.QPushButton("[")
        toggle_composite_button.setMaximumWidth(10)
        toggle_composite_button.setMaximumHeight(25)

        new_filter_layout.addWidget(toggle_composite_button)
        f = SingularFilterWidget()
        self.filters.append(f)
        new_filter_layout.addWidget(f)

        if self.filter_layout.count() > 0:
            operator_combo_box = QtWidgets.QComboBox()
            operator_combo_box.addItems(["AND", "OR"])
            operator_combo_box.setMaximumWidth(50)
            self.filter_layout.addWidget(operator_combo_box)
            self.operators.append(operator_combo_box)

        self.filter_layout.addLayout(new_filter_layout)

        toggle_composite_button.clicked.connect(
            lambda: self.toggle_composite_clicked(new_filter_layout)
        )

    def get_filter(self) -> PacketFilter:
        compound_filter = CompoundFilter(self.filters[0].get_filter())
        for operator, f in zip(self.operators, self.filters[1:]):
            if operator.currentText() == "AND":
                compound_filter.AND(f.get_filter())
            elif operator.currentText() == "OR":
                compound_filter.OR(f.get_filter())
        return compound_filter
