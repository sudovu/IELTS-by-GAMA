"""
Cloud AI Provider for IELTS by GAMA.
Optional online provider for deep analysis and research synthesis when internet is active.
Strictly requires explicit user opt-in and network connectivity.
"""

import os
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from .provider_base import AIProvider, CompletionResponse
from ..sync.connectivity import ConnectivityManager


class CloudAIProvider(AIProvider):
    """Optional Cloud AI provider (e.g., Gemini API)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.connectivity = ConnectivityManager()
        self.name = "CloudAIProvider"

    def is_available(self) -> bool:
        if not self.connectivity.is_online:
            return False
        return bool(self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> CompletionResponse:
        if not self.is_available():
            raise RuntimeError("Cloud AI is unavailable (device is offline or API key is not set)")

        start_time = time.time()
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": f"{system_prompt or ''}\n\n{prompt}".strip()}]
                }
            ],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.4),
                "maxOutputTokens": kwargs.get("max_tokens", 800)
            }
        }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text = "".join([p.get("text", "") for p in parts])
                    latency_ms = int((time.time() - start_time) * 1000)
                    return CompletionResponse(
                        text=text,
                        confidence=0.97,
                        provider_name=self.name,
                        is_offline=False,
                        metadata={"latency_ms": latency_ms, "model": "gemini-1.5-flash"}
                    )
                else:
                    raise RuntimeError("No candidate received from cloud model")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Cloud request failed: {e}")
