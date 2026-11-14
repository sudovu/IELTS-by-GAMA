"""
Phase 18 Automated Test Suite:
Student-First IELTS Platform, Assessment Accuracy & Result Verification.

Covers:
1. Student registration, authentication, and role isolation (learner role strictly enforced).
2. Cross-learner data isolation (preventing unauthorized access to another student's sessions/results).
3. Reading assessment accuracy across all question types (TFNG, MCQ, Matching, Completion).
4. Listening assessment accuracy with sequential question numbering (1-40) and collision prevention.
5. Empty and whitespace-only answer credit guard (zero marks awarded, flagged unanswered).
6. Duplicate submission protection (idempotency, cannot alter marks of completed session).
7. Invalid question keys rejection (arbitrary or spoofed IDs cannot inflate scores).
8. Transparent result breakdown (raw score, total, percentage, band, answer key version, evidence).
9. Historical result reproducibility (persisted audit records retain exact answers and scoring metadata).
10. Writing evaluation hardening (empty essay = Band 0.0, severe underlength band caps, diagnostic disclaimers).
11. Speaking evaluation hardening (empty transcript = Band 0.0, acoustic/pronunciation limitation disclosure).
12. Automated mistake book logging for Reading and Listening diagnostic remediation.
13. Student dashboard analytics, honest empty states, and adaptive recommendations.
14. Educator UI feature simplification (hiding teacher/examiner chrome from student learners).
"""

import unittest
import os
import tempfile
import sqlite3
import json

from core.database.db_manager import DatabaseManager
from core.database.migrations import MigrationManager
from core.database.repositories import LearnerRepository, TestResultRepository
from core.auth.auth_manager import AuthManager
from core.reading.reading_engine import ReadingEngine
from core.reading.question_types import ReadingQuestionTypes
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.scoring.criteria_evaluator import CriteriaEvaluator
from core.exam.exam_manager import ExamManager
from core.progress.mistake_book import MistakeBook
from core.progress.analytics import LearningAnalytics
from core.curriculum.curriculum_engine import CurriculumEngine


class TestPhase18StudentAssessmentIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an isolated temporary SQLite database for Phase 18 tests
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_path = cls.temp_file.name
        cls.temp_file.close()

        cls.db = DatabaseManager(cls.temp_path)
        cls.db.init_schema()
        mig = MigrationManager(cls.db)
        mig.run_migrations()

        cls.auth_mgr = AuthManager(cls.db)
        cls.learner_repo = LearnerRepository(cls.db)
        cls.test_repo = TestResultRepository(cls.db)
        cls.mistake_book = MistakeBook(cls.db)
        cls.analytics = LearningAnalytics(cls.db)
        cls.exam_mgr = ExamManager(cls.db)
        cls.criteria_evaluator = CriteriaEvaluator()
        cls.writing_evaluator = WritingEvaluator()
        cls.speaking_examiner = SpeakingExaminer()
        cls.reading_engine = ReadingEngine()
        cls.listening_engine = ListeningEngine()
        cls.curriculum_engine = CurriculumEngine(cls.db)

    @classmethod
    def tearDownClass(cls):
        try:
            if os.path.exists(cls.temp_path):
                os.remove(cls.temp_path)
        except Exception:
            pass

    # 1. Student Registration & Authentication
    def test_01_student_registration_and_authentication(self):
        # Register a regular student
        res = self.auth_mgr.register_user("student_maya", "StudentPass123!")
        self.assertTrue(res["success"])
        self.assertEqual(res["role"], "learner")

        # Attempt to escalate role during self-registration
        res_esc = self.auth_mgr.register_user("student_hacker", "HackerPass123!", role="admin")
        # Should force role to learner for non-admin callers
        if res_esc["success"]:
            self.assertEqual(res_esc["role"], "learner", "Self-registration must not permit admin role")

        # Authenticate with credentials
        auth = self.auth_mgr.authenticate("student_maya", "StudentPass123!")
        self.assertIsNotNone(auth)
        self.assertEqual(auth["username"], "student_maya")
        self.assertEqual(auth["role"], "learner")

        # Session creation
        token = self.auth_mgr.create_session(auth["id"])
        self.assertTrue(bool(token))
        session_user = self.auth_mgr.validate_session(token)
        self.assertIsNotNone(session_user)
        self.assertEqual(session_user["username"], "student_maya")

    # 2. Cross-Learner Data Isolation
    def test_02_cross_learner_data_isolation(self):
        # Register two learners
        self.auth_mgr.register_user("learner_alpha", "PassAlpha123!")
        self.auth_mgr.register_user("learner_beta", "PassBeta123!")

        # Create exam session for Learner A
        sess_a = self.exam_mgr.start_exam("learner_alpha", track="Academic", module="full_mock")
        self.assertIsNotNone(sess_a)
        session_id = sess_a["session_id"]

        # Learner B attempts to submit or access Learner A's session
        unauth_submit = self.exam_mgr.submit_exam(session_id, "learner_beta", {"reading": {}})
        self.assertFalse(unauth_submit["success"])
        self.assertIn("unauthorized", unauth_submit.get("error", "").lower())

        # Learner B attempts to get Learner A's exam results
        unauth_results = self.exam_mgr.get_exam_results(session_id, "learner_beta")
        self.assertIsNone(unauth_results)

        # Verify that querying history filters strictly by learner_id
        hist_b = self.exam_mgr.list_learner_history("learner_beta")
        b_session_ids = [h["id"] for h in hist_b]
        self.assertNotIn(session_id, b_session_ids)

    # 3. Reading Assessment Accuracy Across Question Types
    def test_03_reading_marking_accuracy_and_question_types(self):
        rq = ReadingQuestionTypes

        # Test TFNG grading
        self.assertTrue(rq.grade_tfng("TRUE", "True", "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_tfng("t", "True", "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_tfng("False", "FALSE", "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_tfng("Not Given", "NG", "ev", "exp")["is_correct"])
        self.assertFalse(rq.grade_tfng("FALSE", "True", "ev", "exp")["is_correct"])

        # Test YNNG grading
        self.assertTrue(rq.grade_ynng("YES", "Yes", "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_ynng("y", "Yes", "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_ynng("NO", "No", "ev", "exp")["is_correct"])
        self.assertFalse(rq.grade_ynng("NO", "Yes", "ev", "exp")["is_correct"])

        # Test Multiple Choice grading
        self.assertTrue(rq.grade_multiple_choice("B", "B", ["A", "B", "C"], "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_multiple_choice("b", "B", ["A", "B", "C"], "ev", "exp")["is_correct"])
        self.assertFalse(rq.grade_multiple_choice("A", "B", ["A", "B", "C"], "ev", "exp")["is_correct"])

        # Test Matching
        self.assertTrue(rq.grade_matching("Matching Headings", "iii", "iii", "ev", "exp")["is_correct"])
        self.assertFalse(rq.grade_matching("Matching Headings", "iv", "iii", "ev", "exp")["is_correct"])

        # Test Completion (with whitespace and casing normalization)
        self.assertTrue(rq.grade_completion("  freshwater ecosystems  ", ["freshwater ecosystems", "freshwater ecosystem"], 2, "ev", "exp")["is_correct"])
        self.assertTrue(rq.grade_completion("FRESHWATER ECOSYSTEMS", ["freshwater ecosystems"], 2, "ev", "exp")["is_correct"])
        self.assertFalse(rq.grade_completion("saltwater ecosystems", ["freshwater ecosystems"], 2, "ev", "exp")["is_correct"])

    # 4. Listening Assessment Accuracy & Sequential Numbering (1-40)
    def test_04_listening_marking_accuracy_and_sequential_numbering(self):
        engine = self.listening_engine

        # Verify all sections have strictly sequential numbers 1..40
        section_ranges = [
            ("sec_1", 1, 10),
            ("sec_2", 11, 20),
            ("sec_3", 21, 30),
            ("sec_4", 31, 40)
        ]

        seen_nums = set()
        for sec_key, start_n, end_n in section_ranges:
            sec_data = engine.SECTIONS[sec_key]
            q_list = sec_data["questions"]
            self.assertEqual(len(q_list), 10, f"{sec_key} must contain 10 questions")
            for idx, q in enumerate(q_list):
                expected_num = start_n + idx
                self.assertEqual(q["num"], expected_num, f"Question {idx+1} in {sec_key} must have num={expected_num}")
                self.assertNotIn(q["num"], seen_nums, f"Duplicate question num {q['num']} in listening engine")
                seen_nums.add(q["num"])

        self.assertEqual(len(seen_nums), 40, "Total listening questions must be exactly 40 unique numbers")

        # Evaluate Section 1 using sequential number and question key (Surname is Sterling)
        eval_sec1 = engine.evaluate_submission("sec_1", {"listen_1": "Sterling", "1": "Sterling"})
        self.assertIn("correct_answers", eval_sec1)
        self.assertIn("total_questions", eval_sec1)
        self.assertEqual(eval_sec1["total_questions"], 10)
        self.assertGreaterEqual(eval_sec1["correct_answers"], 1)

        # Evaluate Section 2 using sequential question ID: 11 (Renovation year is 2018)
        eval_sec2 = engine.evaluate_submission("sec_2", {"11": "2018", "listen_11": "2018"})
        self.assertIn("correct_answers", eval_sec2)
        self.assertEqual(eval_sec2["total_questions"], 10)
        self.assertGreaterEqual(eval_sec2["correct_answers"], 1)

    # 5. Empty and Whitespace Answers Receive Zero Credit
    def test_05_empty_and_whitespace_answers_receive_zero_credit(self):
        rq = ReadingQuestionTypes

        # Direct question type guards
        tfng_res = rq.grade_tfng("   ", "True", "ev", "exp")
        self.assertFalse(tfng_res["is_correct"])
        self.assertTrue(tfng_res.get("is_unanswered", False))

        mcq_res = rq.grade_multiple_choice("", "B", ["A", "B", "C"], "ev", "exp")
        self.assertFalse(mcq_res["is_correct"])
        self.assertTrue(mcq_res.get("is_unanswered", False))

        comp_res = rq.grade_completion("     ", ["renewable energy"], 2, "ev", "exp")
        self.assertFalse(comp_res["is_correct"])
        self.assertTrue(comp_res.get("is_unanswered", False))

        # Reading engine passage evaluation with empty answers
        empty_reading_answers = {f"read_{i}": "   " for i in range(1, 14)}
        eval_read = self.reading_engine.evaluate_test("acad_p1", empty_reading_answers)
        self.assertEqual(eval_read["correct_answers"], 0)
        self.assertEqual(eval_read["estimated_band"], 0.0)

        # Listening engine evaluation with empty answers
        empty_listening_answers = {f"listen_{i}": "" for i in range(1, 11)}
        eval_listen = self.listening_engine.evaluate_submission("sec_1", empty_listening_answers)
        self.assertEqual(eval_listen["correct_answers"], 0)
        self.assertEqual(eval_listen["estimated_band"], 0.0)

    # 6. Duplicate Submission Protection (Idempotency)
    def test_06_duplicate_submission_protection(self):
        learner_id = "learner_idemp"
        self.auth_mgr.register_user(learner_id, "Password123!")

        session = self.exam_mgr.start_exam(learner_id, track="Academic", module="full_mock")
        session_id = session["session_id"]

        test_payload = {
            "reading": {"read_1": "TRUE", "read_2": "FALSE"},
            "listening": {"listen_1": "Sarah Jenkins"},
            "writing": {"task1_response": "Sample essay " * 30, "task2_response": "Sample argument " * 40},
            "speaking": {"part1": "I am a software engineer.", "part2": "I lived in a mountain town.", "part3": "Technology connects us."}
        }

        # First submission
        res1 = self.exam_mgr.submit_exam(session_id, learner_id, test_payload)
        self.assertTrue(res1.get("success", False))
        band_1 = res1.get("overall_band")

        # Second submission of identical session
        res2 = self.exam_mgr.submit_exam(session_id, learner_id, test_payload)
        self.assertTrue(res2.get("success", False))
        self.assertTrue(res2.get("already_submitted", False))
        self.assertEqual(res2.get("band_score"), band_1)

    # 7. Invalid Question IDs Do Not Inflate Score
    def test_07_invalid_question_ids_do_not_inflate_score(self):
        # Submit answers containing nonexistent question IDs to reading passage
        spoofed_answers = {
            "read_9999": "TRUE",
            "fake_question_bonus": "B",
            "sql_injection_test' OR 1=1 --": "answer"
        }
        eval_res = self.reading_engine.evaluate_test("acad_p1", spoofed_answers)
        self.assertEqual(eval_res["correct_answers"], 0)
        self.assertEqual(eval_res["estimated_band"], 0.0)

    # 8. Transparent Result Breakdown
    def test_08_transparent_result_breakdown(self):
        # Create session and submit package
        learner_id = "learner_breakdown"
        self.auth_mgr.register_user(learner_id, "Password123!")
        session = self.exam_mgr.start_exam(learner_id, track="Academic", module="full_mock")
        session_id = session["session_id"]

        submission = {
            "reading": {"read_1": "TRUE", "read_2": "FALSE"},
            "listening": {"listen_1": "Sarah Jenkins"}
        }
        result = self.exam_mgr.submit_exam(session_id, learner_id, submission)
        self.assertTrue(result.get("success"))

        results_data = result.get("results", {})
        read_details = results_data.get("skills", {}).get("reading", {})
        self.assertIn("correct_answers", read_details)
        self.assertIn("total_questions", read_details)
        self.assertIn("accuracy_percent", read_details)
        self.assertIn("estimated_band", read_details)
        self.assertIn("confidence_range", read_details)
        self.assertIn("scoring_rule_version", read_details)
        self.assertIn("answer_key_version", read_details)
        self.assertEqual(read_details.get("examiner_verified"), False)
        self.assertIn("disclaimer", read_details)

        # Question breakdown check
        breakdown = read_details.get("question_breakdown", [])
        self.assertGreater(len(breakdown), 0)
        first_q = breakdown[0]
        self.assertIn("question_id", first_q)
        self.assertIn("prompt", first_q)
        self.assertIn("user_answer", first_q)
        self.assertIn("accepted_answers", first_q)
        self.assertIn("is_correct", first_q)
        self.assertIn("explanation", first_q)

    # 9. Historical Result Reproducibility
    def test_09_historical_result_reproducibility(self):
        learner_id = "learner_repro"
        self.auth_mgr.register_user(learner_id, "Password123!")
        session = self.exam_mgr.start_exam(learner_id, track="General Training", module="full_mock")
        session_id = session["session_id"]

        submission = {
            "reading": {"read_1": "TRUE"},
            "listening": {"listen_1": "Sarah Jenkins"}
        }
        orig_res = self.exam_mgr.submit_exam(session_id, learner_id, submission)
        self.assertTrue(orig_res.get("success"))

        # Retrieve through exam results endpoint
        retrieved_res = self.exam_mgr.get_exam_results(session_id, learner_id)
        self.assertIsNotNone(retrieved_res)
        self.assertEqual(retrieved_res.get("band_score"), orig_res.get("overall_band"))
        self.assertEqual(retrieved_res.get("results"), orig_res.get("results"))

        # Fetch session list directly from db
        history = self.exam_mgr.list_learner_history(learner_id)
        self.assertGreater(len(history), 0)
        found_hist = next((h for h in history if h["id"] == session_id), None)
        self.assertIsNotNone(found_hist)
        self.assertEqual(found_hist["status"], "submitted")

    # 10. Writing Evaluation Hardening (Empty = Band 0.0, Underlength Ceilings)
    def test_10_writing_empty_and_underlength_protection(self):
        evaluator = self.criteria_evaluator

        # Empty response -> Band 0.0
        empty_eval = evaluator.evaluate_writing(
            task_type="task_2", track="Academic", text="",
            tr_score=0.0, cc_score=0.0, lr_score=0.0, gra_score=0.0, word_count=0
        )
        self.assertEqual(empty_eval["estimated_band"], 0.0)
        self.assertEqual(empty_eval["word_count"], 0)

        # Extremely short response (< 25 words) -> Max 1.5
        micro_eval = evaluator.evaluate_writing(
            task_type="task_2", track="Academic",
            text="In my opinion technology is very good and helps people every single day.",
            tr_score=5.0, cc_score=5.0, lr_score=5.0, gra_score=5.0, word_count=13
        )
        self.assertLessEqual(micro_eval["estimated_band"], 1.5)

        # Short response (< 50 words) -> Max 2.5
        short_text = "I believe that higher education should be free for every citizen in modern society. " \
                     "When people study they can improve economic production and develop sustainable technology. " \
                     "Therefore governments should allocate budget."
        short_eval = evaluator.evaluate_writing(
            task_type="task_2", track="Academic", text=short_text,
            tr_score=6.0, cc_score=6.0, lr_score=6.0, gra_score=6.0, word_count=35
        )
        self.assertLessEqual(short_eval["estimated_band"], 2.5)

        # High-level essay evaluator on empty essay
        essay_eval = self.writing_evaluator.evaluate_essay("acad_t2_stem", "")
        self.assertEqual(essay_eval["estimated_band"], 0.0)

        # Verify automated scoring disclaimer
        self.assertIn("disclaimer", short_eval)
        self.assertIn("diagnostic estimate", short_eval["assessment_uncertainty_note"].lower())

    # 11. Speaking Evaluation Hardening (Empty = Band 0.0, Limitation Disclosure)
    def test_11_speaking_empty_and_non_acoustic_disclosure(self):
        # Empty transcript evaluation via SpeakingExaminer
        empty_spk = self.speaking_examiner.evaluate_spoken_response("")
        self.assertEqual(empty_spk["estimated_band"], 0.0)

        # Sample transcript evaluation via CriteriaEvaluator
        spk_eval = self.criteria_evaluator.evaluate_speaking(
            fc_score=6.0, lr_score=6.5, gra_score=6.0, p_score=6.0
        )
        self.assertEqual(spk_eval["estimated_band"], 6.0)

        # Verify non-acoustic pronunciation limitation disclosure
        self.assertIn("pronunciation_limitation", spk_eval)
        self.assertIn("transcript", spk_eval["pronunciation_limitation"].lower())
        self.assertIn("acoustic_disclaimer", spk_eval)

    # 12. Automated Mistake Book Logging on Assessment Failure
    def test_12_mistake_book_logging_on_test_failure(self):
        learner_id = "learner_mistakes"
        self.auth_mgr.register_user(learner_id, "Password123!")

        # Log a mistake for an incorrect reading answer
        rec = self.mistake_book.record_error(
            learner_id=learner_id,
            skill="reading",
            category="factual_inference",
            original_text="FALSE",
            corrected_text="TRUE",
            explanation="The passage explicitly states in paragraph 2 that wetlands act as natural filters."
        )
        self.assertIsNotNone(rec.get("id"))
        self.assertEqual(rec.get("status"), "needs_improvement")

        mistakes = self.mistake_book.get_mistakes(learner_id=learner_id, limit=10)
        self.assertGreater(len(mistakes), 0)
        last_m = mistakes[0]
        self.assertEqual(last_m["original_text"], "FALSE")
        self.assertEqual(last_m["corrected_text"], "TRUE")
        self.assertIn("wetlands", last_m["explanation"].lower())

    # 13. Student Dashboard Analytics, Honest Empty States, and Recommendations
    def test_13_student_dashboard_empty_states_and_recommendations(self):
        learner_id = "learner_newbie"
        self.auth_mgr.register_user(learner_id, "Password123!")

        # Brand new learner dashboard
        dash = self.analytics.get_dashboard_data(learner_id)
        self.assertFalse(dash["has_assessment_data"])
        self.assertIn("empty_state_notices", dash)
        self.assertGreater(len(dash["empty_state_notices"]), 0)
        self.assertIn("recommended_next_activity", dash)
        self.assertEqual(dash["recommended_next_activity"]["module"], "diagnostic")
        self.assertIn("diagnostic", dash["recommended_next_activity"]["title"].lower())

        # Complete a diagnostic test
        self.test_repo.record_result(
            learner_id=learner_id,
            test_type="reading",
            overall_band=5.0,
            reading_band=5.0,
            details={"feedback": "Fair understanding of basic texts, requires work on inference."}
        )

        # Refresh dashboard
        updated_dash = self.analytics.get_dashboard_data(learner_id)
        self.assertTrue(updated_dash["has_assessment_data"])
        self.assertEqual(updated_dash["reading_performance"]["attempts"], 1)
        self.assertEqual(updated_dash["reading_performance"]["last_band"], 5.0)

    # 14. Educator UI Feature Simplification
    def test_14_educator_feature_simplification(self):
        # Verify index.html contains style="display: none;" on educator elements by default
        index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "static", "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        self.assertIn('id="educatorNavGroup" style="display: none;"', html_content)
        self.assertIn('id="educatorFilterBtn" style="display: none;"', html_content)

        # Verify app.js contains role-based protection for educator tabs
        app_js_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "static", "app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            js_content = f.read()

        self.assertIn('!isEducator && ["teacher", "doublemark", "beta"].includes(cleanId)', js_content)
        self.assertIn('eduNav.style.display = isEducator ? "" : "none";', js_content)


if __name__ == "__main__":
    unittest.main()
