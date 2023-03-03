from bases import PacketEntry

from threading import Thread
from scapy.all import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime


class PacketSniffingThread(Thread):
    def __init__(self, interface, filter, callback, url):
        super().__init__()
        self.interface = interface
        self.filter = filter
        self.callback = callback

        self.engine = create_engine(url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        PacketEntry.metadata.create_all(self.engine)

    def run(self):
        # sniff(iface=self.interface, filter=self.filter, prn=self.callback)
        while True:
            sniff(prn=self.handle_packet)

    def handle_packet(self, packet):
        print("Packet sniffed!")
        print(packet.summary())
        new_entry = self.get_entry(packet)
        self.session.add(new_entry)
        self.session.commit()

    def get_entry(self, packet: Packet):
        if IP in packet:
            new_entry = PacketEntry(
                payload=packet.payload,
                source_ip=packet[IP].src,
                source_port=packet[IP].sport,
                destination_ip=packet[IP].dst,
                destination_port=packet[IP].dport,
                protocol=packet[IP].proto.name,
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet)
            )
        else:
            new_entry = PacketEntry(
                payload=packet.payload,
                source_ip=None,
                source_port=None,
                destination_ip=None,
                destination_port=None,
                protocol=None,
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet)
            )
        print(str(new_entry))
        return new_entry
