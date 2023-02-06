from PyQt6 import QtWidgets, QtCore
from GUI import Ui_MainWindow

from filter_widget import FilterWidget


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

        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_filter_clicked(self):
        self.s += 1
        self.s_status.setText(str(self.s))

        new_filter = FilterWidget()

        row = self.filter_layout.count()
        self.filter_layout.insertWidget(row - 1, new_filter)

    def remove_filter_clicked(self):
        self.s_status.setText(str(self.s))
        if self.filter_layout.count() > 1:
            self.filter_layout.removeWidget(self.filter_layout.itemAt(self.filter_layout.count() - 2).widget())

    def packet_filter_clicked(self, btn):
        print("clicked: ", btn.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
