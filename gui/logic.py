from PyQt6 import QtWidgets, QtCore
from GUI import Ui_MainWindow

from filter_widget import FilterWidget
from packet_widget import PacketWidget
from known_protocls import KnownProtocols


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.packet_filters = []
        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)
        self.s = 0

        self.start_sniffing_button.clicked.connect(self.start_sniffing_clicked)
        self.stop_sniffing_button.clicked.connect(self.stop_sniffing_clicked)
        self.restart_sniffing_button.clicked.connect(self.restart_sniffing_clicked)

        self.start_sniffing_button.setEnabled(False)

        self.filter_scroll.setWidget(QtWidgets.QWidget(self.filter_scroll))

        self.filter_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.filter_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.add_packet_button.clicked.connect(self.add_packet_clicked)

        self.packet_scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.packet_scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        w1 = QtWidgets.QWidget()
        w1.setLayout(self.packet_layout)
        self.packet_scroll_area.setWidget(w1)

        self.packet_info_layout = QtWidgets.QHBoxLayout()
        self.raw_packet_info_layout = QtWidgets.QVBoxLayout()
        self.decrypted_packet_info_layout = QtWidgets.QVBoxLayout()

        self.packet_info_layout.addLayout(self.raw_packet_info_layout)
        self.packet_info_layout.addLayout(self.decrypted_packet_info_layout)

        w2 = QtWidgets.QWidget()
        w2.setLayout(self.packet_info_layout)
        self.packet_info_scroll.setWidget(w2)
        self.packet_info_scroll.widget().setLayout(self.packet_info_layout)

        self.raw_packet_info_layout.addWidget(QtWidgets.QLabel("raw packet data will go here"))
        self.decrypted_packet_info_layout.addWidget(QtWidgets.QLabel("decoded packet data will go here"))

    def add_filter_clicked(self):
        self.s += 1
        self.s_status.setText(str(self.s))

        new_filter = FilterWidget()

        row = self.filter_layout.count()
        self.filter_layout.insertWidget(row - 1, new_filter)

    def remove_filter_clicked(self):
        self.s_status.setText(str(self.s))
        if self.filter_layout.count() > 1:
            w = self.filter_layout.itemAt(
                self.filter_layout.count() - 2
            ).widget()
            self.filter_layout.removeWidget(w)

    def start_sniffing_clicked(self):
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)
        print("start sniffing")

    def stop_sniffing_clicked(self):
        self.start_sniffing_button.setEnabled(True)
        self.stop_sniffing_button.setEnabled(False)
        print("stop sniffing")

    def restart_sniffing_clicked(self):
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)
        print("restart sniffing")

    def add_packet_clicked(self):
        new_packet = PacketWidget("time", "source", "destination", KnownProtocols.UDP, "length")
        self.packet_layout.insertWidget(0, new_packet)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
