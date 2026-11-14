# -*- coding: utf-8 -*-
"""
Unified AI English & IELTS Tutor for IELTS by GAMA.
Orchestrates pedagogical dialogue, error interception, conversational practice,
persistent conversation history in SQLite, dynamic CEFR adaptation, and the core learning loop:
ASSESS -> PRACTICE -> ANALYZE -> IDENTIFY MISTAKES -> TEACH -> RETEST -> MEASURE -> ADAPT.
"""

from typing import Dict, Any, List, Optional
from ..ai.hybrid_provider import HybridAIProvider
from ..ai.task_router import TaskType
from ..memory.hot_memory import HotMemory
from ..memory.cache_manager import CacheManager
from ..research.research_planner import ResearchPlanner
from ..sync.connectivity import ConnectivityManager
from ..grammar.grammar_engine import GrammarEngine
from ..progress.mistake_book import MistakeBook
from ..database.db_manager import DatabaseManager
from ..database.repositories import LearnerRepository, AIConversationRepository


class UnifiedAITutor:
    """The central teaching intelligence of IELTS by GAMA with CEFR adaptation and persistent memory."""

    CEFR_PROFILES = {
        "A1": {
            "tone": "Beginner-Friendly & Encouraging",
            "vocab_style": "High-frequency core words, basic present/past tenses, short sentences",
            "guidance": "Explain simply with concrete real-life examples and avoid overly dense grammatical jargon."
        },
        "A2": {
            "tone": "Elementary & Clear",
            "vocab_style": "Everyday vocabulary, routine expressions, simple compound sentences",
            "guidance": "Encourage complete sentences and highlight common prepositions and verb patterns."
        },
        "B1": {
            "tone": "Intermediate & Structured",
            "vocab_style": "Standard English, modal verbs, conditionals, clear paragraphing",
            "guidance": "Introduce foundational IELTS criteria and practice coherent idea expansion."
        },
        "B2": {
            "tone": "Upper-Intermediate & Academic",
            "vocab_style": "Academic Word List (AWL), complex subordinators, varied discourse markers",
            "guidance": "Focus on Band 6.5 to 7.5 target skills: coherence, collocations, and grammatical range."
        },
        "C1": {
            "tone": "Advanced & Analytical",
            "vocab_style": "Elevated academic register, precise idiomatic phrasing, inversion, nuanced discourse",
            "guidance": "Challenge the learner with abstract arguments, sophisticated concessions, and Band 8.0+ lexical upgrades."
        },
        "C2": {
            "tone": "Mastery & Stylistic Precision",
            "vocab_style": "Flawless stylistic nuance, rhetorical devices, near-native idiomatic mastery",
            "guidance": "Refine subtle connotations, rhetorical rhythm, and examination precision."
        }
    }

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.ai = HybridAIProvider(self.db)
        self.hot_memory = HotMemory(max_turns=12)
        self.cache = CacheManager(self.db)
        self.connectivity = ConnectivityManager()
        self.research_planner = ResearchPlanner(self.db, self.ai.local_provider.rag)
        self.mistake_book = MistakeBook(self.db)
        self.learner_repo = LearnerRepository(self.db)
        self.conversation_repo = AIConversationRepository(self.db)

    def process_message(
        self,
        learner_id: str,
        user_message: str,
        context_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main interactive entry point:
        1. Persists user turn into SQLite ai_conversations and hot memory
        2. Detects linguistic errors with GrammarEngine and logs to MistakeBook
        3. Adapts pedagogical response according to learner's CEFR level
        4. Consults local knowledge / AI / RAG
        5. Triggers online research if confidence is low AND internet is available
        6. Persists tutor reply into SQLite ai_conversations
        7. Returns structured tutor reply with status indicators
        """
        self.hot_memory.add_turn(role="user", content=user_message)

        # Retrieve learner profile for CEFR adaptation
        profile = self.learner_repo.get_or_create_default(learner_id)
        cefr_level = profile.get("cefr_level", "B2")
        cefr_info = self.CEFR_PROFILES.get(cefr_level, self.CEFR_PROFILES["B2"])

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

        # Record user turn in SQLite
        self.conversation_repo.add_message(
            learner_id=learner_id,
            role="user",
            message=user_message,
            detected_errors=grammatical_errors,
            metadata={"cefr_level": cefr_level}
        )

        # Check local cache first
        cache_key = f"chat_resp_{cefr_level}_{user_message}"
        cache_hit = self.cache.get(cache_key)
        if cache_hit:
            self.hot_memory.add_turn(role="tutor", content=cache_hit["reply"])
            self.conversation_repo.add_message(
                learner_id=learner_id,
                role="tutor",
                message=cache_hit["reply"],
                metadata={"cached": True, "provider": cache_hit.get("provider", "local")}
            )
            cache_hit["cached"] = True
            return cache_hit

        # Build CEFR-adapted prompt context
        system_context = (
            f"You are the personal AI English & IELTS Tutor for a learner at CEFR level {cefr_level}.\n"
            f"Pedagogical Approach: {cefr_info['guidance']}\n"
            f"Tone & Style: {cefr_info['tone']} | Vocabulary: {cefr_info['vocab_style']}."
        )

        # Query AI (Local first)
        ai_resp = self.ai.generate(
            prompt=user_message,
            system_prompt=system_context,
            task_type=TaskType.GENERAL_CHAT
        )

        # Check if confidence warrants online research
        researched_info = None
        if self.research_planner.should_research(ai_resp.confidence):
            researched_info = self.research_planner.conduct_research_and_learn(user_message)
            if researched_info:
                # Re-query local model now that knowledge is saved locally!
                ai_resp = self.ai.local_provider.generate(
                    prompt=user_message,
                    system_prompt=system_context
                )
                ai_resp.metadata["enhanced_by_online_research"] = True

        reply_text = ai_resp.text

        # Append formative feedback if user made errors not already addressed
        if grammatical_errors and "Formative Correction" not in reply_text:
            corrections_block = "\n\n---\n**Formative Grammar Feedback:**\n" + "\n\n".join(
                [GrammarEngine.format_teach_through_correction(err) for err in grammatical_errors[:2]]
            )
            reply_text += corrections_block

        self.hot_memory.add_turn(role="tutor", content=reply_text)

        # Persist tutor turn in SQLite
        self.conversation_repo.add_message(
            learner_id=learner_id,
            role="tutor",
            message=reply_text,
            metadata={
                "provider": ai_resp.provider_name,
                "confidence": ai_resp.confidence,
                "is_offline": ai_resp.is_offline,
                "cefr_level": cefr_level
            }
        )

        result = {
            "reply": reply_text,
            "provider": ai_resp.provider_name,
            "is_offline": ai_resp.is_offline,
            "connectivity": self.connectivity.get_ui_indicator(),
            "confidence": ai_resp.confidence,
            "detected_mistakes": grammatical_errors,
            "cefr_level": cefr_level,
            "online_research_conducted": bool(researched_info),
            "cached": False
        }

        # Cache response temporarily
        self.cache.set(cache_key, result, ttl_seconds=1800, data_type="chat_completion")
        return result

    def get_conversation_history(self, learner_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves persistent chat dialogue turns from SQLite."""
        return self.conversation_repo.get_conversation_history(learner_id, limit=limit)

    def clear_conversation_history(self, learner_id: str):
        """Clears learner's dialogue history from SQLite and hot memory."""
        self.conversation_repo.clear_history(learner_id)
        self.hot_memory.clear()

    def get_greeting(self, learner_id: str) -> str:
        profile = self.learner_repo.get_or_create_default(learner_id)
        cefr = profile.get("cefr_level", "B2")
        return (
            f"Hello {profile.get('name', 'there')}! I am your AI English & IELTS Tutor.\n\n"
            f"• **Assessed CEFR Level**: {cefr} ({self.CEFR_PROFILES.get(cefr, {}).get('tone', 'Standard')})\n"
            f"• **Target**: Band {profile.get('target_band', 7.0)} ({profile.get('track', 'Academic')})\n"
            f"• **Connectivity Mode**: **{self.connectivity.get_ui_indicator()}**\n\n"
            "How can I assist your study today? Ask a grammar question, request sentence correction, "
            "explore an essay topic, or practice speaking!"
        )
