from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, Path
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

    try:
        db.add(db_event)
        db.commit()

        return {
            "message": "Event stored successfully",
            "event_id": event.event_id
        }

    except IntegrityError:
        db.rollback()

        return {
            "message": "Duplicate event ignored",
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
                "timestamp": e.timestamp,
                "zone_id": e.zone_id,
                "dwell_ms": e.dwell_ms,
                "is_staff": e.is_staff,
                "confidence": e.confidence
            }
            for e in events
        ]
    }
@router.get("/metrics")
def get_metrics(
    db: Session = Depends(get_db)
):

    total_events = db.query(EventTable).count()

    unique_visitors = db.query(
        EventTable.visitor_id
    ).distinct().count()

    entries = db.query(EventTable).filter(
        EventTable.event_type == "ENTRY"
    ).count()

    exits = db.query(EventTable).filter(
        EventTable.event_type == "EXIT"
    ).count()

    staff_events = db.query(EventTable).filter(
        EventTable.is_staff == True
    ).count()

    avg_dwell = db.query(
        func.avg(EventTable.dwell_ms)
    ).scalar()

    return {
        "total_events": total_events,
        "unique_visitors": unique_visitors,
        "entries": entries,
        "exits": exits,
        "staff_events": staff_events,
        "average_dwell_ms": avg_dwell or 0
    }

@router.get("/stores/{store_id}/metrics")
def get_store_metrics(
    store_id: str,
    db: Session = Depends(get_db)
):

    total_events = db.query(EventTable).filter(
        EventTable.store_id == store_id
    ).count()

    unique_visitors = db.query(
        EventTable.visitor_id
    ).filter(
        EventTable.store_id == store_id
    ).distinct().count()

    entries = db.query(EventTable).filter(
        EventTable.store_id == store_id,
        EventTable.event_type == "ENTRY"
    ).count()

    exits = db.query(EventTable).filter(
        EventTable.store_id == store_id,
        EventTable.event_type == "EXIT"
    ).count()

    avg_dwell = db.query(
        func.avg(EventTable.dwell_ms)
    ).filter(
        EventTable.store_id == store_id
    ).scalar()

    return {
        "store_id": store_id,
        "total_events": total_events,
        "unique_visitors": unique_visitors,
        "entries": entries,
        "exits": exits,
        "average_dwell_ms": avg_dwell or 0
    }