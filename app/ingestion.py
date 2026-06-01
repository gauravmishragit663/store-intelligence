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
@router.get("/funnel")
def get_funnel(
    db: Session = Depends(get_db)
):

    entries = db.query(EventTable).filter(
        EventTable.event_type == "ENTRY"
    ).count()

    zone_entries = db.query(EventTable).filter(
        EventTable.event_type == "ZONE_ENTER"
    ).count()

    purchases = db.query(EventTable).filter(
        EventTable.event_type == "PURCHASE"
    ).count()

    exits = db.query(EventTable).filter(
        EventTable.event_type == "EXIT"
    ).count()

    conversion_rate = 0

    if entries > 0:
        conversion_rate = round(
            (purchases / entries) * 100,
            2
        )

    return {
        "entry_count": entries,
        "zone_enter_count": zone_entries,
        "purchase_count": purchases,
        "exit_count": exits,
        "conversion_rate": conversion_rate
    }
@router.get("/anomalies")
def get_anomalies(
    db: Session = Depends(get_db)
):

    suspicious_events = db.query(EventTable).filter(
        EventTable.dwell_ms > 300000
    ).all()

    anomalies = []

    for e in suspicious_events:
        anomalies.append({
            "visitor_id": e.visitor_id,
            "store_id": e.store_id,
            "dwell_ms": e.dwell_ms,
            "reason": "Excessive dwell time"
        })

    return {
        "anomaly_count": len(anomalies),
        "anomalies": anomalies
    }
@router.get("/heatmap")
def get_heatmap(
    db: Session = Depends(get_db)
):

    zone_stats = (
        db.query(
            EventTable.zone_id,
            func.count(EventTable.zone_id)
        )
        .filter(EventTable.zone_id != None)
        .group_by(EventTable.zone_id)
        .all()
    )

    heatmap = {}

    for zone, count in zone_stats:
        heatmap[zone] = count

    return {
        "zones": heatmap
    }