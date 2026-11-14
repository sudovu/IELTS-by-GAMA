# -*- coding: utf-8 -*-
"""
Tests for Phase 8: Comprehensive Vocabulary Vault & Spaced Repetition (SRS).
Verifies:
1. Academic Word List (AWL) seeding and lexical database population.
2. Full lexical word details (IPA, simple/advanced definitions, collocations, word family).
3. Search by keyword and CEFR tier (B2, C1, C2).
4. Creation and review of SM-2 spaced repetition flashcards in SQLite.
"""

import unittest
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.vocabulary.vocabulary_vault import VocabularyVault


class TestPhase8VocabularyVault(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()
        self.vault = VocabularyVault(self.db)

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_seeding_and_word_retrieval(self):
        """Verifies database seeding and rich lexical details."""
        count = self.vault.seed_default_vault()
        self.assertGreaterEqual(count, 10)

        # Retrieve 'substantial'
        word_data = self.vault.get_word("substantial")
        self.assertIsNotNone(word_data)
        self.assertEqual(word_data["pos"], "adjective")
        self.assertEqual(word_data["cefr_level"], "C1")
        self.assertIn("/səbˈstæn.ʃəl/", word_data["ipa"])
        self.assertGreaterEqual(len(word_data["collocations"]), 2)
        self.assertIn("substantiate", word_data["word_family"].values())

    def test_search_and_cefr_filtering(self):
        """Verifies lexical search by query substring and CEFR level."""
        self.vault.seed_default_vault()

        # Search by query
        results = self.vault.search_words("increase")
        self.assertGreaterEqual(len(results), 1)

        # Search by CEFR
        c1_words = self.vault.search_words(cefr_level="C1")
        self.assertGreaterEqual(len(c1_words), 5)
        for w in c1_words:
            self.assertEqual(w["cefr_level"], "C1")

    def test_srs_card_creation_and_sm2_review(self):
        """Verifies card creation and SuperMemo SM-2 interval progression."""
        self.vault.seed_default_vault()
        learner_id = "phase8_srs_learner"

        # 1. Add word to SRS
        card = self.vault.add_word_to_srs(learner_id, "ameliorate")
        self.assertIsNotNone(card["id"])
        self.assertEqual(card["key_term"], "ameliorate")
        self.assertEqual(card["repetition"], 0)

        # 2. Check due deck
        due = self.vault.get_due_srs_deck(learner_id)
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["key_term"], "ameliorate")

        # 3. Review card with perfect grade (5)
        reviewed = self.vault.review_card(card["id"], grade=5)
        self.assertEqual(reviewed["repetition"], 1)
        self.assertEqual(reviewed["interval_days"], 1)
        self.assertGreaterEqual(reviewed["ease_factor"], 2.5)

        # 4. Review again after simulated interval
        reviewed_2 = self.vault.review_card(card["id"], grade=4)
        self.assertEqual(reviewed_2["repetition"], 2)
        self.assertEqual(reviewed_2["interval_days"], 6)


if __name__ == "__main__":
    unittest.main()
