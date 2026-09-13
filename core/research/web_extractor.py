"""
Compact Web Knowledge Extractor for IELTS by GAMA.
Extracts concise educational summaries without downloading or hoarding full web pages.
Implements SSRF protection, strict timeout, and text sanitization.
"""

import re
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional


class WebExtractor:
    """Safely queries public educational sources and distills compact explanations."""

    def __init__(self, timeout_seconds: float = 4.0):
        self.timeout = timeout_seconds

    def _sanitize(self, raw_html: str) -> str:
        # Strip script, style, html tags, extra whitespace
        text = re.sub(r"<(script|style).*?</\1>", "", raw_html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"&[a-z]+;", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def fetch_educational_summary(self, query: str) -> Optional[Dict[str, str]]:
        """
        Queries Wikipedia / Wiktionary API for linguistic & conceptual definitions.
        Free, reliable, and completely compliant with SSRF safety (strictly restricted domain).
        """
        clean_q = re.sub(r"[^a-zA-Z0-9\s]", "", query).strip()
        if not clean_q:
            return None

        # Build safe query to Wikimedia API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(clean_q)}"
        headers = {"User-Agent": "IELTSbyGAMA-EducationalBot/1.0 (local-offline-learning)"}

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    import json
                    data = json.loads(resp.read().decode("utf-8"))
                    extract = data.get("extract", "")
                    title = data.get("title", clean_q)
                    if extract:
                        # Keep only 1-3 sentences
                        sentences = re.split(r"(?<=[.!?])\s+", extract)
                        compact = " ".join(sentences[:3])
                        return {
                            "topic": title,
                            "summary": compact,
                            "source": "Wikimedia Educational"
                        }
        except Exception:
            pass

        # If live fetch fails or is simulated, formulate a high-yield compact rule
        return self._fallback_linguistic_distill(query)

    def _fallback_linguistic_distill(self, query: str) -> Optional[Dict[str, str]]:
        """Synthesizes high-yield pedagogical distinction if network times out."""
        q_lower = query.lower()
        if "affect" in q_lower and "effect" in q_lower:
            return {
                "topic": "Affect vs Effect",
                "summary": "Affect is a verb meaning to influence ('The policy affects us'). Effect is a noun meaning the result ('The policy had an effect').",
                "source": "Linguistic Distiller"
            }
        elif "fewer" in q_lower and "less" in q_lower:
            return {
                "topic": "Fewer vs Less",
                "summary": "Use 'fewer' for countable nouns ('fewer mistakes', 'fewer cars'). Use 'less' for uncountable nouns ('less water', 'less time').",
                "source": "Linguistic Distiller"
            }
        return None
