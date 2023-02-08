# Form implementation generated from reading ui file '.\GUI.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        MainWindow.resize(918, 538)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.remove_filter_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_filter_button.setGeometry(QtCore.QRect(680, 310, 31, 31))
        self.remove_filter_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\icons/remove_filter_minus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.remove_filter_button.setIcon(icon)
        self.remove_filter_button.setIconSize(QtCore.QSize(31, 31))
        self.remove_filter_button.setObjectName("remove_filter_button")
        self.s_status = QtWidgets.QLabel(self.centralwidget)
        self.s_status.setGeometry(QtCore.QRect(660, 60, 47, 13))
        self.s_status.setObjectName("s_status")
        self.filter_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.filter_scroll.setGeometry(QtCore.QRect(640, 80, 231, 221))
        self.filter_scroll.setWidgetResizable(True)
        self.filter_scroll.setObjectName("filter_scroll")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 229, 219))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 231, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.filter_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_layout.setObjectName("filter_layout")
        spacerItem = QtWidgets.QSpacerItem(226, 218, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.filter_layout.addItem(spacerItem)
        self.filter_scroll.setWidget(self.scrollAreaWidgetContents_2)
        self.add_filter_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_filter_button.setGeometry(QtCore.QRect(650, 310, 31, 31))
        self.add_filter_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\icons/add_filter_plus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.add_filter_button.setIcon(icon1)
        self.add_filter_button.setIconSize(QtCore.QSize(31, 31))
        self.add_filter_button.setObjectName("add_filter_button")
        self.start_sniffing_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_sniffing_button.setGeometry(QtCore.QRect(30, 30, 31, 31))
        self.start_sniffing_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".\\icons/start_sniffing.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.start_sniffing_button.setIcon(icon2)
        self.start_sniffing_button.setIconSize(QtCore.QSize(30, 30))
        self.start_sniffing_button.setObjectName("start_sniffing_button")
        self.stop_sniffing_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_sniffing_button.setGeometry(QtCore.QRect(70, 30, 31, 31))
        self.stop_sniffing_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(".\\icons/pause_sniffing.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.stop_sniffing_button.setIcon(icon3)
        self.stop_sniffing_button.setAutoDefault(False)
        self.stop_sniffing_button.setObjectName("stop_sniffing_button")
        self.restart_sniffing_button = QtWidgets.QPushButton(self.centralwidget)
        self.restart_sniffing_button.setGeometry(QtCore.QRect(110, 30, 31, 31))
        self.restart_sniffing_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(".\\icons/restart_sniffing.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.restart_sniffing_button.setIcon(icon4)
        self.restart_sniffing_button.setObjectName("restart_sniffing_button")
        self.packet_scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.packet_scroll_area.setGeometry(QtCore.QRect(20, 80, 561, 251))
        self.packet_scroll_area.setWidgetResizable(True)
        self.packet_scroll_area.setObjectName("packet_scroll_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 559, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(-1, -1, 561, 251))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.packet_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.packet_layout.setContentsMargins(0, 0, 0, 0)
        self.packet_layout.setObjectName("packet_layout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.packet_layout.addItem(spacerItem1)
        self.packet_scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.packet_info_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.packet_info_scroll.setGeometry(QtCore.QRect(20, 350, 561, 131))
        self.packet_info_scroll.setWidgetResizable(True)
        self.packet_info_scroll.setObjectName("packet_info_scroll")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 559, 129))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.packet_info_scroll.setWidget(self.scrollAreaWidgetContents_3)
        self.add_packet_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_packet_button.setGeometry(QtCore.QRect(590, 460, 75, 23))
        self.add_packet_button.setObjectName("add_packet_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 918, 21))
        self.menubar.setObjectName("menubar")
        self.menuimport = QtWidgets.QMenu(self.menubar)
        self.menuimport.setObjectName("menuimport")
        self.menustaticstics = QtWidgets.QMenu(self.menubar)
        self.menustaticstics.setObjectName("menustaticstics")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionfile = QtGui.QAction(MainWindow)
        self.actionfile.setObjectName("actionfile")
        self.actionimport_file = QtGui.QAction(MainWindow)
        self.actionimport_file.setObjectName("actionimport_file")
        self.actionview_hierarchy = QtGui.QAction(MainWindow)
        self.actionview_hierarchy.setObjectName("actionview_hierarchy")
        self.actionvisualization = QtGui.QAction(MainWindow)
        self.actionvisualization.setObjectName("actionvisualization")
        self.menuimport.addAction(self.actionfile)
        self.menuimport.addAction(self.actionimport_file)
        self.menustaticstics.addAction(self.actionview_hierarchy)
        self.menustaticstics.addSeparator()
        self.menustaticstics.addAction(self.actionvisualization)
        self.menubar.addAction(self.menuimport.menuAction())
        self.menubar.addAction(self.menustaticstics.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WireFart"))
        self.s_status.setText(_translate("MainWindow", "TextLabel"))
        self.add_packet_button.setText(_translate("MainWindow", "add packet"))
        self.menuimport.setTitle(_translate("MainWindow", "file"))
        self.menustaticstics.setTitle(_translate("MainWindow", "staticstics"))
        self.actionfile.setText(_translate("MainWindow", "save as"))
        self.actionimport_file.setText(_translate("MainWindow", "import file"))
        self.actionview_hierarchy.setText(_translate("MainWindow", "view hierarchy"))
        self.actionvisualization.setText(_translate("MainWindow", "visualization"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
