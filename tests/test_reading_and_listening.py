"""
Unit tests for Reading and Listening engines.
"""

import unittest
from core.reading.reading_engine import ReadingEngine
from core.reading.question_types import ReadingQuestionTypes
from core.listening.listening_engine import ListeningEngine
from core.listening.answer_checker import ListeningAnswerChecker


class TestReadingAndListening(unittest.TestCase):
    def test_reading_tfng_grading(self):
        res = ReadingQuestionTypes.grade_tfng(
            user_answer="F",
            correct_answer="False",
            passage_evidence="evidence quote",
            explanation="explanation note"
        )
        self.assertTrue(res["is_correct"])

    def test_reading_completion_word_limits(self):
        # Exceeds max words limit
        res = ReadingQuestionTypes.grade_completion(
            user_answer="the big black smokers chimney",
            acceptable_answers=["black smokers"],
            max_words=2,
            passage_evidence="...",
            explanation="..."
        )
        self.assertFalse(res["is_correct"])
        self.assertIn("Exceeded word count", res["explanation"])

    def test_reading_engine_full_evaluation(self):
        user_answers = {
            1: "False",
            2: "False",
            3: "False",
            4: "black smokers"
        }
        report = ReadingEngine.evaluate_test("acad_p1", user_answers)
        self.assertEqual(report["correct_answers"], 4)
        self.assertGreaterEqual(report["estimated_band"], 7.0)
        self.assertIn("Practice estimate only", report["disclaimer"])

    def test_listening_answer_checker_and_distractors(self):
        # Normalization of numbers and case
        is_correct, _ = ListeningAnswerChecker.check_answer("two hundred ten", ["210", "two hundred and ten"], max_words=4)
        is_correct2, _ = ListeningAnswerChecker.check_answer("210", ["210"])
        self.assertTrue(is_correct2)

        # Full listening evaluation
        user_answers = {
            1: "Sterling",
            2: "en-suite",
            3: "210",
            4: "September"
        }
        report = ListeningEngine.evaluate_submission("sec_1", user_answers)
        self.assertEqual(report["correct_answers"], 4)
        self.assertIn("CLASSIC IELTS DISTRACTOR", report["results"][2]["distractor_analysis"])


if __name__ == "__main__":
    unittest.main()
