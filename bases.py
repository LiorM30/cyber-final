from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class PacketEntry(Base):
    __tablename__ = 'packets'

    source_ip = Column(String(255), primary_key=True)
    source_port = Column(Integer, primary_key=True)
    destination_ip = Column(String(255), primary_key=True)
    destination_port = Column(Integer, primary_key=True)
    protocol = Column(String(255), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    length = Column(Integer)
