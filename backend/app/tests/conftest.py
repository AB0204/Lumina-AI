"""
conftest.py - Shared test configuration and fixtures
"""
import sys
from unittest.mock import MagicMock

# Mock heavy ML dependencies before any imports
sys.modules["transformers"] = MagicMock()
sys.modules["torch"] = MagicMock()
sys.modules["PIL"] = MagicMock()
sys.modules["qdrant_client"] = MagicMock()
sys.modules["qdrant_client.models"] = MagicMock()
sys.modules["redis.asyncio"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
