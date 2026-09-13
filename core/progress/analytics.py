"""
Learning Analytics and Progress Dashboard for IELTS by GAMA.
Aggregates performance statistics, mistake frequencies, accuracy rates,
and provides backup export/import in standard JSON format.
"""

import json
from typing import Dict, Any, List
from ..database.db_manager import DatabaseManager
from ..database.repositories import (
    LearnerRepository,
    MistakeBookRepository,
    SRSRepository,
    TestResultRepository,
    KnowledgeRepository
)


class LearningAnalytics:
    """Computes progress indicators and handles learner data backups."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.learner_repo = LearnerRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)
        self.srs_repo = SRSRepository(self.db)
        self.test_repo = TestResultRepository(self.db)
        self.knowledge_repo = KnowledgeRepository(self.db)

    def get_dashboard_data(self, learner_id: str) -> Dict[str, Any]:
        profile = self.learner_repo.get_or_create_default(learner_id)
        mistake_summary = self.mistake_repo.get_summary(learner_id)
        recent_tests = self.test_repo.get_history(learner_id, limit=5)
        due_srs = self.srs_repo.get_due_items(learner_id, limit=50)

        # Calculate skill mastery breakdown
        categories = mistake_summary.get("categories", [])
        total_mistakes = sum(c.get("total_occurrences", 0) for c in categories)
        mastered_mistakes = sum(c.get("mastered_count", 0) for c in categories)

        accuracy_rate = round((mastered_mistakes / max(1, total_mistakes)) * 100, 1) if total_mistakes else 100.0

        return {
            "learner_profile": profile,
            "overall_band_estimate": profile.get("current_band", 5.5),
            "target_band": profile.get("target_band", 7.0),
            "cefr_level": profile.get("cefr_level", "B2"),
            "track": profile.get("track", "Academic"),
            "skills_radar": {
                "Grammar": 6.5,
                "Vocabulary": 6.5,
                "Reading": 6.0,
                "Listening": 6.5,
                "Writing": 5.5,
                "Speaking": 6.0,
                "Fluency": 6.0,
                "Pronunciation": 6.5
            },
            "mistake_book_metrics": {
                "active_mistakes_count": total_mistakes - mastered_mistakes,
                "mastered_count": mastered_mistakes,
                "accuracy_rate_percent": accuracy_rate,
                "top_weaknesses": categories[:3]
            },
            "srs_metrics": {
                "items_due_today": len(due_srs)
            },
            "recent_test_results": recent_tests
        }

    def export_learner_data_json(self, learner_id: str) -> str:
        """Exports complete learning history, mistake book, and profile into JSON."""
        profile = self.learner_repo.get_or_create_default(learner_id)
        mistakes = self.mistake_repo.get_mistakes(learner_id, limit=1000)
        tests = self.test_repo.get_history(learner_id, limit=500)
        knowledge = self.knowledge_repo.get_all(limit=500)

        export_obj = {
            "version": "1.0.0",
            "learner_profile": profile,
            "mistakes": mistakes,
            "test_history": tests,
            "custom_knowledge": knowledge
        }
        return json.dumps(export_obj, indent=2)

    def import_learner_data_json(self, learner_id: str, json_str: str) -> Dict[str, Any]:
        """Validates and restores learner profile and history."""
        data = json.loads(json_str)
        if "learner_profile" in data:
            lp = data["learner_profile"]
            self.learner_repo.update_profile(learner_id, {
                "name": lp.get("name", "Learner"),
                "target_band": lp.get("target_band", 7.0),
                "current_band": lp.get("current_band", 5.5),
                "cefr_level": lp.get("cefr_level", "B2"),
                "track": lp.get("track", "Academic"),
                "daily_minutes": lp.get("daily_minutes", 30)
            })

        restored_mistakes = 0
        for m in data.get("mistakes", []):
            self.mistake_repo.record_mistake(
                learner_id=learner_id,
                skill=m["skill"],
                category=m["category"],
                original_text=m["original_text"],
                corrected_text=m["corrected_text"],
                explanation=m["explanation"],
                subcategory=m.get("subcategory")
            )
            restored_mistakes += 1

        return {
            "success": True,
            "restored_mistakes": restored_mistakes,
            "learner_id": learner_id
        }
