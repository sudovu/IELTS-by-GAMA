"""
Phase 15 - Independent Product Verification, Real-World Testing & Release Readiness Tests
Validates:
1. Full journey for Learner A (Academic) with multi-skill grading and Mistake Book integration.
2. Full journey for Learner B (General Training) with complete data isolation.
3. Cross-learner session access prevention and boundary security.
4. Abandoned exam session submission rejection.
5. Malformed autosave payload handling and safe answer merging.
6. Server-authoritative timing and timeout detection.
7. Zero-word and severely underlength Writing scoring integrity (Band 0.0 vs legacy 5.0).
8. Zero-word Speaking turn scoring integrity (Band 0.0 vs legacy 6.5).
9. Curriculum partial submission mastery prevention.
10. Speech synthesis script availability without answer key leakage.
"""

import unittest
import json
import time
import os
import tempfile
import datetime
from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, MistakeBookRepository, TestResultRepository
from core.database.migrations import MigrationManager
from core.exam.exam_manager import ExamManager
from core.exam.content_repository import ExamContentRepository
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.curriculum.curriculum_engine import CurriculumEngine

class TestPhase15IndependentVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_path = cls.temp_file.name
        cls.temp_file.close()

        cls.db = DatabaseManager(cls.temp_path)
        cls.db.init_schema()
        mig = MigrationManager(cls.db)
        mig.run_migrations()

        cls.learner_repo = LearnerRepository(cls.db)
        cls.mistake_repo = MistakeBookRepository(cls.db)
        cls.result_repo = TestResultRepository(cls.db)
        cls.exam_mgr = ExamManager(
            db=cls.db,
            mistake_repo=cls.mistake_repo
        )
        cls.curriculum = CurriculumEngine(cls.db)

        # Create two isolated test learners
        cls.learner_a = cls.learner_repo.create_learner("Learner Academic", target_band=7.5)
        cls.learner_b = cls.learner_repo.create_learner("Learner General", target_band=6.5)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "temp_path") and os.path.exists(cls.temp_path):
            try:
                os.unlink(cls.temp_path)
            except Exception:
                pass

    def test_01_learner_a_academic_full_journey(self):
        """Validates Learner A completing an authentic Academic exam with mistake logging and recommendations."""
        session = self.exam_mgr.start_exam(self.learner_a["id"], track="Academic", module="full_mock")
        sid = session["session_id"]
        self.assertEqual(session["track"], "Academic")
        self.assertEqual(session["time_limit_seconds"], 164 * 60)

        # Submit answers: 30 Reading, 25 Listening, Academic Task 1 & 2, Speaking
        answers = {
            # Reading (Sample of questions)
            "read_1": "TRUE", "read_2": "FALSE", "read_3": "NOT GIVEN",
            "read_4": "TRUE", "read_5": "FALSE", "read_6": "TRUE",
            "read_7": "surface", "read_8": "vegetation",
            # Listening
            "listen_1": "Sterling", "listen_2": "en-suite", "listen_3": "210",
            "listen_4": "September", "listen_5": "Science",
            # Writing
            "writing_task_1": (
                "The line graph illustrates greenhouse gas emissions across four sectors between 1990 and 2025. "
                "Overall, energy production was the highest contributor initially, while transport demonstrated the most "
                "pronounced continuous increase. Emissions from transport rose from 20 to 75 million tons over the period. "
                "In contrast, agriculture remained relatively steady at approximately 15 million metric tons throughout the duration."
            ),
            "writing_task_2": (
                "Technological automation has rapidly transformed workplace environments across the globe. "
                "I strongly agree that while automation displaces specific routine roles, it ultimately creates higher-value employment. "
                "Firstly, machines eradicate monotonous manual labor, allowing humans to focus on creative and analytical endeavors. "
                "For example, industrial robotics take over dangerous assembly work, reducing workplace injuries significantly. "
                "Secondly, new industries emerge around artificial intelligence development, data architecture, and software governance. "
                "In conclusion, automation should be welcomed as an engine of economic growth rather than feared as a threat."
            ),
            # Speaking
            "speaking_part_1": "My name is Alice. I come from a coastal town known for its peaceful environment and historical architecture.",
            "speaking_part_2": "I would like to describe learning full-stack software development. It was an ambitious goal that required intense discipline.",
            "speaking_part_3": "Technological advancement definitely brings ethical questions regarding data security and workplace equity."
        }

        # Autosave first
        autosave_res = self.exam_mgr.autosave_answers(sid, self.learner_a["id"], answers)
        self.assertTrue(autosave_res["success"])

        # Final submission
        res = self.exam_mgr.submit_exam(sid, self.learner_a["id"])
        self.assertTrue(res["success"])
        results = res["results"]

        self.assertIn("reading", results["skills"])
        self.assertIn("listening", results["skills"])
        self.assertIn("writing", results["skills"])
        self.assertIn("speaking", results["skills"])
        self.assertGreater(results["overall_band"], 0.0)
        self.assertIn("recommendations", results)

        # Check that Mistake Book received un-answered or incorrect items for Learner A
        mistakes_a = self.mistake_repo.get_mistakes_by_learner(self.learner_a["id"])
        self.assertGreater(len(mistakes_a), 0)

    def test_02_learner_b_general_training_full_journey(self):
        """Validates Learner B completing an authentic General Training exam with isolated records."""
        session = self.exam_mgr.start_exam(self.learner_b["id"], track="General Training", module="full_mock")
        sid = session["session_id"]
        self.assertEqual(session["track"], "General Training")

        answers = {
            "read_1": "TRUE", "read_2": "TRUE", "read_3": "FALSE",
            "listen_1": "Sterling", "listen_2": "en-suite",
            "writing_task_1": (
                "Dear Mr. Robinson, I am writing to express my dissatisfaction regarding persistent late-night noise "
                "from apartment 4B. Despite speaking with the tenant twice, loud music continues beyond midnight. "
                "I would appreciate it if management could issue a formal notice to maintain building quiet hours. "
                "Yours sincerely, Bob Smith."
            ),
            "writing_task_2": (
                "Public transit subsidies provide significant community advantages. "
                "I firmly believe that reducing public transport fares improves urban mobility and environmental health. "
                "Firstly, accessible trains and buses reduce private car congestion. "
                "For instance, cities with subsidized transit report 30% fewer traffic gridlocks during peak hours. "
                "Secondly, lower emissions lead to cleaner air for all residents. "
                "In conclusion, government investment in transit infrastructure is essential for sustainable cities."
            ),
            "speaking_part_1": "Hello, my name is Bob. I live in a metropolitan city with diverse cultural neighborhoods."
        }

        res = self.exam_mgr.submit_exam(sid, self.learner_b["id"], final_answers=answers)
        self.assertTrue(res["success"])
        self.assertEqual(res["results"]["track"], "General Training")

        # Verify history isolation: Learner B's history only has Learner B's test
        history_b = self.exam_mgr.list_learner_history(self.learner_b["id"])
        self.assertEqual(len(history_b), 1)
        self.assertEqual(history_b[0]["learner_id"], self.learner_b["id"])

    def test_03_cross_learner_security_boundaries(self):
        """Ensures Learner B cannot view, autosave, or submit Learner A's session."""
        session_a = self.exam_mgr.start_exam(self.learner_a["id"], track="Academic", module="reading")
        sid_a = session_a["session_id"]

        # Learner B attempts to autosave to Learner A's session
        save_hack = self.exam_mgr.autosave_answers(sid_a, self.learner_b["id"], {"read_1": "HACK"})
        self.assertFalse(save_hack["success"])
        self.assertIn("Unauthorized", save_hack["error"])

        # Learner B attempts to submit Learner A's session
        submit_hack = self.exam_mgr.submit_exam(sid_a, self.learner_b["id"], {"read_1": "HACK"})
        self.assertFalse(submit_hack["success"])
        self.assertIn("Unauthorized", submit_hack["error"])

        # Learner B attempts to read results
        results_hack = self.exam_mgr.get_exam_results(sid_a, self.learner_b["id"])
        self.assertIsNone(results_hack)

    def test_04_abandoned_session_submission_rejection(self):
        """Verifies that an abandoned exam cannot be submitted or evaluated."""
        session = self.exam_mgr.start_exam(self.learner_a["id"], track="Academic", module="reading")
        sid = session["session_id"]

        # Abandon session
        self.db.execute("UPDATE exam_sessions SET status = 'abandoned' WHERE id = ?", (sid,))

        # Try to submit abandoned session
        res = self.exam_mgr.submit_exam(sid, self.learner_a["id"])
        self.assertFalse(res["success"])
        self.assertIn("Cannot submit an exam session with status 'abandoned'", res["error"])

    def test_05_malformed_autosave_payload_and_merging(self):
        """Ensures non-dict answers are rejected and valid answers merge safely."""
        session = self.exam_mgr.start_exam(self.learner_a["id"], track="Academic", module="listening")
        sid = session["session_id"]

        # 1. Non-dict payload rejected
        bad_save = self.exam_mgr.autosave_answers(sid, self.learner_a["id"], ["list", "payload"])
        self.assertFalse(bad_save["success"])
        self.assertIn("dictionary", bad_save["error"])

        # 2. Sequential valid saves merge without data loss
        save1 = self.exam_mgr.autosave_answers(sid, self.learner_a["id"], {"listen_1": "Sterling"})
        self.assertTrue(save1["success"])
        self.assertEqual(save1["answered_count"], 1)

        save2 = self.exam_mgr.autosave_answers(sid, self.learner_a["id"], {"listen_2": "en-suite"})
        self.assertTrue(save2["success"])
        self.assertEqual(save2["answered_count"], 2)

        # Retrieve session: verify both keys are retained
        active = self.exam_mgr.get_active_session(self.learner_a["id"])
        self.assertEqual(active["answers"].get("listen_1"), "Sterling")
        self.assertEqual(active["answers"].get("listen_2"), "en-suite")

    def test_06_server_authoritative_timer_and_timeout(self):
        """Ensures exam submissions beyond time limit (+ grace period) are flagged."""
        session = self.exam_mgr.start_exam(self.learner_a["id"], track="Academic", module="reading")
        sid = session["session_id"]

        # Backdate started_at by 3 hours (10800 seconds vs 3600 second limit)
        old_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=3)).isoformat()
        self.db.execute("UPDATE exam_sessions SET started_at = ? WHERE id = ?", (old_time, sid))

        # Autosave should now be rejected as expired
        save_res = self.exam_mgr.autosave_answers(sid, self.learner_a["id"], {"read_1": "TRUE"})
        self.assertFalse(save_res["success"])
        self.assertIn("expired", save_res["error"].lower())

        # Submit should accept the submission but flag timing status as timed out
        sub_res = self.exam_mgr.submit_exam(sid, self.learner_a["id"])
        self.assertTrue(sub_res["success"])
        self.assertTrue(sub_res["results"]["is_timed_out"])
        self.assertIn("expired", sub_res["results"]["timing_status"].lower())

    def test_07_writing_scoring_integrity_zero_and_underlength(self):
        """Verifies zero words receives Band 0.0 and underlength is heavily penalized."""
        # 0 words
        eval_0 = WritingEvaluator.evaluate_essay("acad_w1_report", "")
        self.assertEqual(eval_0["estimated_band"], 0.0)
        self.assertEqual(eval_0["task_achievement_band"], 0.0)

        # 10 words (severely underlength)
        eval_short = WritingEvaluator.evaluate_essay("acad_w1_report", "The line graph shows some industrial greenhouse gas sector emissions.")
        self.assertEqual(eval_short["estimated_band"], 1.5)

    def test_08_speaking_scoring_integrity_zero_and_underlength(self):
        """Verifies zero spoken words receives Band 0.0 and brief turn is penalized."""
        # 0 words
        eval_0 = SpeakingExaminer.evaluate_spoken_response("")
        self.assertEqual(eval_0["estimated_band"], 0.0)
        self.assertEqual(eval_0["criteria_scores"]["FC"], 0.0)

        # 4 words
        eval_short = SpeakingExaminer.evaluate_spoken_response("I like reading books.")
        self.assertEqual(eval_short["estimated_band"], 1.5)

    def test_09_curriculum_mastery_anti_cheat(self):
        """Ensures answering only 1 out of 3 questions yields 33.3%, not 100% or mastery."""
        res = self.curriculum.evaluate_submission(
            learner_id=self.learner_a["id"],
            lesson_id="curric_a2_gram_past_simple",
            answers={"a2_as_1": 1} # Only 1 question out of 3
        )
        self.assertEqual(res["score"], 33.3)
        self.assertNotEqual(res["status"], "mastered")
        self.assertEqual(res["status"], "needs_review")

    def test_10_speech_synthesis_audio_script_retention(self):
        """Verifies that sanitized packages retain dialogue text for speech synthesis without answer leakage."""
        pkg = ExamContentRepository.get_exam_package("exam_listen_1", conceal_answers=True)
        sec1 = pkg["sections"][0]

        # audio_script must be present for Web Speech synthesis
        self.assertIn("audio_script", sec1)
        self.assertGreater(len(sec1["audio_script"]), 50)

        # Answer keys and notes must be strictly removed
        q1 = sec1["questions"][0]
        self.assertNotIn("correct", q1)
        self.assertNotIn("acceptable", q1)
        self.assertNotIn("distractor_note", q1)
        self.assertNotIn("evidence", q1)

if __name__ == "__main__":
    unittest.main()
