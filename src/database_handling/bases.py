from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class PacketEntry(Base):
    __tablename__ = 'packets'

    id = Column(Integer, primary_key=True)
    payload = Column(String(255))
    source_ip = Column(String(255))
    source_port = Column(Integer)
    destination_ip = Column(String(255))
    destination_port = Column(Integer)
    protocol = Column(String(255))
    timestamp = Column(DateTime)
    length = Column(Integer)
