from dataclasses import dataclass

from statistics import median

from . import TrafficAnalyzer
from .database_handling import PacketEntry


class DDOSAnalyzer(TrafficAnalyzer):
    """Analyze traffic for DDOS attacks"""

    def __init__(self, db_url: str):
        super().__init__(db_url)
        self.ip_table: dict[str, AddressStats] = {}

        self.interval = 1  # seconds
        self.packets_per_interval = []
        self.dpackets_per_interval = []  # derivative of packets_per_interval
        self.bytes_per_interval = []
        self.dbytes_per_interval = []  # derivative of bytes_per_interval

    def analyze(self):
        self.get_address_stats()
        self.calc_on_interval()

    def get_result_packets(self):
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

    def get_result_message(self):
        return "DDOS detected"

    def get_address_stats(self) -> None:
        for packet in self.packets:
            if packet.source_ip in self.ip_table:
                self.ip_table[packet.source_ip].sent += 1
                self.ip_table[packet.source_ip].sent_bytes += packet.length
                self.ip_table[packet.source_ip].destination_ports[packet.destination_port] += 1
            else:
                self.ip_table[packet.source_ip] = AddressStats(
                    ip=packet.source_ip,
                    sent=1,
                    received=0,
                    sent_bytes=packet.length,
                    received_bytes=0,
                    destination_ports={packet.destination_port: 1},
                )

            if packet.destination_ip in self.ip_table:
                self.ip_table[packet.destination_ip].received += 1
                self.ip_table[packet.destination_ip].received_bytes += packet.length
            else:
                self.ip_table[packet.destination_ip] = AddressStats(
                    ip=packet.destination_ip,
                    sent=0,
                    received=1,
                    sent_bytes=0,
                    received_bytes=packet.length,
                )

    def calc_on_interval(self) -> None:
        current_time = self.packets[0].timestamp.timestamp()
        for packet in self.packets:
            if packet.timestamp.timestamp() > current_time + self.interval:
                self.packets_per_interval.append(1)
                self.bytes_per_interval.append(packet.length)
            else:
                self.packets_per_interval[-1] += 1
                self.bytes_per_interval[-1] += packet.length
                current_time += self.interval

        for i in range(len(self.packets_per_interval) - 1):
            self.dpackets_per_interval.append(
                (self.packets_per_interval[i] -
                 self.packets_per_interval[i + 1]) / self.interval
            )
            self.dbytes_per_interval.append(
                (self.bytes_per_interval[i] -
                 self.bytes_per_interval[i + 1]) / self.interval
            )


@dataclass
class AddressStats:
    """Class for storing statistics about an address"""

    ip: str
    sent: int
    received: int
    sent_bytes: int
    received_bytes: int

    destination_ports: dict[int, int]
