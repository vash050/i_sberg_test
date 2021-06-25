from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True)
    dev_id = Column(String(200), unique=True, index=True)
    dev_type = Column(String(120), index=True)


class EndPoint(Base):
    __tablename__ = "endpoint"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("Device.id"), onupdate='CASCADE', ondelete='CASCADE')
