from PyQt6 import QtWidgets
from GUI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.packet_filters = []
        self.packet_filters_group = QtWidgets.QButtonGroup()
        self.packet_filters_group.setExclusive(True)
        self.packet_filters_group.buttonClicked.connect(self.packet_filter_clicked)
        self.add_packet_button.clicked.connect(self.add_packet_clicked)
        self.remove_packet_button.clicked.connect(self.remove_packet_clicked)
        self.s = 0

    def add_packet_clicked(self):
        self.s_status.setText(str(self.s))
        self.s += 1
        if self.packetlay.count() <= 5:
            new_filter = QtWidgets.QPushButton(str(self.s))
            self.packet_filters_group.addButton(new_filter)
            self.packet_filters.append(new_filter)
            self.packetlay.addWidget(new_filter)
        else:
            self.packetlay.removeWidget(self.packet_filters[0])
            self.packet_filters_group.removeButton(self.packet_filters[0])
            self.packet_filters.pop(0)

            new_filter = QtWidgets.QPushButton(str(self.s))
            self.packet_filters_group.addButton(new_filter)
            self.packet_filters.append(new_filter)
            self.packetlay.addWidget(new_filter)

        print(", ".join([i.text() for i in self.packet_filters]))

    def remove_packet_clicked(self):
        self.s_status.setText(str(self.s))
        self.s += 1
        if self.packetlay.count() != 0:
            self.packetlay.removeWidget(self.packet_filters[-1])
            self.packet_filters_group.removeButton(self.packet_filters[-1])
            self.packet_filters.pop(-1)
        print(", ".join([i.text() for i in self.packet_filters]))

    def packet_filter_clicked(self, btn):
        print("clicked: ", btn.text())



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
