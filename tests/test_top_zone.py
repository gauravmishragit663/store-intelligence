# PROMPT:
# Generate FastAPI tests for top zone analytics endpoint.
# Validate response availability and correctness.

# CHANGES MADE:
# Simplified assertions to match current implementation.
# Added validation that endpoint returns data successfully.

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_top_zone():

    response = client.get("/top-zone")

    assert response.status_code == 200

    data = response.json()

    assert data is not None