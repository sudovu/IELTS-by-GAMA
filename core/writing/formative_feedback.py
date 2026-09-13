"""
Formative Feedback Formatter for IELTS by GAMA.
Transforms grammatical and lexical errors found in learner writing into
structured 'Teach Through Correction' learning items.
"""

from typing import Dict, Any, List
from ..grammar.grammar_engine import GrammarEngine


class FormativeFeedback:
    """Generates educational explanations rather than silently rewriting essays."""

    @classmethod
    def generate_formative_items(cls, essay_text: str) -> List[Dict[str, Any]]:
        errors = GrammarEngine.check_sentence(essay_text)
        formative_items = []
        for err in errors:
            formative_items.append({
                "category": err["category"],
                "original": err["original"],
                "correction": err["correction"],
                "why": err["why"],
                "better_alternative": err["better_alternative"],
                "practice_exercise": err["practice_exercise"],
                "formatted_view": GrammarEngine.format_teach_through_correction(err)
            })
        return formative_items
