from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from .PacketSniffingThread import PacketSniffingThread


def main():
    p = PacketSniffingThread()


if __name__ == "__main__":
    main()
