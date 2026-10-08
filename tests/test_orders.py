from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Order Fulfillment API is running"
    }


def test_orders_endpoint_exists():
    response = client.get("/orders/")

    assert response.status_code == 200