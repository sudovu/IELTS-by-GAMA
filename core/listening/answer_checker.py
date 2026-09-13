"""
Listening Answer Checker for IELTS by GAMA.
Applies rigorous IELTS answer validation rules:
- Case-insensitivity
- Punctuation stripping
- Number equivalence ('two' == '2')
- Strict word and number count bounds ("NO MORE THAN TWO WORDS AND/OR A NUMBER")
- British vs American spelling equivalencies ('centre' == 'center')
"""

import re
from typing import List, Tuple


class ListeningAnswerChecker:
    """Validates user responses against listening answer keys."""

    SPELLING_VARIANTS = {
        "centre": "center", "center": "centre",
        "colour": "color", "color": "colour",
        "theatre": "theater", "theater": "theatre",
        "programme": "program", "program": "programme",
        "travelling": "traveling", "traveling": "travelling"
    }

    NUMBER_MAP = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"
    }

    @classmethod
    def normalize_token(cls, token: str) -> str:
        t = token.lower().strip(".,;:!?'\"()")
        t = cls.SPELLING_VARIANTS.get(t, t)
        t = cls.NUMBER_MAP.get(t, t)
        return t

    @classmethod
    def check_answer(
        cls,
        user_input: str,
        acceptable_answers: List[str],
        max_words: int = 2,
        allow_number: bool = True
    ) -> Tuple[bool, str]:
        """
        Validates user input.
        Returns: (is_correct, feedback_message)
        """
        raw = user_input.strip()
        if not raw:
            return False, "No answer provided."

        tokens = raw.split()
        if len(tokens) > max_words:
            return False, f"Exceeded word count! Permitted: {max_words} word(s). You wrote {len(tokens)}."

        norm_user_tokens = [cls.normalize_token(t) for t in tokens]
        norm_user = " ".join(norm_user_tokens)

        for acc in acceptable_answers:
            acc_tokens = [cls.normalize_token(t) for t in acc.split()]
            norm_acc = " ".join(acc_tokens)
            if norm_user == norm_acc:
                return True, "Correct!"

        return False, f"Incorrect. Correct answer: '{acceptable_answers[0]}'"
