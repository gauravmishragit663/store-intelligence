from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_event = {
    "event_id": "evt_100",
    "store_id": "store_1",
    "camera_id": "cam_1",
    "visitor_id": "visitor_1",
    "event_type": "ENTRY",
    "timestamp": "2026-01-01T10:00:00",
    "zone_id": "SKINCARE",
    "dwell_ms": 5000,
    "is_staff": False,
    "confidence": 0.95,
    "metadata": {}
}


def test_ingest_event():

    response = client.post(
        "/events/ingest",
        json=test_event
    )

    assert response.status_code == 200


def test_duplicate_event():

    client.post(
        "/events/ingest",
        json=test_event
    )

    response = client.post(
        "/events/ingest",
        json=test_event
    )

    assert response.status_code == 200


def test_get_events():

    response = client.get("/events")

    assert response.status_code == 200

    data = response.json()

    assert "events" in data


def test_metrics():

    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "total_events" in data


def test_store_metrics():

    response = client.get(
        "/stores/store_1/metrics"
    )

    assert response.status_code == 200


def test_funnel():

    response = client.get("/funnel")

    assert response.status_code == 200

    data = response.json()

    assert "conversion_rate" in data


def test_anomalies():

    response = client.get("/anomalies")

    assert response.status_code == 200


def test_heatmap():

    response = client.get("/heatmap")

    assert response.status_code == 200

    data = response.json()

    assert "zones" in data