from PyQt6 import QtWidgets, QtCore
from GUI import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.packet_filters = []
        self.packet_filters_group = QtWidgets.QButtonGroup()
        self.packet_filters_group.setExclusive(True)
        self.packet_filters_group.buttonClicked.connect(
            self.packet_filter_clicked)
        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)
        self.s = 0

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_widget.setLayout(self.filter_layout)

        self.scrollArea.setWidget(self.scroll_widget)
        self.scrollArea.show()

    def add_filter_clicked(self):
        self.s += 1
        self.s_status.setText(str(self.s))

        new_filter = QtWidgets.QPushButton(str(self.s))
        self.packet_filters_group.addButton(new_filter)
        self.packet_filters.append(new_filter)

        row = self.filter_layout.count()
        self.filter_layout.insertWidget(row - 1, new_filter)

    def remove_filter_clicked(self):
        self.s_status.setText(str(self.s))
        if self.filter_layout.count() > 1:
            self.filter_layout.removeWidget(self.packet_filters[-1])
            self.packet_filters_group.removeButton(self.packet_filters[-1])
            self.packet_filters.pop(-1)

    def packet_filter_clicked(self, btn):
        print("clicked: ", btn.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
