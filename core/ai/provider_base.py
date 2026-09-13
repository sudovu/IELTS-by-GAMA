"""
AI Provider Base Interface for IELTS by GAMA.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List


@dataclass
class CompletionResponse:
    text: str
    confidence: float
    provider_name: str
    is_offline: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    sources: List[str] = field(default_factory=list)


class AIProvider(ABC):
    """Abstract base class for all AI providers."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> CompletionResponse:
        """Generates completion for a given prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Returns whether this provider is currently available."""
        pass
