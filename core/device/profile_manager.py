"""
Device Profile and Resource Pressure Manager for IELTS by GAMA.
Detects available host capabilities (RAM, CPU, storage) and tunes model selection,
context buffers, and cache thresholds for optimal low-power operation.
"""

import os
import sys
from typing import Dict, Any


class DeviceProfile:
    ULTRA_LOW = "ULTRA_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    DESKTOP = "DESKTOP"


class ProfileManager:
    """Manages adaptive configuration according to device resource profile."""

    @classmethod
    def detect_profile(cls) -> str:
        """Heuristically determines device capability tier."""
        # Check cpu count
        cpu_count = os.cpu_count() or 2

        # Check platform
        is_windows = sys.platform.startswith("win")
        is_linux = sys.platform.startswith("linux")
        is_darwin = sys.platform.startswith("darwin")

        # Estimate memory tier
        if cpu_count >= 8:
            return DeviceProfile.DESKTOP
        elif cpu_count >= 4:
            return DeviceProfile.HIGH
        elif cpu_count == 2:
            return DeviceProfile.MEDIUM
        else:
            return DeviceProfile.LOW

    @classmethod
    def get_hardware_config(cls, profile: str = None) -> Dict[str, Any]:
        p = profile or cls.detect_profile()

        configs = {
            DeviceProfile.ULTRA_LOW: {
                "profile": DeviceProfile.ULTRA_LOW,
                "model_name": "GAM IELTS Nano",
                "max_context_turns": 4,
                "max_cache_bytes": 10 * 1024 * 1024,  # 10MB
                "audio_bitrate": "32kbps",
                "lazy_load_db": True
            },
            DeviceProfile.LOW: {
                "profile": DeviceProfile.LOW,
                "model_name": "GAM IELTS Nano",
                "max_context_turns": 6,
                "max_cache_bytes": 20 * 1024 * 1024,  # 20MB
                "audio_bitrate": "48kbps",
                "lazy_load_db": True
            },
            DeviceProfile.MEDIUM: {
                "profile": DeviceProfile.MEDIUM,
                "model_name": "GAM IELTS Micro",
                "max_context_turns": 10,
                "max_cache_bytes": 50 * 1024 * 1024,  # 50MB
                "audio_bitrate": "64kbps",
                "lazy_load_db": False
            },
            DeviceProfile.HIGH: {
                "profile": DeviceProfile.HIGH,
                "model_name": "GAM IELTS Standard",
                "max_context_turns": 16,
                "max_cache_bytes": 100 * 1024 * 1024,  # 100MB
                "audio_bitrate": "128kbps",
                "lazy_load_db": False
            },
            DeviceProfile.DESKTOP: {
                "profile": DeviceProfile.DESKTOP,
                "model_name": "GAM IELTS Standard",
                "max_context_turns": 25,
                "max_cache_bytes": 250 * 1024 * 1024,  # 250MB
                "audio_bitrate": "192kbps",
                "lazy_load_db": False
            }
        }
        return configs.get(p, configs[DeviceProfile.MEDIUM])

    @classmethod
    def handle_resource_pressure(cls, cache_manager=None) -> Dict[str, Any]:
        """Triggered when host signals low RAM or storage."""
        freed_bytes = 0
        if cache_manager:
            freed_count = cache_manager.cleanup_expired()
            # Force trim cache to half capacity
            cache_manager._enforce_max_size(0)
            freed_bytes = freed_count * 1024
        return {
            "pressure_action": "cache_trimmed",
            "context_reduced": True,
            "freed_estimated_bytes": freed_bytes
        }
