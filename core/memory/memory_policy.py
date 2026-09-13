"""
Memory Policy for IELTS by GAMA.
Governs which information is retained in Hot RAM, cached temporarily,
or persisted permanently in SQLite.
"""

from typing import Dict, Any, Tuple


class MemoryPolicy:
    """Enforces GAM.AI-style memory tiering and prevents data hoarding."""

    TIER_HOT = "HOT_DATA"
    TIER_CACHE = "CACHE"
    TIER_PERMANENT = "PERMANENT_KNOWLEDGE"
    TIER_DISCARD = "DISCARD"

    @classmethod
    def classify(cls, item_type: str, data: Dict[str, Any]) -> str:
        """
        Classifies incoming information:
        - Mistakes, vocabulary targets, study goals, exam results -> PERMANENT
        - Web search results, temporary exercises, transient audio -> CACHE
        - Ongoing conversation turns -> HOT
        - One-off conversational filler, raw transcripts -> DISCARD
        """
        if item_type in ["mistake", "learner_profile", "test_result", "srs_item", "curated_rule", "distilled_knowledge"]:
            return cls.TIER_PERMANENT

        if item_type in ["research_query", "temporary_exercise", "temporary_audio_metadata", "llm_completion_cache"]:
            return cls.TIER_CACHE

        if item_type in ["chat_turn", "active_timer", "in_progress_state"]:
            return cls.TIER_HOT

        return cls.TIER_DISCARD

    @classmethod
    def distill_for_permanent(cls, raw_explanation: str, max_chars: int = 400) -> str:
        """Condenses explanations to compact, high-value summaries before saving to permanent storage."""
        cleaned = " ".join(raw_explanation.strip().split())
        if len(cleaned) <= max_chars:
            return cleaned
        return cleaned[:max_chars - 3] + "..."
