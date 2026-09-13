"""
Personalized Mistake Book for IELTS by GAMA.
Maintains an active ledger of recurring linguistic and test-taking errors.
Drives targeted drills to eliminate persistent weaknesses.
"""

from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import MistakeBookRepository


class MistakeBook:
    """Manages learner error tracking, recurrence counting, and mastery progression."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.repo = MistakeBookRepository(self.db)

    def record_error(
        self,
        learner_id: str,
        skill: str,
        category: str,
        original_text: str,
        corrected_text: str,
        explanation: str,
        subcategory: Optional[str] = None
    ) -> Dict[str, Any]:
        return self.repo.record_mistake(
            learner_id=learner_id,
            skill=skill,
            category=category,
            original_text=original_text,
            corrected_text=corrected_text,
            explanation=explanation,
            subcategory=subcategory
        )

    def get_due_mistakes(self, learner_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns mistakes that require active review."""
        return self.repo.get_mistakes(learner_id, status="needs_improvement", limit=limit)

    def review_mistake(self, mistake_id: str, is_successful: bool) -> Dict[str, Any]:
        """Updates mastery status based on learner recall in a drill."""
        return self.repo.update_mastery(mistake_id, success=is_successful)

    def generate_review_drill(self, learner_id: str, count: int = 5) -> Dict[str, Any]:
        """Constructs interactive drill from logged mistakes."""
        mistakes = self.get_due_mistakes(learner_id, limit=count)
        drills = []
        for m in mistakes:
            drills.append({
                "mistake_id": m["id"],
                "skill": m["skill"],
                "category": m["category"],
                "prompt": f"Correct the error: \"{m['original_text']}\"",
                "correct_answer": m["corrected_text"],
                "explanation": m["explanation"],
                "occurrences": m["recurrence_count"]
            })
        return {
            "total_items": len(drills),
            "drills": drills
        }

    def get_summary_report(self, learner_id: str) -> Dict[str, Any]:
        return self.repo.get_summary(learner_id)
