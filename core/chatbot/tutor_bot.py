"""
Unified AI English & IELTS Tutor for IELTS by GAMA.
Orchestrates pedagogical dialogue, error interception, conversational practice,
and the core learning loop:
ASSESS -> PRACTICE -> ANALYZE -> IDENTIFY MISTAKES -> TEACH -> RETEST -> MEASURE -> ADAPT.
"""

from typing import Dict, Any, Optional
from ..ai.hybrid_provider import HybridAIProvider
from ..ai.task_router import TaskType
from ..memory.hot_memory import HotMemory
from ..memory.cache_manager import CacheManager
from ..research.research_planner import ResearchPlanner
from ..sync.connectivity import ConnectivityManager
from ..grammar.grammar_engine import GrammarEngine
from ..progress.mistake_book import MistakeBook
from ..database.db_manager import DatabaseManager
from ..database.repositories import LearnerRepository


class UnifiedAITutor:
    """The central teaching intelligence of IELTS by GAMA."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.ai = HybridAIProvider(self.db)
        self.hot_memory = HotMemory(max_turns=12)
        self.cache = CacheManager(self.db)
        self.connectivity = ConnectivityManager()
        self.research_planner = ResearchPlanner(self.db, self.ai.local_provider.rag)
        self.mistake_book = MistakeBook(self.db)
        self.learner_repo = LearnerRepository(self.db)

    def process_message(
        self,
        learner_id: str,
        user_message: str,
        context_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main interactive entry point:
        1. Adds turn to hot memory (RAM only)
        2. Detects linguistic errors in user's prompt
        3. Consults local knowledge / AI
        4. Triggers online research if confidence is low AND internet is available
        5. Returns structured tutor reply with status indicators
        """
        self.hot_memory.add_turn(role="user", content=user_message)

        # Intercept any grammatical issues
        grammatical_errors = GrammarEngine.check_sentence(user_message)
        for err in grammatical_errors:
            self.mistake_book.record_error(
                learner_id=learner_id,
                skill="grammar",
                category=err["category"],
                original_text=err["original"],
                corrected_text=err["correction"],
                explanation=err["why"]
            )

        # Check local cache first
        cache_hit = self.cache.get(f"chat_resp_{user_message}")
        if cache_hit:
            self.hot_memory.add_turn(role="tutor", content=cache_hit["text"])
            cache_hit["cached"] = True
            return cache_hit

        # Query AI (Local first)
        ai_resp = self.ai.generate(prompt=user_message, task_type=TaskType.GENERAL_CHAT)

        # Check if confidence warrants online research
        researched_info = None
        if self.research_planner.should_research(ai_resp.confidence):
            researched_info = self.research_planner.conduct_research_and_learn(user_message)
            if researched_info:
                # Re-query local model now that knowledge is saved locally!
                ai_resp = self.ai.local_provider.generate(prompt=user_message)
                ai_resp.metadata["enhanced_by_online_research"] = True

        reply_text = ai_resp.text
        self.hot_memory.add_turn(role="tutor", content=reply_text)

        result = {
            "reply": reply_text,
            "provider": ai_resp.provider_name,
            "is_offline": ai_resp.is_offline,
            "connectivity": self.connectivity.get_ui_indicator(),
            "confidence": ai_resp.confidence,
            "detected_mistakes": grammatical_errors,
            "online_research_conducted": bool(researched_info),
            "cached": False
        }

        # Cache response temporarily for fast re-turn
        self.cache.set(f"chat_resp_{user_message}", result, ttl_seconds=1800, data_type="chat_completion")
        return result

    def get_greeting(self, learner_id: str) -> str:
        profile = self.learner_repo.get_or_create_default(learner_id)
        return (
            f"Hello {profile.get('name', 'there')}! I am your AI English & IELTS Tutor.\n"
            f"Current Mode: **{self.connectivity.get_ui_indicator()}**.\n"
            f"Target: Band {profile.get('target_band', 7.0)} ({profile.get('track', 'Academic')}).\n"
            "Ask a grammar question, practice vocabulary, evaluate an essay, or start a speaking drill!"
        )
