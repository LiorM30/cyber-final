from threading import Thread
from scapy.all import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime

from .bases import PacketEntry


class PacketSniffingThread(Thread):
    def __init__(self, interface, url):
        super().__init__()
        self.interface = interface

        self.engine = create_engine(url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        PacketEntry.metadata.create_all(self.engine)

        self.session.query(PacketEntry).delete()
        self.session.commit()

        self.packet_id = 0

        self.last_commit = datetime.now()

    def run(self):
        self.running = True
        while self.running:
            sniff(1, prn=self.handle_packet)
            if (datetime.now() - self.last_commit).seconds > 0.1:
                self.session.commit()
                print("commit")
                self.last_commit = datetime.now()

    def handle_packet(self, packet):
        try:
            new_entry = self.get_entry(packet)
        except Exception as e:
            print(e)
            new_entry = PacketEntry(
                id=self.packet_id,
                payload=0,
                source_ip=None,
                source_port=None,
                destination_ip=None,
                destination_port=None,
                protocol=None,
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet)
            )
        self.session.add(new_entry)

        self.packet_id += 1

    def get_uppest_protocol(self, packet):
        while packet.payload and isinstance(packet.payload, (IP, IPv6, TCP, UDP, ICMP)):
            packet = packet.payload
        return packet.name

    def get_entry(self, packet: Packet):
        if IP in packet:  # TODO: work out the packet protocol
            new_entry = PacketEntry(
                # payload=packet.payload,
                id=self.packet_id,
                payload=0,
                source_ip=packet[IP].src,
                source_port=packet[IP].sport,
                destination_ip=packet[IP].dst,
                destination_port=packet[IP].dport,
                protocol=self.get_uppest_protocol(packet),
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet)
            )
        # elif ARP in packet:
        #     pass
        # elif ICMP in packet:
        #     pass
        else:
            new_entry = PacketEntry(
                id=self.packet_id,
                payload=0,
                source_ip=None,
                source_port=None,
                destination_ip=None,
                destination_port=None,
                protocol=self.get_uppest_protocol(packet),
                timestamp=datetime.fromtimestamp(packet.time),
                length=len(packet)
            )
        return new_entry

    def stop(self):
        self.running = False
        self.session.commit()
        self.session.close()
        print("stop")
