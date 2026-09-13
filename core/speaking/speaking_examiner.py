"""
AI IELTS Speaking Examiner for IELTS by GAMA.
Orchestrates official 3-part test format:
- Part 1: Introduction and Interview (4–5 mins)
- Part 2: Long Turn / Cue Card (1 min prep, 2 mins talk)
- Part 3: Two-way Abstract Discussion (4–5 mins)
Evaluates FC, LR, GRA, and Pronunciation criteria with formative feedback.
"""

from typing import Dict, Any, List, Optional
from .fluency_tracker import FluencyTracker
from ..scoring.criteria_evaluator import CriteriaEvaluator
from ..grammar.grammar_engine import GrammarEngine


class SpeakingExaminer:
    """Simulates an interactive IELTS speaking examiner."""

    PART_1_QUESTIONS = [
        "Could you please state your full name?",
        "Where do you come from, and what do you like most about your hometown?",
        "Do you work or are you currently studying?",
        "How do you prefer to spend your weekends?"
    ]

    PART_2_CUE_CARDS = [
        {
            "id": "cue_ambition",
            "topic": "Describe a significant achievement or ambitious goal you reached.",
            "prompts": [
                "What the achievement or goal was",
                "When you first decided to pursue it",
                "What obstacles you faced along the way",
                "And explain why this achievement was personally meaningful to you."
            ],
            "part_3_followups": [
                "Do young people today face greater pressure to achieve success than previous generations?",
                "How should schools balance academic targets with emotional well-being?",
                "Why do some people find it difficult to maintain long-term motivation?"
            ]
        }
    ]

    @classmethod
    def get_test_prompts(cls, card_idx: int = 0) -> Dict[str, Any]:
        card = cls.PART_2_CUE_CARDS[card_idx % len(cls.PART_2_CUE_CARDS)]
        return {
            "part_1": cls.PART_1_QUESTIONS,
            "part_2_cue_card": card,
            "part_3_discussion": card["part_3_followups"],
            "disclaimer": "AI IELTS Speaking Simulation. Practice estimate only."
        }

    @classmethod
    def evaluate_spoken_response(
        cls,
        transcript: str,
        duration_seconds: float = 90.0,
        pronunciation_rating: float = 6.5
    ) -> Dict[str, Any]:
        """Evaluates a learner's spoken turn across all four official criteria."""
        fluency_data = FluencyTracker.analyze_fluency(transcript, duration_seconds)
        fc_score = fluency_data["estimated_fc_band"]

        # Lexical Resource check
        words = transcript.lower().split()
        unique_ratio = len(set(words)) / max(1, len(words))
        lr_score = 6.0
        if unique_ratio > 0.6:
            lr_score += 0.5
        if any(w in transcript.lower() for w in ["significant", "perseverance", "milestone", "challenging", "consequently"]):
            lr_score += 0.5
        lr_score = min(8.5, max(4.0, lr_score))

        # Grammatical Range and Accuracy check
        diagnosed_errors = GrammarEngine.check_sentence(transcript)
        gra_score = 6.5
        if len(diagnosed_errors) == 0 and len(words) > 50:
            gra_score += 0.5
        elif len(diagnosed_errors) >= 2:
            gra_score -= 1.0
        gra_score = min(8.5, max(4.0, gra_score))

        p_score = pronunciation_rating

        criteria_result = CriteriaEvaluator.evaluate_speaking(
            fc_score=fc_score,
            lr_score=lr_score,
            gra_score=gra_score,
            p_score=p_score,
            fluency_metrics=fluency_data
        )

        criteria_result["corrections"] = diagnosed_errors
        criteria_result["actionable_tips"] = [
            "Use cohesive conversational signposts ('To be entirely honest', 'Looking back at that period', 'In the broader scheme of things').",
            "Keep speech continuous by elaborating on causes and personal reflections."
        ]
        return criteria_result
