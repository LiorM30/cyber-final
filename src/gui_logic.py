from PyQt6 import QtWidgets, QtCore
from .GUI import Ui_MainWindow

from .widgets import FilterWidget
from .widgets import PacketWidget
from . import KnownProtocols
from . import PacketDisplayThread
from . import PacketDTO


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)

        self.active_filters = []

        self.enter_filters_button.clicked.connect(self.on_apply_filters)

        self.start_sniffing_button.clicked.connect(self.start_sniffing_clicked)
        self.stop_sniffing_button.clicked.connect(self.stop_sniffing_clicked)
        self.restart_sniffing_button.clicked.connect(
            self.restart_sniffing_clicked)

        self.start_sniffing_button.setEnabled(False)
        w = QtWidgets.QWidget()
        w.setLayout(self.filter_layout)
        self.filter_scroll.setWidget(w)

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
        w = QtWidgets.QWidget()
        w.setLayout(self.packet_layout)
        self.packet_scroll_area.setWidget(w)

        self.packet_info_layout = QtWidgets.QHBoxLayout()
        self.raw_packet_info_layout = QtWidgets.QVBoxLayout()
        self.decrypted_packet_info_layout = QtWidgets.QVBoxLayout()

        self.packet_info_layout.addLayout(self.raw_packet_info_layout)
        self.packet_info_layout.addLayout(self.decrypted_packet_info_layout)

        self.packet_display_thread = PacketDisplayThread("sqlite:///test.db")

        self.packet_display_thread.new_packets_signal.connect(
            self.on_new_packets)

        self.packet_display_thread.start()

        w = QtWidgets.QWidget()
        w.setLayout(self.packet_info_layout)
        self.packet_info_scroll.setWidget(w)
        self.packet_info_scroll.widget().setLayout(self.packet_info_layout)

        self.raw_packet_info_layout.addWidget(
            QtWidgets.QLabel("raw packet data will go here"))
        self.decrypted_packet_info_layout.addWidget(
            QtWidgets.QLabel("decoded packet data will go here"))

    def add_filter_clicked(self):
        new_filter = FilterWidget()

        new_filter.changed_type.connect(self.changed_filter_type)
        new_filter.changed_value.connect(self.changed_filter_value)

        row = self.filter_layout.count()
        self.filter_layout.insertWidget(row - 1, new_filter)

    def remove_filter_clicked(self):
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
        new_packet = PacketWidget(
            "time", "source", "destination", KnownProtocols.UDP.name, "length")
        self.packet_layout.insertWidget(0, new_packet)

    def changed_filter_type(self, filter_widget: FilterWidget):
        pass

    def changed_filter_value(self, filter_widget: FilterWidget):
        pass

    def on_apply_filters(self):
        print("apply filters")
        self.active_filters = []
        for i in range(self.filter_layout.count() - 1):
            w = self.filter_layout.itemAt(i).widget()
            self.active_filters.append(w.get_filter())

        for f in self.active_filters:
            print(f.__dict__)

        self.packet_display_thread.set_filters(self.active_filters)
        while self.packet_layout.count():
            item = self.packet_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def on_new_packets(self, packets: list[PacketDTO]):
        for packet in packets:
            new_packet = PacketWidget(
                packet.timestamp, packet.source_ip, packet.destination_ip,
                packet.protocol, packet.length
            )
            self.packet_layout.insertWidget(0, new_packet)
