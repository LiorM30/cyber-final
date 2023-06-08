from PyQt6.QtWidgets import QApplication
from src.gui_logic import MainWindow
from src.database_handling import PacketSniffingThread


def main():
    p = PacketSniffingThread(interface="wlp3s0", url="sqlite:///test.db")
    p.start()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    p.stop()


if __name__ == "__main__":
    main()
