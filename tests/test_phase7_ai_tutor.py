# -*- coding: utf-8 -*-
"""
Tests for Phase 7: AI English Teacher & Dynamic CEFR Adaptation.
Verifies:
1. Multi-turn dialogue persistence in SQLite ai_conversations table.
2. Formative error interception and Teach-Through-Correction in conversational flow.
3. Dynamic CEFR adaptation according to learner's assessed level (A1 to C2).
4. Dialogue history retrieval and clearing.
"""

import unittest
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, AIConversationRepository
from core.chatbot.tutor_bot import UnifiedAITutor


class TestPhase7AITutor(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

        self.learner_repo = LearnerRepository(self.db)
        self.tutor = UnifiedAITutor(self.db)
        # Ensure offline mode for fast reliable deterministic local execution
        self.tutor.connectivity.set_forced_offline(True)

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_multi_turn_persistence_in_sqlite(self):
        """Verifies conversation turns are persisted in SQLite ai_conversations."""
        learner_id = "phase7_learner_1"
        self.learner_repo.get_or_create_default(learner_id, name="Sarah")

        # Turn 1
        resp_1 = self.tutor.process_message(learner_id, "Explain the difference between affect and effect.")
        self.assertIn("Affect", resp_1["reply"])
        self.assertIn("Effect", resp_1["reply"])

        # Turn 2
        resp_2 = self.tutor.process_message(learner_id, "Give me an example of an IELTS Task 2 essay topic.")
        self.assertIn("Task 2", resp_2["reply"])

        # Check conversation history in SQLite
        history = self.tutor.get_conversation_history(learner_id)
        self.assertEqual(len(history), 4)  # 2 user turns + 2 tutor turns
        self.assertEqual(history[0]["role"], "user")
        self.assertIn("affect", history[0]["message"].lower())
        self.assertEqual(history[1]["role"], "tutor")
        self.assertEqual(history[2]["role"], "user")
        self.assertEqual(history[3]["role"], "tutor")

    def test_formative_error_interception(self):
        """Verifies tutor intercepts grammar mistakes and appends formative feedback."""
        learner_id = "phase7_learner_2"
        self.learner_repo.get_or_create_default(learner_id)

        resp = self.tutor.process_message(learner_id, "I am agree with the government policy.")
        self.assertTrue(len(resp["detected_mistakes"]) > 0)
        self.assertIn("agree", resp["reply"].lower())

        # Check mistake logged in mistake book
        mistakes = self.tutor.mistake_book.get_mistakes(learner_id)
        self.assertGreaterEqual(len(mistakes), 1)

    def test_dynamic_cefr_adaptation(self):
        """Verifies tutor adapts to learner's current CEFR level."""
        learner_a1 = "learner_a1_user"
        self.learner_repo.create_learner(name="A1 Learner", cefr_level="A1")
        # Ensure learner exists
        a1_profile = self.learner_repo.get_or_create_default(learner_a1)
        self.learner_repo.update_profile(learner_a1, {"cefr_level": "A1"})

        resp_a1 = self.tutor.process_message(learner_a1, "How can I improve my English?")
        self.assertEqual(resp_a1["cefr_level"], "A1")

        learner_c1 = "learner_c1_user"
        self.learner_repo.get_or_create_default(learner_c1)
        self.learner_repo.update_profile(learner_c1, {"cefr_level": "C1"})

        resp_c1 = self.tutor.process_message(learner_c1, "How can I improve my English?")
        self.assertEqual(resp_c1["cefr_level"], "C1")

    def test_clear_conversation_history(self):
        """Verifies history clearing resets both SQLite and hot memory."""
        learner_id = "phase7_learner_3"
        self.learner_repo.get_or_create_default(learner_id)

        self.tutor.process_message(learner_id, "Hello tutor!")
        history_before = self.tutor.get_conversation_history(learner_id)
        self.assertEqual(len(history_before), 2)

        self.tutor.clear_conversation_history(learner_id)
        history_after = self.tutor.get_conversation_history(learner_id)
        self.assertEqual(len(history_after), 0)


if __name__ == "__main__":
    unittest.main()
