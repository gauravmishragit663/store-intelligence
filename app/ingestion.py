from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import Event
from app.models_db import EventTable
from app.database import get_db

router = APIRouter()


@router.post("/events/ingest")
def ingest_event(
    event: Event,
    db: Session = Depends(get_db)
):

    db_event = EventTable(
        event_id=event.event_id,
        store_id=event.store_id,
        camera_id=event.camera_id,
        visitor_id=event.visitor_id,
        event_type=event.event_type,
        timestamp=event.timestamp,
        zone_id=event.zone_id,
        dwell_ms=event.dwell_ms,
        is_staff=event.is_staff,
        confidence=event.confidence
    )

    db.add(db_event)
    db.commit()

    return {
        "message": "Event stored successfully",
        "event_id": event.event_id
    }


@router.get("/events")
def get_events(
    db: Session = Depends(get_db)
):

    events = db.query(EventTable).all()

    return {
        "count": len(events),
        "events": [
            {
                "event_id": e.event_id,
                "store_id": e.store_id,
                "camera_id": e.camera_id,
                "visitor_id": e.visitor_id,
                "event_type": e.event_type,
                "timestamp": e.timestamp
            }
            for e in events
        ]
    }