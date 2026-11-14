"""
Unit tests for Phase 4: IELTS Reading and Listening Examination Expansion.
Covers Academic and General Training reading passages, 14 question types,
examination mode answer concealment, full mock exam generators,
and 40-question listening sections with distractor analysis.
"""

import unittest
import tempfile
import os
from core.reading.reading_engine import ReadingEngine
from core.reading.question_types import ReadingQuestionTypes
from core.listening.listening_engine import ListeningEngine
from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, TestResultRepository
from core.progress.analytics import LearningAnalytics


class TestPhase4ReadingListening(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()
        self.learner_repo = LearnerRepository(self.db)
        self.learner = self.learner_repo.create_learner(name="Exam Candidate", track="Academic")

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_reading_passages_both_tracks(self):
        passages = ReadingEngine.list_passages()
        self.assertGreaterEqual(len(passages), 6)

        acad_passages = ReadingEngine.list_passages(track="Academic")
        self.assertEqual(len(acad_passages), 3)

        gt_passages = ReadingEngine.list_passages(track="General Training")
        self.assertEqual(len(gt_passages), 3)

    def test_reading_exam_mode_conceals_answers(self):
        # Exam mode: show_answers=False
        passage_exam = ReadingEngine.get_passage("acad_p1", show_answers=False)
        self.assertIsNotNone(passage_exam)
        self.assertNotIn("synonym_table", passage_exam)
        for q in passage_exam["questions"]:
            self.assertNotIn("correct", q)
            self.assertNotIn("acceptable", q)
            self.assertNotIn("evidence", q)
            self.assertNotIn("explanation", q)

        # Review mode: show_answers=True
        passage_review = ReadingEngine.get_passage("acad_p1", show_answers=True)
        self.assertIn("synonym_table", passage_review)
        for q in passage_review["questions"]:
            self.assertTrue("correct" in q or "acceptable" in q)
            self.assertIn("evidence", q)
            self.assertIn("explanation", q)

    def test_reading_question_types_evaluations(self):
        # 1. TFNG
        res_tfng = ReadingQuestionTypes.grade_tfng("False", "False", "evidence text", "explanation text")
        self.assertTrue(res_tfng["is_correct"])

        res_tfng_alias = ReadingQuestionTypes.grade_tfng("f", "False", "evidence", "explanation")
        self.assertTrue(res_tfng_alias["is_correct"])

        # 2. YNNG
        res_ynng = ReadingQuestionTypes.grade_ynng("Yes", "Yes", "author claims", "explanation")
        self.assertTrue(res_ynng["is_correct"])

        # 3. MCQ with distractor analysis
        distractors = {"A": "Too narrow", "C": "Contradicts paragraph 2"}
        res_mcq = ReadingQuestionTypes.grade_multiple_choice("A", "B", "evidence", "Correct is B.", distractors)
        self.assertFalse(res_mcq["is_correct"])
        self.assertIn("Why 'A' is a distractor", res_mcq["explanation"])

        # 4. Matching Headings
        res_match = ReadingQuestionTypes.grade_matching("Matching Headings", "iv", "iv", "evidence", "Correct heading")
        self.assertTrue(res_match["is_correct"])

        # 5. Completion with strict word count
        res_comp_exceed = ReadingQuestionTypes.grade_completion("more than two words entered", ["black smokers"], max_words=2, passage_evidence="ev", explanation="exp")
        self.assertFalse(res_comp_exceed["is_correct"])
        self.assertIn("Exceeded word count limit", res_comp_exceed["explanation"])

        res_comp_ok = ReadingQuestionTypes.grade_completion("black smokers", ["black smokers"], max_words=2, passage_evidence="ev", explanation="exp")
        self.assertTrue(res_comp_ok["is_correct"])

    def test_reading_full_mock_generation(self):
        acad_mock = ReadingEngine.generate_full_mock(track="Academic")
        self.assertEqual(acad_mock["track"], "Academic")
        self.assertEqual(len(acad_mock["passages"]), 3)
        self.assertEqual(acad_mock["time_limit_minutes"], 60)

        gt_mock = ReadingEngine.generate_full_mock(track="General Training")
        self.assertEqual(gt_mock["track"], "General Training")
        self.assertEqual(len(gt_mock["passages"]), 3)

    def test_listening_sections_expanded_to_40_questions(self):
        sections = ListeningEngine.list_sections()
        self.assertEqual(len(sections), 4)

        total_questions = sum(s["question_count"] for s in sections)
        self.assertEqual(total_questions, 40)

        for s in sections:
            self.assertEqual(s["question_count"], 10)

    def test_listening_full_mock_generation(self):
        mock = ListeningEngine.generate_full_listening_mock(show_transcripts=False)
        self.assertEqual(mock["total_questions"], 40)
        self.assertEqual(len(mock["sections"]), 4)
        for sec in mock["sections"]:
            self.assertNotIn("audio_script", sec)

    def test_listening_evaluation_with_distractor_analysis(self):
        # Submit section 1 answers
        answers = {
            1: "Sterling",
            2: "en-suite",
            3: "210",
            4: "September",
            5: "Science",
            6: "self",
            7: "350",
            8: "48",
            9: "4829",
            10: "passport"
        }
        res = ListeningEngine.evaluate_submission("sec_1", answers)
        self.assertEqual(res["total_questions"], 10)
        self.assertEqual(res["correct_answers"], 10)
        self.assertEqual(res["estimated_band"], 9.0)
        self.assertIn("results", res)
        self.assertTrue(all(r["is_correct"] for r in res["results"]))

    def test_exam_result_persisted_updates_radar(self):
        test_repo = TestResultRepository(self.db)
        test_repo.record_result(
            learner_id=self.learner["id"],
            test_type="reading",
            track="Academic",
            overall_band=8.0,
            reading_band=8.0,
            details={"notes": "Excellent Academic Reading mock"}
        )
        test_repo.record_result(
            learner_id=self.learner["id"],
            test_type="listening",
            track="Academic",
            overall_band=7.5,
            listening_band=7.5,
            details={"notes": "Strong Section 1-4 performance"}
        )

        analytics = LearningAnalytics(self.db)
        dash = analytics.get_dashboard_data(self.learner["id"])
        radar = dash["skills_radar"]

        self.assertEqual(radar["Reading"], 8.0)
        self.assertEqual(radar["Listening"], 7.5)


if __name__ == "__main__":
    unittest.main()
