# Note: Don't import anything from aporia.training here, it won't work without extra dependencies
from .core.core_api import create_model_version, init, shutdown
from .model import Model

__all__ = [
    # Core
    "create_model_version",
    "init",
    "shutdown",
    # Inference
    "Model",
]
