from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "service": "Lumina API",
        "status": "active",
        "version": "0.1.0"
    }

def test_api_docs_reachable():
    response = client.get("/docs")
    assert response.status_code == 200
