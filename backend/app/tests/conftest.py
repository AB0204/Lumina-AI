"""
conftest.py - Mock all heavy ML dependencies before any test imports.
This runs BEFORE any test file, ensuring modules are mocked globally.
"""
import sys
from unittest.mock import MagicMock

# Create comprehensive mocks for all heavy dependencies
# These must be set before ANY app code is imported

# PyTorch
sys.modules["torch"] = MagicMock()

# Transformers (HuggingFace)
sys.modules["transformers"] = MagicMock()

# PIL / Pillow
_pil_mock = MagicMock()
sys.modules["PIL"] = _pil_mock
sys.modules["PIL.Image"] = _pil_mock.Image

# Qdrant
_qdrant_mock = MagicMock()
sys.modules["qdrant_client"] = _qdrant_mock
sys.modules["qdrant_client.models"] = _qdrant_mock.models

# Redis
_redis_mock = MagicMock()
sys.modules["redis"] = _redis_mock
sys.modules["redis.asyncio"] = _redis_mock

# Sentence Transformers
sys.modules["sentence_transformers"] = MagicMock()

# SciPy
sys.modules["scipy"] = MagicMock()

# NumPy - keep real if available, mock otherwise
try:
    import numpy
except ImportError:
    sys.modules["numpy"] = MagicMock()
