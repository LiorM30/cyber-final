from .bases import PacketEntry

from threading import Thread
from scapy.all import *

from sqlalchemy.orm import sessionmaker


class PacketSnifferThread(Thread):
    def __init__(self, interface, filter, callback, url):
        super().__init__()
        self.interface = interface
        self.filter = filter
        self.callback = callback

        self.engine = create_engine(url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        PacketEntry.metadata.create_all(self.engine)

    def run(self):
        # sniff(iface=self.interface, filter=self.filter, prn=self.callback)
        sniff(prn=self.handle_packet)

    def handle_packet(self, packet):
        new_entry = self.get_entry(packet)
        self.session.add(new_entry)
        self.session.commit()

    def get_entry(self, packet):
        new_entry = PacketEntry(
            source_ip=packet[IP].src,
            source_port=packet[TCP].sport,
            destination_ip=packet[IP].dst,
            destination_port=packet[TCP].dport,
            protocol=packet[IP].proto,
            timestamp=packet.time,
            length=packet.len
        )
        print(new_entry)
        return new_entry
