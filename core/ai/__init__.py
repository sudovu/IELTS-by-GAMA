"""AI Subsystem package for IELTS by GAMA."""
from .provider_base import AIProvider, CompletionResponse
from .local_provider import LocalAIProvider
from .cloud_provider import CloudAIProvider
from .hybrid_provider import HybridAIProvider
from .task_router import TaskRouter, TaskType
from .local_rag import LocalRAG

__all__ = [
    "AIProvider",
    "CompletionResponse",
    "LocalAIProvider",
    "CloudAIProvider",
    "HybridAIProvider",
    "TaskRouter",
    "TaskType",
    "LocalRAG",
]
