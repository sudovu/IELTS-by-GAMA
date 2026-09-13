"""
Hybrid AI Provider for IELTS by GAMA.
Orchestrates seamless cooperation between LocalAIProvider and optional CloudAIProvider.
Strictly adheres to the Local-First Principle.
"""

from typing import Optional, Dict, Any
from .provider_base import AIProvider, CompletionResponse
from .local_provider import LocalAIProvider
from .cloud_provider import CloudAIProvider
from .task_router import TaskRouter, TaskType
from ..sync.connectivity import ConnectivityManager
from ..database.db_manager import DatabaseManager
from ..database.repositories import SettingsRepository


class HybridAIProvider(AIProvider):
    """Hybrid AI Provider with smart routing and fault-tolerant local fallback."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.local_provider = LocalAIProvider(self.db)
        self.cloud_provider = CloudAIProvider()
        self.connectivity = ConnectivityManager()
        self.settings = SettingsRepository(self.db)
        self.name = "HybridAIProvider"

    def is_available(self) -> bool:
        # Local provider is always available, so hybrid is always available
        return True

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        task_type: TaskType = TaskType.GENERAL_CHAT,
        **kwargs
    ) -> CompletionResponse:
        # Step 1: Run local inference first to establish local baseline and confidence
        local_res = self.local_provider.generate(prompt, system_prompt, **kwargs)

        # Step 2: Check user preference for Cloud AI (default: OFF for privacy)
        cloud_enabled_val = self.settings.get("cloud_ai_enabled", "false").lower() == "true"

        # Step 3: Determine target via TaskRouter
        target = TaskRouter.decide_target(
            task_type=task_type,
            connectivity_state=self.connectivity.state,
            cloud_ai_enabled=cloud_enabled_val,
            local_confidence=local_res.confidence
        )

        if target == "cloud" and self.cloud_provider.is_available():
            try:
                cloud_res = self.cloud_provider.generate(prompt, system_prompt, **kwargs)
                cloud_res.metadata["routed_target"] = "cloud"
                cloud_res.metadata["local_fallback_available"] = True
                return cloud_res
            except Exception:
                # Automatic resilient fallback to local
                local_res.metadata["cloud_fallback_triggered"] = True
                return local_res

        local_res.metadata["routed_target"] = "local"
        return local_res
