from PyQt6.QtWidgets import QApplication
from src.gui_logic import MainWindow

import logging
import argparse

from src.analyses.parsers import *
from src.analyses import DDOSAnalyzer


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
        logging.FileHandler(r"logs\root.log", mode="w"))

    logger = logging.getLogger("root")

    parsers = {
        "Link": {
            "Ethernet": EthernetParser(),
        },
        "Network": {
            "IPv4": IPv4Parser(),
            "IPv6": IPv6Parser(),
        },
        "Transport": {
            "TCP": TCPParser(),
            "UDP": UDPParser(),
        },
        "Application": {
            "HTTP": HTTPParser(),
        }
    }

    analyzers = {
        "DDOS": DDOSAnalyzer
    }

    db_url = "sqlite:///packets_session.db"

    logger.info("Starting application")
    app = QApplication([])
    window = MainWindow(parsers, analyzers, db_url)
    window.show()
    app.exec()
    logger.info("Application closed")


if __name__ == "__main__":
    main()
