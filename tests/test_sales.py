from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sales_summary():

    response = client.get("/sales-summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_orders" in data
    assert "total_sales" in data
    assert "top_brand" in data