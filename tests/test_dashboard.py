# PROMPT:
# Generate FastAPI tests for dashboard summary endpoint.
# Verify status code and key dashboard metrics.

# CHANGES MADE:
# Updated assertions to match dashboard API response.
# Added validation for total visitors, average dwell time,
# and most visited zone.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_summary():

    response = client.get("/dashboard-summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_visitors" in data
    assert "average_dwell_time" in data
    assert "most_visited_zone" in data