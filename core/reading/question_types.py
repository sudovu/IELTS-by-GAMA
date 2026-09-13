"""
IELTS Reading Question Types and Graders for IELTS by GAMA.
Supports:
- True / False / Not Given (TFNG)
- Yes / No / Not Given (YNNG)
- Matching Headings
- Sentence / Summary Completion
- Multiple Choice
"""

from typing import Dict, Any, List, Optional


class ReadingQuestionTypes:
    """Evaluates answers across distinct IELTS reading question formats."""

    @classmethod
    def grade_tfng(cls, user_answer: str, correct_answer: str, passage_evidence: str, explanation: str) -> Dict[str, Any]:
        """
        Grades True/False/Not Given.
        True = information agrees with passage
        False = information contradicts passage
        Not Given = impossible to know what the author says
        """
        norm_user = user_answer.strip().lower()
        norm_correct = correct_answer.strip().lower()

        # Handle common abbreviations (T, F, NG)
        alias_map = {"t": "true", "f": "false", "ng": "not given", "notgiven": "not given"}
        norm_user = alias_map.get(norm_user, norm_user)
        norm_correct = alias_map.get(norm_correct, norm_correct)

        is_correct = (norm_user == norm_correct)
        return {
            "type": "TFNG",
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation
        }

    @classmethod
    def grade_completion(
        cls,
        user_answer: str,
        acceptable_answers: List[str],
        max_words: int,
        passage_evidence: str,
        explanation: str
    ) -> Dict[str, Any]:
        """Grades fill-in-the-blank with strict word-count limits."""
        tokens = user_answer.strip().split()
        if len(tokens) > max_words:
            return {
                "type": "Completion",
                "user_answer": user_answer,
                "correct_answer": acceptable_answers[0],
                "is_correct": False,
                "passage_evidence": passage_evidence,
                "explanation": f"Exceeded word count limit! Max allowed: {max_words} words. You wrote {len(tokens)} words."
            }

        norm_user = user_answer.strip().lower().strip(".,;:!")
        is_correct = any(norm_user == acc.strip().lower() for acc in acceptable_answers)

        return {
            "type": "Completion",
            "user_answer": user_answer,
            "correct_answer": acceptable_answers[0],
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation
        }
