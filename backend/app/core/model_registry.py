"""
Model Registry & Upgrade Configuration
Centralizes model version management for easy A/B testing and upgrades.

Upgrade Path:
  SigLIP-base → SigLIP-Large (+15-20% retrieval accuracy)
  OWLv2 → GroundingDINO / Florence-2 (more precise detection)
  Qwen-VL → Qwen2.5-VL (better scene understanding)
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class ModelConfig:
    model_id: str
    embedding_dim: int
    description: str
    memory_gb: float

# Model Registry - swap versions without code changes
MODEL_REGISTRY: Dict[str, Dict[str, ModelConfig]] = {
    "siglip": {
        "v1": ModelConfig(
            model_id="google/siglip-base-patch16-384",
            embedding_dim=768,
            description="SigLIP Base - baseline multimodal embeddings",
            memory_gb=1.5,
        ),
        "v2": ModelConfig(
            model_id="google/siglip-large-patch16-384",
            embedding_dim=1024,
            description="SigLIP Large - 15-20% better retrieval accuracy",
            memory_gb=2.8,
        ),
    },
    "detection": {
        "v1": ModelConfig(
            model_id="google/owlv2-base-patch16-ensemble",
            embedding_dim=0,
            description="OWLv2 - zero-shot object detection",
            memory_gb=1.7,
        ),
        "v2": ModelConfig(
            model_id="IDEA-Research/grounding-dino-base",
            embedding_dim=0,
            description="GroundingDINO - more precise open-set detection",
            memory_gb=2.1,
        ),
    },
    "reranker": {
        "v1": ModelConfig(
            model_id="cross-encoder/ms-marco-MiniLM-L-6-v2",
            embedding_dim=0,
            description="MiniLM reranker - fast, general purpose",
            memory_gb=0.3,
        ),
        "v2": ModelConfig(
            model_id="BAAI/bge-reranker-large",
            embedding_dim=0,
            description="BGE reranker - higher quality, fashion-friendly",
            memory_gb=1.2,
        ),
    },
}

def get_model_config(model_type: str, version: str = "v1") -> ModelConfig:
    """Get model configuration by type and version"""
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model type: {model_type}")
    if version not in MODEL_REGISTRY[model_type]:
        raise ValueError(f"Unknown version {version} for {model_type}")
    return MODEL_REGISTRY[model_type][version]

def get_total_memory(versions: Dict[str, str] = None) -> float:
    """Calculate total GPU memory needed for a configuration"""
    if versions is None:
        versions = {"siglip": "v1", "detection": "v1", "reranker": "v1"}
    
    total = 0.0
    for model_type, version in versions.items():
        config = get_model_config(model_type, version)
        total += config.memory_gb
    return total
