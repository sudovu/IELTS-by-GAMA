# -*- coding: utf-8 -*-
"""
Tests for Phase 9: Analytics & Adaptive Study Planner.
Verifies:
1. Daily and weekly study plan generation.
2. Adaptive study planner synthesizing actual test records and radar metrics.
3. Weakest sub-skill prioritization and milestone structuring.
4. Target exam countdown calculation.
"""

import unittest
import os
import tempfile
import datetime
from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, TestResultRepository, MistakeBookRepository
from core.progress.study_planner import StudyPlanner


class TestPhase9StudyPlanner(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

        self.learner_repo = LearnerRepository(self.db)
        self.test_repo = TestResultRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)
        self.planner = StudyPlanner(self.db)

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_daily_and_weekly_plan(self):
        """Verifies daily and weekly plans allocate study time appropriately."""
        learner_id = "phase9_learner_1"
        self.learner_repo.get_or_create_default(learner_id)
        self.learner_repo.update_profile(learner_id, {"daily_minutes": 40})

        daily = self.planner.generate_daily_plan(learner_id)
        self.assertEqual(daily["daily_minutes"], 40)
        self.assertEqual(len(daily["tasks"]), 3)
        self.assertIn("task_vocab", [t["task_id"] for t in daily["tasks"]])

        weekly = self.planner.generate_weekly_plan(learner_id)
        self.assertEqual(len(weekly["weekly_schedule"]), 7)

    def test_adaptive_study_plan_synthesis(self):
        """Verifies multi-week adaptive milestones targeting real learner weaknesses."""
        learner_id = "phase9_learner_adaptive"
        future_date = (datetime.date.today() + datetime.timedelta(days=45)).isoformat()
        self.learner_repo.get_or_create_default(learner_id)
        self.learner_repo.update_profile(learner_id, {
            "target_band": 7.5,
            "current_band": 6.0,
            "cefr_level": "B2",
            "track": "Academic",
            "target_exam_date": future_date,
            "daily_minutes": 45
        })

        # Record test where writing is significantly weaker than other skills
        self.test_repo.record_result(
            learner_id=learner_id,
            test_type="mock",
            track="Academic",
            overall_band=6.0,
            listening_band=7.0,
            reading_band=7.0,
            writing_band=5.0,
            speaking_band=6.5
        )

        plan = self.planner.generate_adaptive_study_plan(learner_id)
        self.assertEqual(plan["learner_id"], learner_id)
        self.assertEqual(plan["track"], "Academic")
        self.assertEqual(plan["target_band"], 7.5)
        self.assertEqual(plan["current_band"], 6.0)
        self.assertEqual(plan["band_gap"], 1.5)
        self.assertGreaterEqual(plan["days_until_exam"], 40)

        # Writing was explicitly scored at 5.0, so weakest skill should be writing
        self.assertEqual(plan["weakest_skill"], "writing")
        self.assertIn("WRITING", plan["strategy_summary"])

        # Check 4 phases present
        self.assertEqual(len(plan["four_week_milestones"]), 4)
        phase_names = [m["phase"] for m in plan["four_week_milestones"]]
        self.assertTrue(any("Remediation" in p for p in phase_names))
        self.assertTrue(any("Technique" in p for p in phase_names))


if __name__ == "__main__":
    unittest.main()
