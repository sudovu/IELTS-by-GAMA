"""
Knowledge Saver for IELTS by GAMA.
Saves online-researched educational knowledge into local SQLite database
and refreshes Local RAG index for instant offline availability.
"""

from typing import Dict, Any
from ..database.db_manager import DatabaseManager
from ..database.repositories import KnowledgeRepository
from ..ai.local_rag import LocalRAG


class KnowledgeSaver:
    """Persists distilled knowledge and triggers RAG index re-computation."""

    def __init__(self, db: DatabaseManager = None, rag: LocalRAG = None):
        self.db = db or DatabaseManager()
        self.knowledge_repo = KnowledgeRepository(self.db)
        self.rag = rag or LocalRAG(self.db)

    def save_distilled_knowledge(
        self,
        topic: str,
        query_trigger: str,
        compact_knowledge: str,
        subtopic: str = "Online Research",
        source: str = "online_distilled",
        confidence: float = 0.90
    ) -> Dict[str, Any]:
        result = self.knowledge_repo.upsert_knowledge(
            topic=topic,
            query_trigger=query_trigger,
            compact_knowledge=compact_knowledge,
            subtopic=subtopic,
            source=source,
            confidence=confidence,
            version="1.0.0"
        )
        # Refresh local RAG so it is immediately searchable offline
        self.rag.refresh()
        return result
