"""
Unit tests for IELTS Band Scoring and Study Planning.
"""

import unittest
from core.scoring.band_calculator import BandCalculator
from core.scoring.cefr_diagnostic import CEFRDiagnostic
from core.progress.study_planner import StudyPlanner
from core.progress.analytics import LearningAnalytics
from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, TestResultRepository, MistakeBookRepository
import tempfile
import os


class TestStudyPlanAndScoring(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()
        self.planner = StudyPlanner(self.db)

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_official_ielts_half_band_rounding(self):
        # Rounding rules:
        # 6.125 -> 6.0
        # 6.25 -> 6.5
        # 6.625 -> 6.5
        # 6.75 -> 7.0
        self.assertEqual(BandCalculator.round_band(6.125), 6.0)
        self.assertEqual(BandCalculator.round_band(6.25), 6.5)
        self.assertEqual(BandCalculator.round_band(6.625), 6.5)
        self.assertEqual(BandCalculator.round_band(6.75), 7.0)

    def test_overall_composite_band(self):
        # 6.5, 6.5, 6.0, 6.0 -> mean 6.25 -> round 6.5
        overall = BandCalculator.calculate_overall(6.5, 6.5, 6.0, 6.0)
        self.assertEqual(overall["overall_band"], 6.5)

    def test_study_planner_daily_generation(self):
        plan = self.planner.generate_daily_plan("student_1")
        self.assertIn("tasks", plan)
        self.assertEqual(len(plan["tasks"]), 3)
        self.assertIn("Good morning", plan["daily_greeting"])

    def test_dynamic_skills_radar_baseline(self):
        # Baseline without test records should derive from CEFR level
        learner_repo = LearnerRepository(self.db)
        learner = learner_repo.create_learner(name="Test B1", current_band=5.0, cefr_level="B1")

        analytics = LearningAnalytics(self.db)
        dashboard = analytics.get_dashboard_data(learner["id"])

        radar = dashboard["skills_radar"]
        self.assertIn("Reading", radar)
        self.assertIn("Listening", radar)
        self.assertIn("Writing", radar)
        self.assertIn("Speaking", radar)
        self.assertIn("Grammar", radar)
        self.assertIn("Vocabulary", radar)
        self.assertIn("Fluency", radar)
        self.assertIn("Pronunciation", radar)
        # B1 base is 5.0
        self.assertEqual(radar["Reading"], 5.0)
        self.assertEqual(radar["Listening"], 5.0)

    def test_dynamic_skills_radar_with_test_evidence(self):
        learner_repo = LearnerRepository(self.db)
        learner = learner_repo.create_learner(name="Scored Learner", current_band=6.0, cefr_level="B2")

        test_repo = TestResultRepository(self.db)
        test_repo.record_result(
            learner_id=learner["id"],
            test_type="mock_reading",
            track="Academic",
            overall_band=7.5,
            reading_band=8.0,
            listening_band=7.0
        )

        analytics = LearningAnalytics(self.db)
        dashboard = analytics.get_dashboard_data(learner["id"])
        radar = dashboard["skills_radar"]

        # Reading should be 8.0, Listening should be 7.0 from real test results
        self.assertEqual(radar["Reading"], 8.0)
        self.assertEqual(radar["Listening"], 7.0)


if __name__ == "__main__":
    unittest.main()
