"""
Spaced Repetition System (SRS) for IELTS by GAMA.
Uses SuperMemo SM-2 algorithm to schedule retention reviews for vocabulary,
grammar patterns, phrasal verbs, and collocations.
"""

from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import SRSRepository


class SpacedRepetitionSystem:
    """SuperMemo SM-2 based spaced repetition manager."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.repo = SRSRepository(self.db)

    def add_vocabulary_card(
        self,
        learner_id: str,
        word: str,
        definition: str,
        example_sentence: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        prompt = f"What is the definition and an example sentence for: **{word}**?"
        answer = f"**Definition:** {definition}\n**Example:** {example_sentence}"
        return self.repo.add_or_get_item(
            learner_id=learner_id,
            item_type="vocabulary",
            key_term=word,
            prompt=prompt,
            answer=answer,
            notes=notes
        )

    def add_collocation_card(
        self,
        learner_id: str,
        collocation: str,
        meaning: str,
        example: str
    ) -> Dict[str, Any]:
        prompt = f"Complete the natural academic collocation: *\"{collocation.split()[0]} _____\"*"
        answer = f"**Collocation:** {collocation}\n**Meaning:** {meaning}\n**Example:** {example}"
        return self.repo.add_or_get_item(
            learner_id=learner_id,
            item_type="collocation",
            key_term=collocation,
            prompt=prompt,
            answer=answer,
            notes=""
        )

    def get_due_deck(self, learner_id: str, limit: int = 15) -> List[Dict[str, Any]]:
        return self.repo.get_due_items(learner_id, limit=limit)

    def review_card(self, item_id: str, grade: int) -> Dict[str, Any]:
        """
        Grade:
        5: Perfect recall
        4: Correct after brief hesitation
        3: Correct with serious difficulty
        2: Incorrect; where the correct one seemed easy to recall
        1: Incorrect; remembered the wrong thing
        0: Complete blackout
        """
        if grade < 0 or grade > 5:
            raise ValueError("Grade must be an integer between 0 and 5")
        return self.repo.record_review(item_id, grade)
