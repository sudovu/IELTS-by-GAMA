# -*- coding: utf-8 -*-
"""
test_phase11_learner_journey.py
Comprehensive End-to-End QA Validation Test for Phase 11B.
Tests complete 21+ step learner journeys for multiple learners,
persistence across DB restarts, cross-learner data isolation,
and graceful offline fallback.
"""

import unittest
import os
import tempfile
import shutil

from core.database.db_manager import DatabaseManager
from core.database.repositories import (
    LearnerRepository,
    SettingsRepository,
    MistakeBookRepository,
    SRSRepository,
    TestResultRepository,
    AIConversationRepository
)
from core.curriculum.curriculum_engine import CurriculumEngine
from core.grammar.grammar_engine import GrammarEngine
from core.scoring.cefr_diagnostic import CEFRDiagnostic
from core.vocabulary.vocabulary_vault import VocabularyVault
from core.reading.reading_engine import ReadingEngine
from core.reading.question_types import ReadingQuestionTypes
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.speaking.fluency_tracker import FluencyTracker
from core.speaking.pronunciation_coach import PronunciationCoach
from core.chatbot.tutor_bot import UnifiedAITutor
from core.progress.study_planner import StudyPlanner
from core.progress.analytics import LearningAnalytics
from core.progress.mistake_book import MistakeBook


class TestPhase11LearnerJourney(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_journey.db")
        self.db = DatabaseManager(self.db_path)
        self.db.init_schema()

        self.learner_repo = LearnerRepository(self.db)
        self.settings_repo = SettingsRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)
        self.srs_repo = SRSRepository(self.db)
        self.test_result_repo = TestResultRepository(self.db)
        self.chat_repo = AIConversationRepository(self.db)

        self.curriculum = CurriculumEngine(self.db)
        self.curriculum.seed_default_curriculum()
        self.grammar = GrammarEngine()
        self.vocab = VocabularyVault(self.db)
        self.vocab.seed_default_vault()
        self.tutor = UnifiedAITutor(self.db)
        self.tutor.connectivity.set_forced_offline(True)
        self.planner = StudyPlanner(self.db)
        self.analytics = LearningAnalytics(self.db)
        self.mistake_book = MistakeBook(self.db)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_complete_e2e_learner_journey_and_isolation(self):
        # -------------------------------------------------------------
        # STEP 1: First launch & Create Learner 1 (Alice: Academic, B2, 7.5)
        # -------------------------------------------------------------
        alice = self.learner_repo.create_learner(
            name="Alice",
            target_band=7.5,
            current_band=6.0,
            cefr_level="B2",
            track="Academic",
            daily_minutes=60,
            target_exam_date="2026-12-01"
        )
        alice_id = alice["id"]
        self.assertIsNotNone(alice_id)
        self.assertEqual(alice["name"], "Alice")
        self.assertEqual(alice["track"], "Academic")
        self.assertEqual(alice["target_band"], 7.5)

        # Set Alice as active in settings
        self.settings_repo.set("active_learner_id", alice_id)
        self.assertEqual(self.settings_repo.get("active_learner_id"), alice_id)

        # -------------------------------------------------------------
        # STEP 2: Diagnostic Assessment
        # -------------------------------------------------------------
        diag_questions = CEFRDiagnostic.DIAGNOSTIC_QUESTIONS
        self.assertGreaterEqual(len(diag_questions), 10, "Diagnostic must have at least 10 items")
        alice_diag_answers = {}
        for idx, q in enumerate(diag_questions):
            q_id = q["id"]
            if idx < 9:
                alice_diag_answers[q_id] = q["correct"]
            else:
                wrong_opt = [opt for opt in q["options"] if opt != q["correct"]][0]
                alice_diag_answers[q_id] = wrong_opt

        diag_eval = CEFRDiagnostic.grade_diagnostic(alice_diag_answers)
        self.assertEqual(diag_eval["correct_count"], 9)
        self.assertIn("estimated_cefr", diag_eval)
        self.assertIn("estimated_band", diag_eval)
        self.assertIn("disclaimer", diag_eval)

        # Record diagnostic test result
        self.test_result_repo.record_result(
            learner_id=alice_id,
            test_type="diagnostic",
            track="Academic",
            overall_band=diag_eval["estimated_band"],
            details=diag_eval
        )

        # -------------------------------------------------------------
        # STEP 3: CEFR Lesson & Exercise with Intentional Mistakes
        # -------------------------------------------------------------
        lesson_id = "curric_b2_gram_conditionals"
        lesson = self.curriculum.get_lesson(lesson_id, learner_id=alice_id)
        self.assertIsNotNone(lesson)
        assessments = lesson["assessment"]
        self.assertGreaterEqual(len(assessments), 1)

        # Submit intentional wrong answer to test formative error logging
        q1 = assessments[0]
        wrong_opt = (q1["correct_index"] + 1) % len(q1["options"])

        sub_res = self.curriculum.evaluate_submission(
            learner_id=alice_id,
            lesson_id=lesson_id,
            answers={q1["id"]: wrong_opt}
        )
        self.assertTrue(sub_res["success"])
        self.assertEqual(sub_res["score"], 0.0)
        self.assertEqual(sub_res["status"], "needs_review")

        # Verify mistake was logged in Mistake Book
        alice_mistakes = self.mistake_repo.get_mistakes_by_learner(alice_id)
        self.assertGreaterEqual(len(alice_mistakes), 1)

        # -------------------------------------------------------------
        # STEP 4: Vocabulary Vault & SRS Scheduling
        # -------------------------------------------------------------
        srs_card = self.vocab.add_word_to_srs(alice_id, "substantial")
        self.assertIsNotNone(srs_card["id"])
        self.assertEqual(srs_card["key_term"], "substantial")
        self.assertEqual(srs_card["repetition"], 0)

        # Review card with SuperMemo SM-2 (grade 5)
        reviewed_card = self.vocab.review_card(srs_card["id"], grade=5)
        self.assertEqual(reviewed_card["repetition"], 1)
        self.assertEqual(reviewed_card["interval_days"], 1)

        # -------------------------------------------------------------
        # STEP 5: Reading Practice Session
        # -------------------------------------------------------------
        acad_passages = ReadingEngine.list_passages(track="Academic")
        self.assertGreater(len(acad_passages), 0)
        p1 = ReadingEngine.get_passage(acad_passages[0]["id"], show_answers=True)

        # Grade a completion and a TFNG question
        comp_res = ReadingQuestionTypes.grade_completion("black smokers", ["black smokers"], max_words=2, passage_evidence="ev", explanation="exp")
        self.assertTrue(comp_res["is_correct"])

        tfng_res = ReadingQuestionTypes.grade_tfng("True", "True", "evidence", "exp")
        self.assertTrue(tfng_res["is_correct"])

        # Record Reading Exam Result
        self.test_result_repo.record_result(
            learner_id=alice_id,
            test_type="reading",
            track="Academic",
            overall_band=7.0,
            reading_band=7.0,
            details={"passage_id": acad_passages[0]["id"], "correct_count": 11, "total": 13}
        )

        # -------------------------------------------------------------
        # STEP 6: Listening Practice Session
        # -------------------------------------------------------------
        listening_mock = ListeningEngine.generate_full_listening_mock(show_transcripts=False)
        self.assertEqual(listening_mock["total_questions"], 40)
        self.assertEqual(len(listening_mock["sections"]), 4)

        # Record Listening Exam Result
        self.test_result_repo.record_result(
            learner_id=alice_id,
            test_type="listening",
            track="Academic",
            overall_band=7.5,
            listening_band=7.5,
            details={"correct_count": 33, "total": 40}
        )

        # -------------------------------------------------------------
        # STEP 7: Writing Task 2 Evaluation
        # -------------------------------------------------------------
        task2_sample = (
            "In contemporary society, an increasing number of individuals argue that high school students "
            "should exclusively study science, technology, engineering, and mathematics (STEM), while others "
            "contend that creative arts are equally indispensable. Although technical proficiencies drive economic prosperity, "
            "I firmly believe that both domains are mutually reinforcing and vital for well-rounded development.\n\n"
            "Firstly, STEM disciplines furnish students with analytical capabilities to solve pressing global dilemmas. "
            "For instance, computing and mathematics foster logical problem-solving skills that prepare secondary students "
            "for technological industries. Without rigorous scientific foundations, students may encounter limitations in emerging global labor markets.\n\n"
            "Conversely, arts and humanities cultivate creative discernment, emotional intelligence, and critical expression. "
            "Scientific knowledge without creative inspiration often yields rigid solutions. Artistic pursuits encourage students "
            "to approach scientific challenges from imaginative angles, thereby stimulating innovative design and holistic thinking.\n\n"
            "Furthermore, multidisciplinary education ensures balanced personal development. Exposure to literature, painting, "
            "and music reduces academic burnout and enhances communication abilities, which are paramount when explaining "
            "complex technical projects to broader audiences.\n\n"
            "In conclusion, although STEM education is vital for technological progress, artistic subjects nourish the creative "
            "and expressive capacities required to deploy technology humanely. Therefore, secondary curricula should maintain "
            "an integrated approach rather than prioritizing one field over another."
        )
        writing_eval = WritingEvaluator.evaluate_essay("acad_t2_stem", task2_sample, db=self.db)
        self.assertIn("Task Response", writing_eval["criteria"])
        self.assertIn("Coherence and Cohesion", writing_eval["criteria"])
        self.assertIn("Lexical Resource", writing_eval["criteria"])
        self.assertIn("Grammatical Range and Accuracy", writing_eval["criteria"])
        self.assertGreaterEqual(writing_eval["estimated_band"], 6.0)

        # Record Writing Attempt
        self.test_result_repo.record_result(
            learner_id=alice_id,
            test_type="writing",
            track="Academic",
            overall_band=writing_eval["estimated_band"],
            writing_band=writing_eval["estimated_band"],
            details=writing_eval
        )

        # -------------------------------------------------------------
        # STEP 8: Speaking Simulation & Pronunciation Coach
        # -------------------------------------------------------------
        speech_sample = (
            "Well, in my spare time, I genuinely enjoy reading scientific literature and jogging in the local park. "
            "It helps me unwind after an intensive working day, and furthermore, it keeps me physically fit."
        )
        fluency_res = FluencyTracker.analyze_fluency(speech_sample, duration_seconds=12.0)
        self.assertGreaterEqual(fluency_res["words_per_minute"], 60.0)

        # Pronunciation Coach check
        pron_res = PronunciationCoach.evaluate_drill_attempt(
            drill_type="minimal_pair",
            target_word="sheep",
            spoken_transcript="The sheep was in the green field"
        )
        self.assertTrue(pron_res["phonemic_match"])

        # Record Speaking Attempt
        self.test_result_repo.record_result(
            learner_id=alice_id,
            test_type="speaking",
            track="Academic",
            overall_band=7.0,
            speaking_band=7.0,
            details={"fluency": fluency_res, "pronunciation": pron_res}
        )

        # -------------------------------------------------------------
        # STEP 9: Multi-turn AI Tutor Chat
        # -------------------------------------------------------------
        resp1 = self.tutor.process_message(alice_id, "Explain the difference between affect and effect.")
        self.assertIn("reply", resp1)
        self.assertIn("Affect", resp1["reply"])

        resp2 = self.tutor.process_message(alice_id, "Give me an example sentence for each word.")
        self.assertIn("reply", resp2)

        chat_history = self.chat_repo.get_conversation_history(alice_id)
        self.assertGreaterEqual(len(chat_history), 2)

        # -------------------------------------------------------------
        # STEP 10: Adaptive Study Plan Generation & Dashboard Verification
        # -------------------------------------------------------------
        adaptive_plan = self.planner.generate_adaptive_study_plan(alice_id)
        self.assertIn("daily_minutes", adaptive_plan)
        self.assertIn("four_week_milestones", adaptive_plan)
        self.assertEqual(adaptive_plan["weakest_skill"], "writing")

        dash = self.analytics.get_dashboard_data(alice_id)
        self.assertIn("overall_band_estimate", dash)
        self.assertIn("skills_radar", dash)
        self.assertGreaterEqual(len(dash["recent_test_results"]), 4)

        # -------------------------------------------------------------
        # STEP 11: Database Persistence Across Close and Reopen
        # -------------------------------------------------------------
        self.db.close()

        # Reopen fresh DatabaseManager on same SQLite file
        reopened_db = DatabaseManager(self.db_path)
        reopened_learner_repo = LearnerRepository(reopened_db)
        reopened_test_repo = TestResultRepository(reopened_db)
        reopened_mistake_repo = MistakeBookRepository(reopened_db)
        reopened_srs_repo = SRSRepository(reopened_db)
        reopened_chat_repo = AIConversationRepository(reopened_db)

        # Verify Alice's profile persists intact
        alice_reloaded = reopened_learner_repo.get_learner(alice_id)
        self.assertIsNotNone(alice_reloaded)
        self.assertEqual(alice_reloaded["name"], "Alice")
        self.assertEqual(alice_reloaded["target_band"], 7.5)

        # Verify test results persisted
        alice_results = reopened_test_repo.get_history(alice_id)
        self.assertGreaterEqual(len(alice_results), 4)

        # Verify mistakes persisted
        reloaded_mistakes = reopened_mistake_repo.get_mistakes_by_learner(alice_id)
        self.assertGreaterEqual(len(reloaded_mistakes), 1)

        # Verify SRS card persisted
        reloaded_card = reopened_srs_repo.get_item(srs_card["id"])
        self.assertIsNotNone(reloaded_card)
        self.assertEqual(reloaded_card["key_term"], "substantial")

        # Verify chat history persisted
        reloaded_chat = reopened_chat_repo.get_conversation_history(alice_id)
        self.assertGreaterEqual(len(reloaded_chat), 2)

        # -------------------------------------------------------------
        # STEP 12: Learner 2 (Bob: General Training, B1, 6.5) & Strict Isolation
        # -------------------------------------------------------------
        bob = reopened_learner_repo.create_learner(
            name="Bob",
            target_band=6.5,
            current_band=5.0,
            cefr_level="B1",
            track="General Training",
            daily_minutes=45,
            target_exam_date="2027-01-15"
        )
        bob_id = bob["id"]
        self.assertNotEqual(alice_id, bob_id)

        # Verify Bob has zero data initially
        self.assertEqual(len(reopened_test_repo.get_history(bob_id)), 0)
        self.assertEqual(len(reopened_mistake_repo.get_mistakes_by_learner(bob_id)), 0)
        self.assertEqual(len(reopened_chat_repo.get_conversation_history(bob_id)), 0)

        # Bob adds his own vocabulary card
        bob_vocab = VocabularyVault(reopened_db)
        bob_card = bob_vocab.add_word_to_srs(bob_id, "ameliorate")
        self.assertIsNotNone(bob_card["id"])

        # Bob takes a General Training Writing Task 1
        gt_letter = (
            "Dear Sir or Madam,\n\n"
            "I am writing to formally register a complaint regarding my checked baggage, "
            "which was delivered severely damaged and three days late on flight GA-402 on October 14th.\n\n"
            "Upon retrieving my suitcase at the terminal carousel, I discovered that the hard outer shell was cracked, "
            "and valuable photographic equipment inside was broken. Specifically, the professional camera lens was shattered "
            "and the casing was dented beyond repair. Furthermore, because my luggage was missing for three days, "
            "I had to purchase emergency clothing, toiletries, and business attire at considerable personal expense.\n\n"
            "Given these unfortunate circumstances, I expect the airline to provide financial compensation of 450 dollars "
            "to cover the replacement cost of the suitcase and damaged contents. In addition, I request reimbursement for essential expenses.\n\n"
            "I look forward to your prompt response and an equitable resolution to this matter within fourteen business days.\n\n"
            "Yours faithfully,\nBob Johnson"
        )
        bob_eval = WritingEvaluator.evaluate_essay("gt_t1_airline_complaint", gt_letter, db=reopened_db)
        reopened_test_repo.record_result(
            learner_id=bob_id,
            test_type="writing",
            track="General Training",
            overall_band=bob_eval["estimated_band"],
            writing_band=bob_eval["estimated_band"],
            details=bob_eval
        )

        # Bob chats with AI tutor
        bob_tutor = UnifiedAITutor(reopened_db)
        bob_tutor.connectivity.set_forced_offline(True)
        bob_tutor.process_message(bob_id, "How do I organize a formal letter for General Training IELTS?")

        # -------------------------------------------------------------
        # STEP 13: Strict Cross-Learner Data Isolation Audit
        # -------------------------------------------------------------
        alice_final_results = reopened_test_repo.get_history(alice_id)
        alice_final_chat = reopened_chat_repo.get_conversation_history(alice_id)

        bob_final_results = reopened_test_repo.get_history(bob_id)
        bob_final_chat = reopened_chat_repo.get_conversation_history(bob_id)

        # Assert no cross-leakage in test results
        alice_tracks = {r["track"] for r in alice_final_results}
        bob_tracks = {r["track"] for r in bob_final_results}
        self.assertNotIn("General Training", alice_tracks, "Alice must not see Bob's GT results")
        self.assertIn("General Training", bob_tracks)

        # Assert no cross-leakage in chat history
        alice_messages = [m["message"] for m in alice_final_chat]
        bob_messages = [m["message"] for m in bob_final_chat]
        self.assertTrue(any("affect and effect" in m.lower() for m in alice_messages))
        self.assertFalse(any("affect and effect" in m.lower() for m in bob_messages))
        self.assertTrue(any("formal letter" in m.lower() for m in bob_messages))
        self.assertFalse(any("formal letter" in m.lower() for m in alice_messages))

        # Clean up
        reopened_db.close()


if __name__ == "__main__":
    unittest.main()
