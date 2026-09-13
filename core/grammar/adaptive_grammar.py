"""
Adaptive Grammar Generator for IELTS by GAMA.
Monitors learner error frequencies from Mistake Book and dynamically creates
personalized grammar lesson plans, drills, and quizzes without re-teaching mastered topics.
"""

from typing import Dict, Any, List
from ..database.db_manager import DatabaseManager
from ..database.repositories import MistakeBookRepository
from .grammar_engine import GrammarEngine


class AdaptiveGrammar:
    """Generates targeted grammar interventions based on recurring mistakes."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.mistake_repo = MistakeBookRepository(self.db)
        self.engine = GrammarEngine()

    def get_priority_weaknesses(self, learner_id: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Identifies active non-mastered grammatical categories needing intervention."""
        summary = self.mistake_repo.get_summary(learner_id)
        grammar_categories = [
            c for c in summary.get("categories", [])
            if c.get("skill") == "grammar" and c.get("avg_mastery", 0.0) < 0.85
        ]
        return grammar_categories[:limit]

    def generate_adaptive_session(self, learner_id: str) -> Dict[str, Any]:
        """Creates a customized lesson and exercise suite tailored to the learner's current grammar errors."""
        weaknesses = self.get_priority_weaknesses(learner_id)

        if not weaknesses:
            # Fallback to foundational IELTS high-yield topics
            target_category = "Articles"
            occurrences = 0
        else:
            target_category = weaknesses[0]["category"]
            occurrences = weaknesses[0]["total_occurrences"]

        lesson = self.engine.get_topic_lesson(target_category)

        # Retrieve recent errors in this category to construct personalized drills
        recent_mistakes = self.mistake_repo.get_mistakes(learner_id, skill="grammar", limit=5)
        category_mistakes = [m for m in recent_mistakes if m.get("category") == target_category]

        exercises = []
        for m in category_mistakes:
            exercises.append({
                "prompt": f"Correct the error: \"{m['original_text']}\"",
                "expected_answer": m["corrected_text"],
                "explanation": m["explanation"]
            })

        # Add standard rule drill if learner has few specific mistakes recorded
        if not exercises:
            exercises.append({
                "prompt": "Choose the correct sentence: (A) I am agree with your proposal. (B) I agree with your proposal.",
                "expected_answer": "B",
                "explanation": "'Agree' is a full verb that does not take the auxiliary 'am' in simple present."
            })

        return {
            "target_category": target_category,
            "recurrence_count": occurrences,
            "status": "adaptive_intervention_required" if occurrences > 0 else "foundational_review",
            "lesson": lesson,
            "drills": exercises,
            "message": f"Detected {occurrences} recurring error(s) in {target_category}. Targeted study generated."
        }
