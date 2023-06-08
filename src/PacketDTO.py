from dataclasses import dataclass

from .database_handling.bases import PacketEntry


@dataclass
class PacketDTO:
    id: int
    payload: str
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int
    protocol: str
    timestamp: str
    length: int

    @classmethod
    def from_packet_entry(cls, packet_entry: PacketEntry):
        return cls(
            id=packet_entry.id,
            payload=packet_entry.payload,
            source_ip=packet_entry.source_ip,
            source_port=packet_entry.source_port,
            destination_ip=packet_entry.destination_ip,
            destination_port=packet_entry.destination_port,
            protocol=packet_entry.protocol,
            timestamp=packet_entry.timestamp.isoformat(),
            length=packet_entry.length,
        )
