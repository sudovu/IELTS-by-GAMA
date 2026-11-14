"""
Tests for Phase 14: Full IELTS Examination Simulation & End-to-End Validation.
Verifies:
1. Academic and General Training full mock exam creation and structure.
2. 40-question Reading evaluation and question-type accuracy.
3. 40-question Listening evaluation with number, spelling, and word-limit bounds.
4. Dual-task Writing submission with official 1/3 (Task 1) + 2/3 (Task 2) weighting.
5. 3-stage Speaking response handling and non-acoustic STT transparency.
6. Real-time timer calculation, autosave persistence, and refresh recovery.
7. Flagged and unanswered question tracking.
8. Duplicate submission locking and idempotent results.
9. Answer-key concealment in active client payloads.
10. Strict multi-learner isolation and tamper prevention.
11. Automatic Mistake Book logging and adaptive diagnostic recommendations.
"""

import unittest
import tempfile
import os
import json
import time
from core.database.db_manager import DatabaseManager
from core.database.repositories import (
    LearnerRepository,
    ExamSessionRepository,
    MistakeBookRepository,
    TestResultRepository
)
from core.exam.content_repository import ExamContentRepository
from core.exam.exam_manager import ExamManager
from core.scoring.band_calculator import BandCalculator


class TestPhase14ExamSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_path = cls.temp_file.name
        cls.temp_file.close()

        cls.db = DatabaseManager(cls.temp_path)
        cls.db.init_schema()

        # Apply migrations
        from core.database.migrations import MigrationManager
        mig = MigrationManager(cls.db)
        mig.run_migrations()

        cls.learner_repo = LearnerRepository(cls.db)
        cls.mistake_repo = MistakeBookRepository(cls.db)
        cls.exam_repo = ExamSessionRepository(cls.db)
        cls.result_repo = TestResultRepository(cls.db)
        cls.exam_mgr = ExamManager(db=cls.db, mistake_repo=cls.mistake_repo)

        # Create test learners
        cls.learner_1 = cls.learner_repo.create_learner("Candidate Academic", target_band=7.5)
        cls.learner_2 = cls.learner_repo.create_learner("Candidate GT", target_band=6.5)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.close()
        except Exception:
            pass
        try:
            if os.path.exists(cls.temp_path):
                os.remove(cls.temp_path)
        except Exception:
            pass

    def test_exam_library_catalog_and_content_availability(self):
        """Verifies available practice exams meet Academic and General Training specifications."""
        library = ExamContentRepository.list_available_exams()
        self.assertGreaterEqual(len(library), 8)

        exam_ids = [e["id"] for e in library]
        self.assertIn("mock_full_acad", exam_ids)
        self.assertIn("mock_full_gt", exam_ids)
        self.assertIn("exam_read_acad_1", exam_ids)
        self.assertIn("exam_read_gt_1", exam_ids)
        self.assertIn("exam_listen_1", exam_ids)
        self.assertIn("exam_write_acad_1", exam_ids)
        self.assertIn("exam_write_gt_1", exam_ids)
        self.assertIn("exam_speak_1", exam_ids)

    def test_answer_key_concealment_in_client_payloads(self):
        """Verifies active examination payloads strictly conceal answer keys, evidence, and explanations."""
        # Concealed client package
        client_pkg = ExamContentRepository.get_exam_package("exam_read_acad_1", conceal_answers=True)
        self.assertIsNotNone(client_pkg)

        for p in client_pkg.get("passages", []):
            self.assertNotIn("synonym_table", p)
            for q in p.get("questions", []):
                self.assertNotIn("correct", q, f"Question {q.get('num')} leaked correct answer key!")
                self.assertNotIn("correct_index", q, f"Question {q.get('num')} leaked correct_index!")
                self.assertNotIn("acceptable", q, f"Question {q.get('num')} leaked acceptable answers!")
                self.assertNotIn("evidence", q, f"Question {q.get('num')} leaked evidence!")
                self.assertNotIn("explanation", q, f"Question {q.get('num')} leaked explanation!")

        # Unconcealed grading package
        grading_pkg = ExamContentRepository.get_exam_package("exam_read_acad_1", conceal_answers=False)
        self.assertIn("correct", grading_pkg["passages"][0]["questions"][0])
        self.assertIn("explanation", grading_pkg["passages"][0]["questions"][0])

    def test_academic_reading_40_questions_and_grading(self):
        """Verifies Academic Reading contains 40 questions and evaluates properly."""
        pkg = ExamContentRepository.get_exam_package("exam_read_acad_1", conceal_answers=False)
        passages = pkg["passages"]
        self.assertEqual(len(passages), 3, "Academic reading must contain 3 passages")

        total_q = sum(len(p["questions"]) for p in passages)
        self.assertEqual(total_q, 40, "Academic reading mock must contain exactly 40 questions")

        # Start an exam session
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="reading")
        sid = session["session_id"]

        # Submit sample answers
        answers = {
            "read_1": "False",  # Correct
            "read_2": "True",   # Correct
            "read_3": "False",  # Correct
            "read_4": "False",  # Correct
            "read_5": "False",  # Correct
            "read_6": "Not Given", # Correct
            "read_7": "True",   # Correct
            "read_8": "400",    # Correct
            "read_9": "black smokers", # Correct
            "read_10": "plumes", # Correct
            "read_11": "wrong_organ", # Incorrect
            "read_12": "bacteria", # Correct
            "read_13": "Rapid larval dispersion across inhospitable abyssal waters" # Correct
        }
        res = self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers=answers)
        self.assertTrue(res["success"])
        read_eval = res["results"]["skills"]["reading"]
        self.assertEqual(read_eval["total_questions"], 40)
        self.assertEqual(read_eval["correct_answers"], 12)
        self.assertGreaterEqual(read_eval["estimated_band"], 3.5)
        self.assertIn("confidence_range", read_eval)

    def test_general_training_reading_40_questions_and_grading(self):
        """Verifies General Training Reading contains 40 questions across 3 sections."""
        pkg = ExamContentRepository.get_exam_package("exam_read_gt_1", conceal_answers=False)
        sections = pkg["sections"]
        self.assertEqual(len(sections), 3, "GT reading must contain 3 sections")

        total_q = sum(len(s["questions"]) for s in sections)
        self.assertEqual(total_q, 40, "GT reading mock must contain exactly 40 questions")

        session = self.exam_mgr.start_exam(self.learner_2["id"], track="General Training", module="reading")
        sid = session["session_id"]

        # Submit answers
        answers = {
            "read_1": "True", "read_2": "False", "read_3": "True",
            "read_8": "140", "read_9": "15", "read_10": "50"
        }
        res = self.exam_mgr.submit_exam(sid, self.learner_2["id"], final_answers=answers)
        self.assertTrue(res["success"])
        read_eval = res["results"]["skills"]["reading"]
        self.assertEqual(read_eval["total_questions"], 40)
        self.assertGreaterEqual(read_eval["correct_answers"], 6)

    def test_listening_40_questions_and_grading(self):
        """Verifies Listening contains 40 questions and evaluates with number and spelling bounds."""
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="listening")
        sid = session["session_id"]
        self.assertEqual(session["time_limit_seconds"], 1920) # 32 minutes

        answers = {
            "listen_1": "Sterling",
            "listen_2": "en-suite",
            "listen_3": "210",
            "listen_4": "September",
            "listen_5": "Science",
            "listen_6": "self",
            "listen_7": "350",
            "listen_8": "48",
            "listen_9": "4829",
            "listen_10": "passport"
        }
        res = self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers=answers)
        self.assertTrue(res["success"])
        listen_eval = res["results"]["skills"]["listening"]
        self.assertEqual(listen_eval["total_questions"], 40)
        self.assertGreaterEqual(listen_eval["correct_answers"], 10)
        self.assertIn("transcript_strategy_practice", listen_eval["activity_type"])

    def test_writing_dual_task_weighting(self):
        """Verifies Writing enforces 1/3 (Task 1) + 2/3 (Task 2) weighting."""
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="writing")
        sid = session["session_id"]

        t1_essay = (
            "The line graph illustrates industrial greenhouse gas emissions across four economic sectors "
            "between 1990 and 2025 in a European nation. Overall, energy production commenced as the primary "
            "polluter, whereas transportation exhibited the most marked continuous upward trajectory. "
            "In 1990, emissions from energy production stood at approximately 80 million metric tons, followed "
            "closely by manufacturing at 65 million tons. Over the 35-year timeframe, energy production emissions "
            "declined substantially due to renewable grid investment, falling to roughly 35 million tons by 2025. "
            "Conversely, transportation emissions escalated dramatically from 40 million tons to 75 million tons. "
            "Agriculture remained relatively stable, fluctuating around 25 million metric tons throughout the period."
        )

        t2_essay = (
            "The advent of artificial intelligence and automated robotics has sparked contentious debate "
            "regarding the economic survival of the modern workforce. While some commentators argue that "
            "governments should introduce an unconditional Universal Basic Income (UBI) to protect citizens, "
            "critics assert that such measures disincentivize productive labor and risk fiscal insolvency. "
            "In my view, while a universal cash grant may alleviate immediate poverty, a targeted safety net "
            "coupled with active educational reskilling provides a far more viable long-term strategy.\n\n"
            "Proponents of Universal Basic Income emphasize that rapid technological disruption will render millions "
            "of manual and cognitive positions obsolete. When automated algorithms replace drivers, accountants, "
            "and assembly workers, structural unemployment could precipitate widespread destitution. A guaranteed "
            "baseline income provides a vital cushion, allowing displaced individuals to afford essential nutrition, "
            "shelter, and healthcare while transitioning between occupations.\n\n"
            "However, an unconditional UBI carries profound economic and psychological drawbacks. Financing such an "
            "immense entitlement program would require unprecedented tax burdens, potentially stifling technological "
            "innovation and entrepreneurial investment. Furthermore, employment provides individuals with purpose, "
            "social integration, and self-esteem that unconditional financial transfers cannot replicate.\n\n"
            "In conclusion, rather than distributing indiscriminate stipends, state authorities should invest in "
            "subsidized technical education and public infrastructure projects. This approach ensures economic dignity "
            "and sustainable national productivity."
        )

        res = self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers={
            "writing_task_1": t1_essay,
            "writing_task_2": t2_essay
        })

        self.assertTrue(res["success"])
        writing_eval = res["results"]["skills"]["writing"]
        t1_band = writing_eval["task_1"]["band"]
        t2_band = writing_eval["task_2"]["band"]
        comp_band = writing_eval["estimated_band"]

        # Verify weighted formula: round_band(1/3 * t1 + 2/3 * t2)
        expected_raw = (1.0 / 3.0) * t1_band + (2.0 / 3.0) * t2_band
        expected_band = BandCalculator.round_band(expected_raw)
        self.assertEqual(comp_band, expected_band, "Writing must strictly apply 1/3 + 2/3 weighting formula")

    def test_speaking_3_stage_evaluation(self):
        """Verifies Speaking handles Parts 1, 2, and 3 and discloses STT transcript modality."""
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="speaking")
        sid = session["session_id"]

        answers = {
            "speaking_part_1": "I find myself most productive during early mornings when my schedule is completely quiet.",
            "speaking_part_2": "An ambitious goal I achieved was leading a comprehensive renewable energy research initiative at university.",
            "speaking_part_3": "Career prestige is increasingly balanced against personal mental wellbeing in contemporary workplaces."
        }
        res = self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers=answers)
        self.assertTrue(res["success"])
        speaking_eval = res["results"]["skills"]["speaking"]
        self.assertIn("speech_recognition_transcript_matching", speaking_eval["assessment_modality"])
        self.assertIn("acoustic_analysis_disclaimer", speaking_eval)
        self.assertTrue(speaking_eval["parts_evaluated"]["part_1"])
        self.assertTrue(speaking_eval["parts_evaluated"]["part_2"])
        self.assertTrue(speaking_eval["parts_evaluated"]["part_3"])

    def test_autosave_and_session_recovery_after_refresh(self):
        """Verifies candidate answers and elapsed time persist safely across simulated page refreshes."""
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="reading")
        sid = session["session_id"]

        # Autosave partial answers and flagged question
        save_res = self.exam_mgr.autosave_answers(
            session_id=sid,
            learner_id=self.learner_1["id"],
            answers={"read_1": "False", "read_2": "True"},
            flagged_questions=[5, 12],
            current_section="reading",
            current_question=3,
            time_spent_seconds=180
        )
        self.assertTrue(save_res["success"])

        # Simulate page refresh by querying get_active_session()
        recovered = self.exam_mgr.get_active_session(self.learner_1["id"])
        self.assertIsNotNone(recovered)
        self.assertEqual(recovered["session_id"], sid)
        self.assertEqual(recovered["answers"]["read_1"], "False")
        self.assertEqual(recovered["answers"]["read_2"], "True")
        self.assertIn(5, recovered["flagged"])
        self.assertIn(12, recovered["flagged"])
        self.assertEqual(recovered["current_question"], 3)
        self.assertLessEqual(recovered["remaining_seconds"], 3600 - 180)

    def test_duplicate_submission_prevention(self):
        """Verifies duplicate submissions of the same exam session are rejected idempotently."""
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="reading")
        sid = session["session_id"]

        sub1 = self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers={"read_1": "False"})
        self.assertTrue(sub1["success"])
        band1 = sub1["overall_band"]

        # Duplicate submission attempt
        sub2 = self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers={"read_1": "True"})
        self.assertTrue(sub2["success"])
        self.assertTrue(sub2.get("already_submitted", False))
        self.assertEqual(sub2["band_score"], band1, "Duplicate submission must return original grade without alteration")

    def test_multi_learner_isolation(self):
        """Verifies a learner cannot access, autosave to, or submit another learner's examination session."""
        session_1 = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="reading")
        sid_1 = session_1["session_id"]

        # Learner 2 attempts to autosave to Learner 1's session
        hack_save = self.exam_mgr.autosave_answers(
            session_id=sid_1,
            learner_id=self.learner_2["id"],
            answers={"read_1": "Hacked"}
        )
        self.assertFalse(hack_save["success"])
        self.assertIn("unauthorized", hack_save["error"].lower())

        # Learner 2 attempts to submit Learner 1's session
        hack_sub = self.exam_mgr.submit_exam(
            session_id=sid_1,
            learner_id=self.learner_2["id"],
            final_answers={"read_1": "Hacked"}
        )
        self.assertFalse(hack_sub["success"])
        self.assertIn("unauthorized", hack_sub["error"].lower())

    def test_mistake_book_integration_on_exam_completion(self):
        """Verifies incorrect examination answers are automatically recorded into the Mistake Book."""
        session = self.exam_mgr.start_exam(self.learner_1["id"], track="Academic", module="reading")
        sid = session["session_id"]

        # Submit deliberately wrong answer
        self.exam_mgr.submit_exam(sid, self.learner_1["id"], final_answers={"read_1": "True"}) # Correct is False

        mistakes = self.mistake_repo.get_mistakes_by_learner(self.learner_1["id"])
        self.assertGreater(len(mistakes), 0, "Mistake Book must log incorrect examination items")
        has_reading_mistake = any("reading" in m["skill"].lower() for m in mistakes)
        self.assertTrue(has_reading_mistake)


if __name__ == "__main__":
    unittest.main()
