from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch, MagicMock

# Mock services to prevent connection errors during tests
@pytest.fixture(scope="module", autouse=True)
def mock_startup_dependencies():
    with patch("app.services.qdrant_service.QdrantService.init_collection") as mock_init, \
         patch("app.services.redis_service.RedisService.get_client") as mock_redis:
        yield

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
