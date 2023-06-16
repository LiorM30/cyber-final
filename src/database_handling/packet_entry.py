from scapy.all import Ether
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary

Base = declarative_base()


class PacketEntry(Base):
    __tablename__ = 'packets'

    id = Column(Integer, primary_key=True)
    source_ip = Column(String(255))
    source_port = Column(Integer)
    destination_ip = Column(String(255))
    destination_port = Column(Integer)
    protocol = Column(String(255))
    timestamp = Column(DateTime)
    length = Column(Integer)
    raw = Column(LargeBinary)

    def scapyfy(self):
        """Return the raw packet as a scapy Ether object.
        """
        return Ether(self.raw)
