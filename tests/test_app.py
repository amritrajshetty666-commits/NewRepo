
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://test:test@localhost:5432/testdb",
)

from app import app

client = TestClient(app)


def test_health_returns_503_when_database_fails(monkeypatch):
    def fail_connection():
        raise RuntimeError("Simulated database failure")

    monkeypatch.setattr("app.get_connection", fail_connection)

    response = client.get("/api/health")

    assert response.status_code == 503
    assert response.json()["detail"] == "Database unavailable"


def test_create_order_rejects_zero_amount():
    response = client.post(
        "/api/orders",
        json={"customer_name": "Test Customer", "amount": 0},
    )

    assert response.status_code == 422


def test_create_order_rejects_missing_customer_name():
    response = client.post(
        "/api/orders",
        json={"amount": 100},
    )

    assert response.status_code == 422

