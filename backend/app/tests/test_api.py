import sys
from unittest.mock import MagicMock

# Mock module dependencies to allow tests to run without heavy ML libraries
sys.modules["transformers"] = MagicMock()
sys.modules["torch"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["qdrant_client"] = MagicMock()
sys.modules["redis.asyncio"] = MagicMock()

from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch

# Mock services to prevent connection errors and logic execution
@pytest.fixture(scope="module", autouse=True)
def mock_startup_dependencies():
    with patch("app.services.qdrant_service.QdrantService.init_collection") as mock_init, \
         patch("app.services.redis_service.RedisService.get_client") as mock_redis, \
         patch("app.services.owlv2_service.Owlv2Service.get_model") as mock_owl, \
         patch("app.services.siglip_service.SiglipService.get_model") as mock_siglip:
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
