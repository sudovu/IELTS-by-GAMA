"""
Unit tests for Mistake Book and Spaced Repetition System (SRS).
"""

import unittest
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.progress.mistake_book import MistakeBook
from core.progress.srs import SpacedRepetitionSystem


class TestMistakeBookAndSRS(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

        self.mistake_book = MistakeBook(self.db)
        self.srs = SpacedRepetitionSystem(self.db)

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_mistake_recurrence_and_mastery(self):
        # Record mistake once
        m1 = self.mistake_book.record_error(
            learner_id="test_student",
            skill="grammar",
            category="Subject-Verb Agreement",
            original_text="The collection are lost",
            corrected_text="The collection is lost",
            explanation="Collection is singular."
        )
        self.assertEqual(m1["recurrence_count"], 1)

        # Record same mistake again -> recurrence increments
        m2 = self.mistake_book.record_error(
            learner_id="test_student",
            skill="grammar",
            category="Subject-Verb Agreement",
            original_text="The collection are lost",
            corrected_text="The collection is lost",
            explanation="Collection is singular."
        )
        self.assertEqual(m2["recurrence_count"], 2)

        # Review successfully -> mastery increases
        updated = self.mistake_book.review_mistake(m2["id"], is_successful=True)
        self.assertGreater(updated["mastery_score"], 0.0)

    def test_srs_sm2_algorithm(self):
        card = self.srs.add_vocabulary_card(
            learner_id="test_student",
            word="substantial",
            definition="Of considerable importance or size.",
            example_sentence="A substantial improvement."
        )
        self.assertEqual(card["repetition"], 0)
        self.assertEqual(card["interval_days"], 1.0)

        # Pass review with grade 5
        reviewed = self.srs.review_card(card["id"], grade=5)
        self.assertEqual(reviewed["repetition"], 1)
        self.assertEqual(reviewed["interval_days"], 1.0)

        # Next pass -> interval grows to 6 days under SM-2
        reviewed_2 = self.srs.review_card(card["id"], grade=5)
        self.assertEqual(reviewed_2["repetition"], 2)
        self.assertEqual(reviewed_2["interval_days"], 6.0)


if __name__ == "__main__":
    unittest.main()
