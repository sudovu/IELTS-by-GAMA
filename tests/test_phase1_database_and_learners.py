"""
Unit tests for Phase 1: Database Integrity, Migrations, and Learner Management.
"""

import unittest
import tempfile
import os
import json
from core.database.db_manager import DatabaseManager
from core.database.migrations import MigrationManager
from core.database.repositories import (
    LearnerRepository,
    CurriculumRepository,
    VocabularyVaultRepository,
    ExamSessionRepository,
    WritingDraftRepository,
    AIConversationRepository
)


class TestPhase1DatabaseAndLearners(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_phase1.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()
        self.learner_repo = LearnerRepository(self.db)
        self.curriculum_repo = CurriculumRepository(self.db)
        self.vocab_repo = VocabularyVaultRepository(self.db)
        self.exam_repo = ExamSessionRepository(self.db)
        self.writing_repo = WritingDraftRepository(self.db)
        self.ai_conv_repo = AIConversationRepository(self.db)

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    def test_migration_idempotence(self):
        mm = MigrationManager(self.db)
        # Migrations already ran on init_schema; running again should apply 0
        newly_applied = mm.run_migrations()
        self.assertEqual(newly_applied, 0)

        # Check all tables exist
        with self.db.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = {row[0] for row in cursor.fetchall()}
            expected = {
                "learners", "mistake_book", "srs_items", "knowledge_base",
                "study_plans", "test_results", "smart_cache", "system_settings",
                "schema_migrations", "curriculum_lessons", "lesson_progress",
                "vocabulary_vault", "exam_sessions", "writing_drafts", "ai_conversations"
            }
            self.assertTrue(expected.issubset(tables))

    def test_learner_lifecycle_and_extended_fields(self):
        # 1. Default learner
        default_l = self.learner_repo.get_or_create_default()
        self.assertEqual(default_l["id"], "default_learner")
        self.assertEqual(default_l["target_band"], 7.0)

        # 2. Create custom learner with extended fields
        custom_l = self.learner_repo.create_learner(
            name="Aarav Sharma",
            target_band=8.0,
            current_band=6.5,
            cefr_level="B2",
            track="Academic",
            daily_minutes=45,
            target_exam_date="2027-01-15",
            native_language="Nepali",
            target_sub_skills=["Writing Task 2", "Speaking Part 3"],
            notes="Focusing on complex sentence structures."
        )
        self.assertTrue(custom_l["id"].startswith("learner_"))
        self.assertEqual(custom_l["name"], "Aarav Sharma")
        self.assertEqual(custom_l["target_exam_date"], "2027-01-15")
        self.assertEqual(custom_l["native_language"], "Nepali")
        sub_skills = json.loads(custom_l["target_sub_skills"])
        self.assertIn("Writing Task 2", sub_skills)

        # 3. Update profile
        updated = self.learner_repo.update_profile(custom_l["id"], {
            "current_band": 7.0,
            "cefr_level": "C1",
            "notes": "Diagnostic passed with B2->C1 upgrade."
        })
        self.assertEqual(updated["current_band"], 7.0)
        self.assertEqual(updated["cefr_level"], "C1")
        self.assertEqual(updated["notes"], "Diagnostic passed with B2->C1 upgrade.")

        # 4. List all learners
        all_learners = self.learner_repo.list_all_learners()
        self.assertGreaterEqual(len(all_learners), 2)
        ids = [l["id"] for l in all_learners]
        self.assertIn("default_learner", ids)
        self.assertIn(custom_l["id"], ids)

        # 5. Delete custom learner
        deleted = self.learner_repo.delete_learner(custom_l["id"])
        self.assertTrue(deleted)
        self.assertIsNone(self.learner_repo.get_learner(custom_l["id"]))

    def test_curriculum_and_progress_repository(self):
        # Insert lesson
        lesson = self.curriculum_repo.upsert_lesson(
            lesson_id="grammar_a1_01",
            cefr_level="A1",
            module_type="grammar",
            title="Present Simple: Affirmative & Negative",
            order_index=1,
            objectives=["Understand subject-verb agreement for he/she/it.", "Form negative sentences with don't/doesn't."],
            explanation_markdown="Use present simple for permanent states and routines.",
            examples=[{"sentence": "I live in London.", "explanation": "Permanent state."}],
            guided_exercises=[{"prompt": "He _____ (play) football.", "answer": "plays"}],
            interactive_practice=[{"prompt": "She _____ (not/like) coffee.", "answer": "doesn't like"}],
            assessment=[{"q": 1, "question": "They _____ to school.", "options": ["walk", "walks"], "correct": "walk"}]
        )
        self.assertEqual(lesson["id"], "grammar_a1_01")
        self.assertEqual(len(lesson["objectives"]), 2)

        # List lessons
        lessons_a1 = self.curriculum_repo.list_lessons(cefr_level="A1")
        self.assertEqual(len(lessons_a1), 1)

        # Record progress
        prog = self.curriculum_repo.record_progress(
            learner_id="default_learner",
            lesson_id="grammar_a1_01",
            score=0.95,
            status="completed"
        )
        self.assertEqual(prog["status"], "completed")
        self.assertEqual(prog["score"], 0.95)

        # Fetch progress
        user_prog = self.curriculum_repo.get_learner_progress("default_learner")
        self.assertEqual(len(user_prog), 1)
        self.assertEqual(user_prog[0]["title"], "Present Simple: Affirmative & Negative")

    def test_vocabulary_vault_repository(self):
        word = self.vocab_repo.upsert_word(
            word="ameliorate",
            pos="verb",
            cefr_level="C2",
            band_tier="Band 8-9",
            simple_definition="To make something bad or unsatisfactory better.",
            advanced_definition="To improve or mitigate a suboptimal condition through deliberate intervention.",
            example_sentences=["Targeted social spending can ameliorate regional economic disparities."],
            synonyms=["improve", "mitigate", "alleviate", "enhance"],
            antonyms=["exacerbate", "worsen", "aggravate"],
            word_family={"noun": "amelioration", "verb": "ameliorate", "adjective": "ameliorative"},
            collocations=["ameliorate the situation", "ameliorate living conditions", "ameliorate poverty"],
            common_mistakes=["Do not use 'ameliorate' for things that are already positive."],
            pronunciation="uh-MEE-lee-uh-rayt",
            ipa="/əˈmiːl.jə.reɪt/",
            academic_usage="Academic Task 2 solutions paragraph."
        )
        self.assertEqual(word["word"], "ameliorate")
        self.assertEqual(word["pos"], "verb")
        self.assertIn("improve", word["synonyms"])

        # Search
        searched = self.vocab_repo.search_words("mitigate")
        self.assertEqual(len(searched), 1)
        self.assertEqual(searched[0]["word"], "ameliorate")

    def test_exam_session_lifecycle(self):
        # Start session
        session = self.exam_repo.start_session(
            learner_id="default_learner",
            module="reading",
            track="Academic",
            time_limit_seconds=3600
        )
        self.assertEqual(session["status"], "in_progress")
        self.assertEqual(session["time_limit_seconds"], 3600)

        # Update answers
        updated = self.exam_repo.update_answers(
            session_id=session["id"],
            answers={"1": "False", "2": "True"},
            time_spent_seconds=600
        )
        self.assertEqual(updated["answers"]["1"], "False")
        self.assertEqual(updated["time_spent_seconds"], 600)

        # Complete session
        completed = self.exam_repo.complete_session(
            session_id=session["id"],
            results={"correct_answers": 32, "total_questions": 40},
            band_score=7.5
        )
        self.assertEqual(completed["status"], "submitted")
        self.assertEqual(completed["band_score"], 7.5)

    def test_writing_draft_and_evaluation(self):
        draft = self.writing_repo.save_draft(
            learner_id="default_learner",
            prompt_id="acad_t2_stem",
            task_type="task_2",
            track="Academic",
            draft_text="In the contemporary era, secondary educational curricula...",
            word_count=285
        )
        self.assertEqual(draft["status"], "draft")
        self.assertEqual(draft["word_count"], 285)

        evaluated = self.writing_repo.record_evaluation(
            draft_id=draft["id"],
            ta_score=7.5,
            cc_score=7.0,
            lr_score=7.5,
            gra_score=8.0,
            overall_band=7.5,
            feedback={"advice": "Strong paragraph PEEL cohesion."}
        )
        self.assertEqual(evaluated["status"], "evaluated")
        self.assertEqual(evaluated["overall_band"], 7.5)
        self.assertEqual(evaluated["feedback"]["advice"], "Strong paragraph PEEL cohesion.")

    def test_ai_conversation_history(self):
        msg1 = self.ai_conv_repo.add_message(
            learner_id="default_learner",
            role="user",
            message="Can you explain the difference between 'despite' and 'in spite of'?",
            detected_errors=[]
        )
        self.assertEqual(msg1["role"], "user")

        msg2 = self.ai_conv_repo.add_message(
            learner_id="default_learner",
            role="tutor",
            message="'Despite' and 'in spite of' share the identical meaning...",
            detected_errors=[]
        )
        self.assertEqual(msg2["role"], "tutor")

        history = self.ai_conv_repo.get_conversation_history("default_learner")
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "tutor")


if __name__ == "__main__":
    unittest.main()
