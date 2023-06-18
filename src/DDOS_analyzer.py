from . import TrafficAnalyzer

from .database_handling import PacketEntry


class DDOSAnalyzer(TrafficAnalyzer):
    """Analyze traffic for DDOS attacks"""

    def __init__(self, db_url: str):
        super().__init__(db_url)

        self.result_packets = []
        self.result_message = ""

    def analyze(self):
        # currently just a placeholder
        self.result_packets.append(
            PacketEntry(
                id=0,
                source_ip=None,
                source_port=None,
                destination_ip=None,
                destination_port=None,
                protocol=None,
                timestamp=0,
                length=0,
                raw=b'raw'
            )
        )

        self.result_message = "DDOS detected"

    def get_result_packets(self):
        return self.result_packets

    def get_result_message(self):
        return self.result_message
