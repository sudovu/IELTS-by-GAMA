# -*- coding: utf-8 -*-
"""
Personalized Study Planner for IELTS by GAMA.
Generates Daily, Weekly, and Adaptive Multi-Week actionable study plans based on learner goals,
target examination date, available daily minutes, and identified linguistic weaknesses.
"""

import datetime
from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import LearnerRepository, MistakeBookRepository, SRSRepository, CurriculumRepository
from .analytics import LearningAnalytics


class StudyPlanner:
    """Generates balanced, achievable preparation schedules adapted to learner diagnostic records."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.learner_repo = LearnerRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)
        self.srs_repo = SRSRepository(self.db)
        self.curriculum_repo = CurriculumRepository(self.db)
        self.analytics = LearningAnalytics(self.db)

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
                "description": "Review 10-15 due vocabulary cards to reinforce Academic Word List retention."
            },
            {
                "task_id": "task_mistake_drill",
                "title": f"Targeted Weakness Drill ({top_weakness})",
                "duration_minutes": drill_time,
                "description": "Practice 5 targeted correction exercises from your personal Mistake Book."
            },
            {
                "task_id": "task_core_practice",
                "title": "IELTS Writing / Speaking Module Practice",
                "duration_minutes": core_time,
                "description": "Complete an Academic Task 2 essay outline or a 2-minute Speaking Part 2 cue card."
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

    def generate_adaptive_study_plan(self, learner_id: str) -> Dict[str, Any]:
        """
        Synthesizes actual assessment metrics, SRS load, and target exam deadlines
        into an adaptive multi-week study roadmap.
        """
        profile = self.learner_repo.get_or_create_default(learner_id)
        target_band = profile.get("target_band", 7.0)
        current_band = profile.get("current_band", 5.5)
        cefr_level = profile.get("cefr_level", "B2")
        daily_minutes = profile.get("daily_minutes", 30)
        track = profile.get("track", "Academic")
        exam_date_str = profile.get("target_exam_date")

        days_remaining = None
        if exam_date_str:
            try:
                target_dt = datetime.date.fromisoformat(exam_date_str.split("T")[0])
                delta = (target_dt - datetime.date.today()).days
                days_remaining = max(1, delta)
            except Exception:
                days_remaining = 60

        dash = self.analytics.get_dashboard_data(learner_id)
        radar = dash.get("skills_radar", {})
        radar_lower = {str(k).lower(): float(v) for k, v in radar.items()}

        # Identify weakest sub-skill
        skill_scores = {
            "listening": radar_lower.get("listening", 6.0),
            "reading": radar_lower.get("reading", 6.0),
            "writing": radar_lower.get("writing", 6.0),
            "speaking": radar_lower.get("speaking", 6.0)
        }
        weakest_skill = min(skill_scores, key=skill_scores.get)

        # Due SRS cards
        due_cards = self.srs_repo.get_due_items(learner_id)
        due_count = len(due_cards)

        # Incomplete lessons for CEFR level
        all_lessons = self.curriculum_repo.list_lessons(cefr_level=cefr_level)
        learner_progress = self.curriculum_repo.get_learner_progress(learner_id)
        completed_ids = set(p["lesson_id"] for p in learner_progress if p.get("status") == "completed")
        pending_lessons_count = max(0, len(all_lessons) - len(completed_ids))

        band_gap = round(max(0.0, target_band - current_band), 1)

        # Strategy narrative
        strategy_summary = (
            f"To advance from Band {current_band} to Band {target_band} in {track} track, "
            f"your highest-priority focus is {weakest_skill.upper()} (current score: {skill_scores[weakest_skill]}). "
            f"You have {due_count} flashcard(s) due for recall and {pending_lessons_count} curriculum lesson(s) pending for level {cefr_level}."
        )

        milestones = [
            {
                "phase": "Phase 1: Remediation & Error Elimination",
                "duration": "Weeks 1–2",
                "core_objective": f"Eliminate recurring mistakes in {weakest_skill.capitalize()} and consolidate level {cefr_level} grammar.",
                "weekly_hours": round((daily_minutes * 7) / 60.0, 1),
                "milestone_check": "Achieve 85% accuracy on targeted Mistake Book review drills."
            },
            {
                "phase": "Phase 2: Exam Technique & Sectional Mastery",
                "duration": "Weeks 3–4",
                "core_objective": f"Timed sectional practice in {track} Reading, Listening distractor analysis, and Writing structure.",
                "weekly_hours": round((daily_minutes * 7) / 60.0, 1),
                "milestone_check": f"Score at least Band {min(target_band, current_band + 0.5)} on two consecutive practice sections."
            },
            {
                "phase": "Phase 3: High-Band Lexical Precision & Speed",
                "duration": "Weeks 5–6",
                "core_objective": "Integrate Band 8 Academic Word List collocations, formal letters/graphs, and fluent speaking turns.",
                "weekly_hours": round((daily_minutes * 7) / 60.0, 1),
                "milestone_check": f"Maintain WPM pacing of 130–150 and complete Writing Task 2 within 40 minutes."
            },
            {
                "phase": "Phase 4: Examination Simulation & Peak Performance",
                "duration": "Final 2 Weeks",
                "core_objective": "Simulate full 3-hour examination under strict exam conditions with comprehensive post-test review.",
                "weekly_hours": round((daily_minutes * 7) / 60.0, 1),
                "milestone_check": f"Reach verified target score of Band {target_band} across all four skills."
            }
        ]

        return {
            "learner_id": learner_id,
            "track": track,
            "current_band": current_band,
            "target_band": target_band,
            "band_gap": band_gap,
            "cefr_level": cefr_level,
            "days_until_exam": days_remaining,
            "daily_minutes": daily_minutes,
            "skills_radar": skill_scores,
            "weakest_skill": weakest_skill,
            "due_srs_cards_count": due_count,
            "pending_lessons_count": pending_lessons_count,
            "strategy_summary": strategy_summary,
            "four_week_milestones": milestones
        }
