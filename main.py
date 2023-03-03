from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PacketSniffingThread import PacketSniffingThread


def main():
    p = PacketSniffingThread(interface="wlp3s0", filter="tcp", callback=None, url="sqlite:///test.db")
    p.start()


if __name__ == "__main__":
    main()
