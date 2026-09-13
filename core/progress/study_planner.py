"""
Personalized Study Planner for IELTS by GAMA.
Generates Daily, Weekly, and Monthly actionable study plans based on learner goals,
available daily minutes, and identified linguistic weaknesses.
"""

import datetime
from typing import Dict, Any, List
from ..database.db_manager import DatabaseManager
from ..database.repositories import LearnerRepository, MistakeBookRepository


class StudyPlanner:
    """Generates balanced, achievable preparation schedules."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.learner_repo = LearnerRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)

    def generate_daily_plan(self, learner_id: str) -> Dict[str, Any]:
        profile = self.learner_repo.get_or_create_default(learner_id)
        minutes = profile.get("daily_minutes", 30)
        target = profile.get("target_band", 7.0)
        current = profile.get("current_band", 5.5)

        summary = self.mistake_repo.get_summary(learner_id)
        top_weakness = "Grammar: Subject-Verb Agreement"
        if summary.get("categories"):
            top_cat = summary["categories"][0]
            top_weakness = f"{top_cat['skill'].capitalize()}: {top_cat['category']}"

        # Allocate daily time
        vocab_time = max(5, int(minutes * 0.25))
        drill_time = max(5, int(minutes * 0.25))
        core_time = minutes - (vocab_time + drill_time)

        tasks = [
            {
                "task_id": "task_vocab",
                "title": "Spaced Repetition Vocabulary Review",
                "duration_minutes": vocab_time,
                "description": f"Review 10-15 due vocabulary cards to reinforce Academic Word List retention."
            },
            {
                "task_id": "task_mistake_drill",
                "title": f"Targeted Weakness Drill ({top_weakness})",
                "duration_minutes": drill_time,
                "description": f"Practice 5 targeted correction exercises from your personal Mistake Book."
            },
            {
                "task_id": "task_core_practice",
                "title": "IELTS Writing / Speaking Module Practice",
                "duration_minutes": core_time,
                "description": f"Complete an Academic Task 2 essay outline or a 2-minute Speaking Part 2 cue card."
            }
        ]

        today_str = datetime.date.today().isoformat()
        return {
            "date": today_str,
            "learner_id": learner_id,
            "current_band": current,
            "target_band": target,
            "daily_minutes": minutes,
            "focus_area": top_weakness,
            "tasks": tasks,
            "daily_greeting": (
                f"Good morning! You have {minutes} minutes planned today. "
                f"Your estimated band: {current} | Target: {target}. "
                f"Today's priority: {top_weakness}. Ready to begin?"
            )
        }

    def generate_weekly_plan(self, learner_id: str) -> Dict[str, Any]:
        profile = self.learner_repo.get_or_create_default(learner_id)
        return {
            "learner_id": learner_id,
            "target_band": profile.get("target_band", 7.0),
            "weekly_schedule": [
                {"day": "Monday", "focus": "Listening Section 1 & 2 + Spelling Drills"},
                {"day": "Tuesday", "focus": "Academic Reading Skimming & Scanning + TFNG"},
                {"day": "Wednesday", "focus": "Writing Task 1 Data Reporting & Cohesion"},
                {"day": "Thursday", "focus": "Speaking Part 1 & 2 Fluency & WPM pacing"},
                {"day": "Friday", "focus": "Writing Task 2 Argumentation & Complex Grammar"},
                {"day": "Saturday", "focus": "Full Sectional Mock Test & Timed Review"},
                {"day": "Sunday", "focus": "Mistake Book Consolidation & Weekly Review"}
            ]
        }
