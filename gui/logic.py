from PyQt6 import QtWidgets
from GUI import Ui_MainWindow
import turtle

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.czxc.clicked.connect(self.on_button_clicked)
        self.b1.clicked.connect(self.on_button_clicked)

        self.s = ""

    def on_button_clicked(self):
        self.b1.setLabel(self.s)
        self.s += "1"

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
