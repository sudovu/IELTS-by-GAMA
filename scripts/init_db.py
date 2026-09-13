"""
Database Initialization and Seed Script for IELTS by GAMA.
Initializes SQLite schema, seeds starter educational curriculum,
and sets up default learner profile.
"""

import json
import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.database.db_manager import DatabaseManager
from core.database.repositories import (
    LearnerRepository,
    KnowledgeRepository,
    SRSRepository,
    SettingsRepository
)
from core.ai.local_rag import LocalRAG


def init_database(db_path: str = None) -> DatabaseManager:
    print(f"[1/4] Initializing database at: {db_path or 'default data/ielts_gama.db'}")
    db = DatabaseManager(db_path)
    db.init_schema()

    learner_repo = LearnerRepository(db)
    knowledge_repo = KnowledgeRepository(db)
    srs_repo = SRSRepository(db)
    settings_repo = SettingsRepository(db)

    print("[2/4] Setting default learner profile & preferences...")
    learner = learner_repo.get_or_create_default("default_learner", "GAMA Student")
    settings_repo.set("content_version", "1.0.0")
    settings_repo.set("auto_research", "true")
    settings_repo.set("cloud_ai_enabled", "false")  # Private by default

    print("[3/4] Seeding curated starter curriculum...")
    grammar_file = os.path.join(BASE_DIR, "content", "grammar", "core_rules.json")
    if os.path.exists(grammar_file):
        with open(grammar_file, "r", encoding="utf-8") as f:
            rules = json.load(f)
            for r in rules:
                knowledge_repo.upsert_knowledge(
                    topic=r["topic"],
                    query_trigger=r["query_trigger"],
                    compact_knowledge=r["compact_knowledge"],
                    subtopic=r.get("subtopic"),
                    source=r.get("source", "curated"),
                    confidence=r.get("confidence", 0.95),
                    version="1.0.0"
                )

    vocab_file = os.path.join(BASE_DIR, "content", "vocabulary", "academic_collocations.json")
    if os.path.exists(vocab_file):
        with open(vocab_file, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                knowledge_repo.upsert_knowledge(
                    topic=item["topic"],
                    query_trigger=item["query_trigger"],
                    compact_knowledge=item["compact_knowledge"],
                    subtopic=item.get("subtopic"),
                    source=item.get("source", "curated"),
                    confidence=item.get("confidence", 0.95),
                    version="1.0.0"
                )

    # Seed initial SRS items
    srs_repo.add_or_get_item(
        learner_id="default_learner",
        item_type="vocabulary",
        key_term="substantial",
        prompt="Define 'substantial' and provide an academic IELTS example.",
        answer="Adjective: Of considerable importance, size, or worth. Example: 'There was a substantial increase in public transport usage.'"
    )
    srs_repo.add_or_get_item(
        learner_id="default_learner",
        item_type="collocation",
        key_term="make a decision",
        prompt="Complete natural collocation: 'Citizens must _____ a decision.'",
        answer="Verb: 'make a decision' (unnatural: 'do a decision')."
    )

    print("[4/4] Building Local RAG index...")
    rag = LocalRAG(db)
    rag.refresh()

    print("[OK] IELTS by GAMA database successfully initialized and ready for offline operation!")
    return db


if __name__ == "__main__":
    init_database()
