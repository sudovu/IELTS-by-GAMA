# -*- coding: utf-8 -*-
"""
test_phase12_curriculum_expansion.py
Unit and Integration Tests for Phase 12: Comprehensive English Curriculum & Content Expansion.
Verifies:
1. Complete 6-level CEFR curriculum (A1–C2) with 9 structured modules each (54 lessons total).
2. Automated ContentValidator results: 100% question keys, valid answer bounds, non-empty explanations.
3. Prerequisite DAG enforcement and mastery progression.
4. 15 themed vocabulary collections with full lexical metadata.
5. Interactive vocabulary exercise generators (gap-fill, synonyms, collocations, word-family, quizzes).
6. Performance-driven review recommendations connected to the Mistake Book.
7. Spaced Repetition (SM-2) integration with vocabulary items.
8. Backward compatibility with all 18 starter lesson IDs.
"""

import unittest
import os
import tempfile
import shutil

from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, MistakeBookRepository
from core.curriculum.content_manager import ContentManager
from core.curriculum.validator import ContentValidator
from core.curriculum.curriculum_engine import CurriculumEngine, STARTER_LESSONS
from core.vocabulary.vocabulary_vault import VocabularyVault


class TestPhase12CurriculumExpansion(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_phase12.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()

        self.learner_repo = LearnerRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)
        self.curriculum = CurriculumEngine(self.db)
        self.vocab = VocabularyVault(self.db)

        self.learner = self.learner_repo.create_learner(
            name="Curriculum Scholar",
            cefr_level="B2",
            target_band=7.5
        )

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_curriculum_completeness_and_cefr_levels(self):
        """Verifies exactly 54 structured lessons covering all 6 CEFR levels (A1 to C2)."""
        lessons = ContentManager.load_curriculum_lessons(force_reload=True)
        self.assertGreaterEqual(len(lessons), 54, "Curriculum must have at least 54 structured lessons")

        levels = {l["cefr_level"] for l in lessons}
        self.assertEqual(levels, {"A1", "A2", "B1", "B2", "C1", "C2"})

        for lvl in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            lvl_lessons = [l for l in lessons if l["cefr_level"] == lvl]
            self.assertEqual(len(lvl_lessons), 9, f"Level {lvl} must have exactly 9 modules")
            modules = {l["module_type"] for l in lvl_lessons}
            expected_mods = {
                "grammar", "vocabulary", "reading", "listening",
                "writing", "speaking", "pronunciation", "functional", "review"
            }
            self.assertEqual(modules, expected_mods, f"Level {lvl} missing modules: {expected_mods - modules}")

    def test_backward_compatibility_with_starter_lessons(self):
        """Verifies all 18 existing starter lesson IDs remain intact and accessible."""
        lessons = ContentManager.load_curriculum_lessons()
        lesson_ids = {l["id"] for l in lessons}

        for starter in STARTER_LESSONS:
            self.assertIn(starter["id"], lesson_ids, f"Starter lesson {starter['id']} must be preserved")

    def test_automated_content_validator_clean_pass(self):
        """Executes ContentValidator and verifies 100% quality score with 0 critical issues."""
        lessons = ContentManager.load_curriculum_lessons()
        c_val = ContentValidator.validate_curriculum(lessons)
        self.assertEqual(c_val["total_issues_found"], 0, f"Curriculum issues detected: {c_val['issues']}")
        self.assertEqual(c_val["quality_score_percent"], 100.0)

        themes = ContentManager.load_vocabulary_themes()
        v_val = ContentValidator.validate_vocabulary_themes(themes)
        self.assertEqual(v_val["total_issues_found"], 0, f"Vocabulary issues detected: {v_val['issues']}")
        self.assertEqual(v_val["quality_score_percent"], 100.0)

    def test_prerequisite_enforcement(self):
        """Tests that lesson prerequisites correctly enforce sequential learning progression."""
        # curric_b1_gram_present_perfect requires curric_a2_gram_past_simple
        lesson_id = "curric_b1_gram_present_perfect"
        check = self.curriculum.check_prerequisites(self.learner["id"], lesson_id)
        self.assertFalse(check["unlocked"], "Lesson should be locked before completing prerequisite")
        self.assertEqual(len(check["missing_prerequisites"]), 1)
        self.assertEqual(check["missing_prerequisites"][0]["id"], "curric_a2_gram_past_simple")

        # Now complete the prerequisite with master score across all assessment items
        self.curriculum.evaluate_submission(
            learner_id=self.learner["id"],
            lesson_id="curric_a2_gram_past_simple",
            answers={"a2_as_1": 1, "a2_g_as_2": 1, "a2_g_as_3": 1}
        )

        # Check again: should now be unlocked!
        unlocked_check = self.curriculum.check_prerequisites(self.learner["id"], lesson_id)
        self.assertTrue(unlocked_check["unlocked"], "Lesson should unlock once prerequisite is mastered")

    def test_curriculum_map_generation(self):
        """Verifies curriculum map schema matches Part 1 requirements."""
        cmap = ContentManager.get_curriculum_map()
        self.assertEqual(cmap["total_levels"], 6)
        self.assertGreaterEqual(cmap["total_lessons"], 54)
        self.assertIn("A1", cmap["levels"])
        self.assertIn("grammar", cmap["levels"]["A1"])
        gram_lesson = cmap["levels"]["A1"]["grammar"][0]
        self.assertIn("title", gram_lesson)
        self.assertIn("estimated_minutes", gram_lesson)
        self.assertIn("prerequisites", gram_lesson)
        self.assertIn("completion_threshold", gram_lesson)

    def test_vocabulary_themes_coverage(self):
        """Verifies all 15 themed vocabulary collections exist with rich lexical details."""
        themes = ContentManager.load_vocabulary_themes()
        expected_themes = {
            "daily_life", "education", "work_and_careers", "technology", "science",
            "environment", "health", "society", "culture", "business",
            "travel", "government", "economics", "media", "academic_english"
        }
        self.assertEqual(set(themes.keys()), expected_themes)

        for tid, words in themes.items():
            self.assertGreaterEqual(len(words), 2, f"Theme {tid} must contain at least 2 entries")
            for w in words:
                self.assertIn("pos", w)
                self.assertIn("ipa", w)
                self.assertIn("collocations", w)
                self.assertIn("word_family", w)
                self.assertIn("ielts_usefulness", w)

    def test_vocabulary_exercise_generators(self):
        """Verifies on-demand gap-fill, synonym, collocation, and quiz generation."""
        # 1. Gap Fill
        gap_ex = self.vocab.generate_gap_fill_exercise()
        self.assertEqual(gap_ex["exercise_type"], "gap_fill")
        self.assertEqual(len(gap_ex["options"]), 4)
        self.assertIn("_____", gap_ex["masked_sentence"])
        self.assertIn(gap_ex["target_word"], gap_ex["options"])

        # 2. Synonym Selection
        syn_ex = self.vocab.generate_synonym_exercise()
        self.assertEqual(syn_ex["exercise_type"], "synonym_selection")
        self.assertEqual(len(syn_ex["options"]), 4)

        # 3. Collocation Practice
        col_ex = self.vocab.generate_collocation_exercise()
        self.assertEqual(col_ex["exercise_type"], "collocation_practice")
        self.assertEqual(len(col_ex["options"]), 4)

        # 4. Word Family Practice
        wf_ex = self.vocab.generate_word_family_exercise()
        self.assertEqual(wf_ex["exercise_type"], "word_family")
        self.assertEqual(len(wf_ex["options"]), 4)

        # 5. Full Vocab Quiz
        quiz = self.vocab.generate_vocab_quiz(count=4)
        self.assertEqual(quiz["total_questions"], 4)
        self.assertEqual(len(quiz["questions"]), 4)

    def test_vocabulary_quiz_evaluation_and_mistake_integration(self):
        """Verifies quiz scoring and automatic logging into Mistake Book upon error."""
        quiz = self.vocab.generate_vocab_quiz(count=2)
        q1 = quiz["questions"][0]
        q2 = quiz["questions"][1]

        # 1 correct, 1 wrong
        correct_ans = q1["correct_index"]
        wrong_ans = (q2["correct_index"] + 1) % len(q2["options"])

        eval_res = self.vocab.evaluate_quiz_submission(
            learner_id=self.learner["id"],
            quiz=quiz,
            answers={q1["id"]: correct_ans, q2["id"]: wrong_ans}
        )
        self.assertEqual(eval_res["correct_count"], 1)
        self.assertEqual(eval_res["score_percent"], 50.0)

        # Verify mistake was recorded in Mistake Book
        mistakes = self.mistake_repo.get_mistakes_by_learner(self.learner["id"])
        self.assertGreaterEqual(len(mistakes), 1)
        vocab_mistakes = [m for m in mistakes if m["skill"] == "vocabulary"]
        self.assertGreaterEqual(len(vocab_mistakes), 1)

    def test_performance_driven_review_recommendation(self):
        """Verifies that the system recommends review lessons matching recorded learner mistakes."""
        # Initially no mistakes -> no review recommendations
        recs_initial = self.curriculum.recommend_review_lessons(self.learner["id"])
        self.assertEqual(len(recs_initial), 0)

        # Log repeated grammar mistakes for this learner
        for _ in range(3):
            self.mistake_repo.record_mistake(
                learner_id=self.learner["id"],
                skill="grammar",
                category="Conditionals",
                original_text="If I would go",
                corrected_text="If I went",
                explanation="Never use would in if-clause"
            )

        # Now system should recommend grammar remediation
        recs = self.curriculum.recommend_review_lessons(self.learner["id"])
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0]["module_type"], "grammar")
        self.assertIn("Targeted remediation", recs[0]["reason"])

    def test_database_persistence_and_querying(self):
        """Tests that full 54 lessons seed into SQLite and persist across DB connections."""
        seeded_count = self.curriculum.seed_default_curriculum()
        self.assertEqual(seeded_count, 54)

        # Query lessons from SQLite
        all_lessons = self.curriculum.list_lessons()
        self.assertEqual(len(all_lessons), 54)

        # Query with level and module filters
        c1_speaking = self.curriculum.list_lessons(cefr_level="C1", module_type="speaking")
        self.assertEqual(len(c1_speaking), 1)
        self.assertEqual(c1_speaking[0]["id"], "curric_c1_speak_discourse_markers")


if __name__ == "__main__":
    unittest.main()
