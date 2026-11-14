"""
Unit tests for English Learning Academy (CurriculumEngine) and GrammarEngine expansion.
Verifies CEFR A1-C2 lessons, progress tracking, interactive evaluation,
regex diagnostics, and cloze fill-up drills.
"""

import unittest
import tempfile
import os
from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository
from core.curriculum.curriculum_engine import CurriculumEngine, STARTER_LESSONS
from core.grammar.grammar_engine import GrammarEngine


class TestCurriculumAndGrammar(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()
        self.curriculum = CurriculumEngine(self.db)
        self.curriculum.seed_default_curriculum()
        self.learner_repo = LearnerRepository(self.db)
        self.learner = self.learner_repo.create_learner(name="Curriculum Test User", cefr_level="B2")

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_curriculum_lessons_seeded_across_cefr(self):
        lessons = self.curriculum.list_lessons()
        self.assertGreaterEqual(len(lessons), 18)

        levels = {l["cefr_level"] for l in lessons}
        self.assertEqual(levels, {"A1", "A2", "B1", "B2", "C1", "C2"})

        # Check filtering by level and module
        b2_lessons = self.curriculum.list_lessons(cefr_level="B2")
        self.assertGreaterEqual(len(b2_lessons), 3)

        grammar_lessons = self.curriculum.list_lessons(module_type="grammar")
        self.assertGreaterEqual(len(grammar_lessons), 6)

    def test_get_lesson_structure(self):
        lesson = self.curriculum.get_lesson("curric_b2_gram_conditionals", learner_id=self.learner["id"])
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson["cefr_level"], "B2")
        self.assertEqual(lesson["module_type"], "grammar")
        self.assertIn("Hypothetical Conditionals", lesson["title"])
        self.assertGreater(len(lesson["objectives"]), 0)
        self.assertIn("explanation_markdown", lesson)
        self.assertGreater(len(lesson["examples"]), 0)
        self.assertGreater(len(lesson["guided_exercises"]), 0)
        self.assertGreater(len(lesson["interactive_practice"]), 0)
        self.assertGreater(len(lesson["assessment"]), 0)
        self.assertEqual(lesson["learner_progress"]["status"], "not_started")

    def test_evaluate_submission_scoring_and_progress(self):
        lesson_id = "curric_a1_gram_present_simple"
        lesson = self.curriculum.get_lesson(lesson_id)
        assessments = lesson["assessment"]

        # Submit all correct answers
        correct_answers = {q["id"]: q["correct_index"] for q in assessments}
        result = self.curriculum.evaluate_submission(self.learner["id"], lesson_id, correct_answers)

        self.assertTrue(result["success"])
        self.assertEqual(result["score"], 100.0)
        self.assertEqual(result["status"], "mastered")
        self.assertEqual(result["correct_count"], len(assessments))

        # Verify progress recorded in DB
        updated_lesson = self.curriculum.get_lesson(lesson_id, learner_id=self.learner["id"])
        self.assertEqual(updated_lesson["learner_progress"]["status"], "mastered")
        self.assertEqual(updated_lesson["learner_progress"]["score"], 100.0)

    def test_evaluate_submission_mistakes_logged(self):
        lesson_id = "curric_a1_gram_present_simple"
        # Submit deliberately wrong answers
        wrong_answers = {"a1_as_1": 99, "a1_as_2": 99}
        result = self.curriculum.evaluate_submission(self.learner["id"], lesson_id, wrong_answers)

        self.assertTrue(result["success"])
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["status"], "needs_review")

        # Verify mistakes were logged into mistake book (either distinct rows or incremented recurrence)
        mistakes = self.curriculum.mistake_repo.get_mistakes_by_learner(self.learner["id"])
        total_occurrences = sum(m["recurrence_count"] for m in mistakes)
        self.assertGreaterEqual(total_occurrences, 2)

    def test_grammar_engine_expanded_drills(self):
        drills = GrammarEngine.get_fill_up_drills()
        self.assertGreaterEqual(len(drills), 25)

        # Test evaluation of a cloze drill
        res_correct = GrammarEngine.evaluate_fill_up("fill_cond_1", "had invested")
        self.assertTrue(res_correct["is_correct"])

        res_wrong = GrammarEngine.evaluate_fill_up("fill_cond_1", "invested")
        self.assertFalse(res_wrong["is_correct"])

    def test_grammar_engine_expanded_error_diagnostics(self):
        self.assertGreaterEqual(len(GrammarEngine.ERROR_RULES), 25)

        # Test diagnostic patterns
        diag_did_went = GrammarEngine.check_sentence("They did not went to the library.")
        self.assertTrue(any(d["category"] == "Tenses" for d in diag_did_went))

        diag_much_people = GrammarEngine.check_sentence("Much people agree with this policy.")
        self.assertTrue(any(d["category"] == "Determiners & Quantifiers" for d in diag_much_people))

        diag_look_forward = GrammarEngine.check_sentence("I look forward to hear your response.")
        self.assertTrue(any(d["category"] == "Gerunds & Infinitives" for d in diag_look_forward))


if __name__ == "__main__":
    unittest.main()
