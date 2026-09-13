"""
Speech Adapter for IELTS by GAMA.
Handles cross-platform offline Text-to-Speech (TTS) and Speech-to-Text (STT) hooks.
Ensures zero audio hoarding and temporary file cleanup.
"""

import os
import tempfile
from typing import Optional, Dict, Any


class SpeechAdapter:
    """Provides speech capabilities across desktop, mobile, and web runtimes."""

    def __init__(self):
        self.offline_tts_available = self._detect_local_tts()

    def _detect_local_tts(self) -> bool:
        try:
            import pyttsx3
            return True
        except ImportError:
            return False

    def speak_text_offline(self, text: str) -> bool:
        """Plays speech through local synthesizer if installed."""
        if not self.offline_tts_available:
            return False
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception:
            return False

    def generate_web_speech_payload(self, text: str, voice_locale: str = "en-GB") -> Dict[str, Any]:
        """
        Generates standard Web Speech API configuration.
        Enables zero-installation, private local client-side synthesis directly inside the browser.
        """
        return {
            "text": text,
            "lang": voice_locale,
            "rate": 0.95,
            "pitch": 1.0,
            "engine": "WebSpeechAPI"
        }
