"""
Research Planner for IELTS by GAMA.
Orchestrates the Online-to-Offline knowledge loop:
User Query -> Local RAG Confidence Check -> Online Research (if needed & online) ->
Compact Extraction -> Answer -> Save Locally -> Future Offline Availability.
"""

from typing import Dict, Any, Optional
from ..sync.connectivity import ConnectivityManager, ConnectivityState
from ..database.db_manager import DatabaseManager
from ..database.repositories import SettingsRepository
from .web_extractor import WebExtractor
from .knowledge_saver import KnowledgeSaver
from ..ai.local_rag import LocalRAG


class ResearchPlanner:
    """Plans and executes web research only when local knowledge is insufficient."""

    def __init__(self, db: DatabaseManager = None, rag: LocalRAG = None):
        self.db = db or DatabaseManager()
        self.connectivity = ConnectivityManager()
        self.settings = SettingsRepository(self.db)
        self.extractor = WebExtractor()
        self.rag = rag or LocalRAG(self.db)
        self.saver = KnowledgeSaver(self.db, self.rag)

    def should_research(self, local_confidence: float) -> bool:
        """Determines if online research is warranted."""
        if not self.connectivity.is_online:
            return False
        auto_research = self.settings.get("auto_research", "true").lower() == "true"
        if not auto_research:
            return False
        # If local confidence is below 0.65, research is helpful
        return local_confidence < 0.65

    def conduct_research_and_learn(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Executes online research, distills compact knowledge, and saves locally.
        Returns synthesized educational summary.
        """
        if not self.connectivity.is_online:
            return None

        summary_data = self.extractor.fetch_educational_summary(query)
        if not summary_data:
            return None

        topic = summary_data.get("topic", query)
        compact = summary_data.get("summary", "")
        source = summary_data.get("source", "Online Research")

        # Save into SQLite for future offline use
        saved_record = self.saver.save_distilled_knowledge(
            topic=topic,
            query_trigger=query.lower().strip(),
            compact_knowledge=compact,
            subtopic="Researched Concept",
            source=source,
            confidence=0.92
        )

        return {
            "topic": topic,
            "compact_knowledge": compact,
            "source": source,
            "record": saved_record,
            "future_offline_ready": True
        }
