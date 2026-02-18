"""
API Tests - Lightweight tests that verify API routing and health.
Heavy ML dependencies are mocked via conftest.py (runs first).
"""
from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest

# Patch services BEFORE importing app to prevent startup connections
with patch("app.services.qdrant_service.QdrantService.get_client"), \
     patch("app.services.qdrant_service.QdrantService.init_collection"):
    from app.main import app

client = TestClient(app)


def test_health_check():
    """Verify the root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Lumina API"
    assert data["status"] == "active"


def test_api_docs_reachable():
    """Verify Swagger docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
