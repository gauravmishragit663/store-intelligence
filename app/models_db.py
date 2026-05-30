from sqlalchemy import Column, String, Integer, Float, Boolean
from app.database import Base


class EventTable(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    store_id = Column(String)
    camera_id = Column(String)
    visitor_id = Column(String)
    event_type = Column(String)
    timestamp = Column(String)

    zone_id = Column(String, nullable=True)
    dwell_ms = Column(Integer)

    is_staff = Column(Boolean)
    confidence = Column(Float)