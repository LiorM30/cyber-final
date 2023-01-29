from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import turtle

def main():
    app = QApplication([])
    Form, Window = uic.loadUiType("GUI.ui")
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
