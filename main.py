from PyQt6.QtWidgets import QApplication
from src.gui_logic import MainWindow

import logging
import argparse

from src.database_handling.bases import PacketEntry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", type=int, default=10)
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s %(levelname)s %(name)s [%(filename)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    logging.getLogger("GUI").addHandler(
        logging.FileHandler(r"logs\GUI.log", mode="w"))

    logging.getLogger("database handling").addHandler(
        logging.FileHandler(r"logs\database handling.log", mode="w"))

    logging.getLogger("root").addHandler(
        logging.FileHandler(r"logs\general.log", mode="w"))

    logger = logging.getLogger("root")

    logger.info("Starting application")
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    logger.info("Application closed")


if __name__ == "__main__":
    main()
