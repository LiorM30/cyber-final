import logging
from PyQt6 import QtGui, QtWidgets, QtCore
from .GUI import Ui_MainWindow

from .widgets import *
from . import KnownProtocols
from . import PacketDisplayThread
from . import PacketDTO
from .database_handling.bases import PacketEntry
from .database_handling import PacketSniffingThread


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_filter_button.clicked.connect(self.add_filter_clicked)
        self.remove_filter_button.clicked.connect(self.remove_filter_clicked)

        self.active_filters = []

        self.apply_filters_button.clicked.connect(self.on_apply_filters)

        self.start_sniffing_button.clicked.connect(self.start_sniffing_clicked)
        self.stop_sniffing_button.clicked.connect(self.stop_sniffing_clicked)
        self.restart_sniffing_button.clicked.connect(
            self.restart_sniffing_clicked)

        self.stop_sniffing_button.setEnabled(False)
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

        self.packet_display = PacketDisplayWidget(self.centralwidget)
        self.packet_display.setGeometry(QtCore.QRect(20, 80, 561, 251))
        # self.packet_layout.addWidget(self.packet_display)

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

        self.packet_sniffing_thread = PacketSniffingThread(
            interface="wlp3s0", url="sqlite:///test.db")

        self.packet_sniffing_thread.start()

        self.logger = logging.getLogger("GUI")

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
        self.logger.info("pressed start sniffing")
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)

        self.packet_sniffing_thread.start_session()

    def stop_sniffing_clicked(self):
        self.logger.info("pressed stop sniffing")
        self.start_sniffing_button.setEnabled(True)
        self.stop_sniffing_button.setEnabled(False)

        self.packet_sniffing_thread.stop_session()

    def restart_sniffing_clicked(self):
        self.logger.info("pressed restart sniffing")
        self.start_sniffing_button.setEnabled(False)
        self.stop_sniffing_button.setEnabled(True)

        self.packet_sniffing_thread.start()
        self.packet_display.flush()

    def add_packet_clicked(self):
        new_packet = PacketEntry(
            timestamp=0,
            source_ip="source",
            destination_ip="destination",
            protocol="protocol",
            length=0
        )
        self.packet_display.add_packet(new_packet)

    def changed_filter_type(self, filter_widget: FilterWidget):
        pass

    def changed_filter_value(self, filter_widget: FilterWidget):
        pass

    def on_apply_filters(self):
        self.logger.info("pressed apply filters")
        self.active_filters = []
        for i in range(self.filter_layout.count() - 1):
            w: FilterWidget = self.filter_layout.itemAt(i).widget()
            self.active_filters.append(w.get_filter())

            self.logger.debug(f"added filter: {str(w.get_filter())}")

        self.packet_display_thread.set_filters(self.active_filters)
        self.packet_display.flush()

    def on_new_packets(self, packets: list[PacketDTO]):
        for packet in packets:
            self.packet_display.add_packet(packet)

    def closeEvent(self, a0) -> None:
        self.packet_sniffing_thread.stop_session()
        return super().closeEvent(a0)
