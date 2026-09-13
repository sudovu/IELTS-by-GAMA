"""
IELTS Assessment Criteria Evaluator for IELTS by GAMA.
Evaluates Writing and Speaking based on official IELTS public band descriptor criteria:
- Writing: Task Response / Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range and Accuracy
- Speaking: Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, Pronunciation
"""

from typing import Dict, Any, List
from .band_calculator import BandCalculator


class CriteriaEvaluator:
    """Computes criterion-referenced band estimates and qualitative feedback."""

    @classmethod
    def evaluate_writing(
        cls,
        task_type: str,  # 'task_1' or 'task_2'
        track: str,      # 'Academic' or 'General'
        text: str,
        tr_score: float,
        cc_score: float,
        lr_score: float,
        gra_score: float,
        word_count: int,
        feedback_notes: Dict[str, str] = None
    ) -> Dict[str, Any]:
        # Penalty for underlength
        min_words = 150 if task_type == "task_1" else 250
        length_penalty = 0.0
        if word_count < min_words:
            deficit = min_words - word_count
            length_penalty = min(1.0, round(deficit / 100.0, 1))

        # Average four criteria
        raw_avg = (tr_score + cc_score + lr_score + gra_score) / 4.0
        adjusted_avg = max(1.0, raw_avg - length_penalty)
        final_band = BandCalculator.round_band(adjusted_avg)

        criterion_name_1 = "Task Achievement" if task_type == "task_1" else "Task Response"

        return {
            "task_type": task_type,
            "track": track,
            "estimated_band": final_band,
            "raw_average": round(raw_avg, 2),
            "word_count": word_count,
            "minimum_required_words": min_words,
            "underlength_penalty": length_penalty,
            "criteria": {
                criterion_name_1: round(tr_score, 1),
                "Coherence and Cohesion": round(cc_score, 1),
                "Lexical Resource": round(lr_score, 1),
                "Grammatical Range and Accuracy": round(gra_score, 1)
            },
            "feedback": feedback_notes or {},
            "disclaimer": BandCalculator.DISCLAIMER,
            "notice": "Official IELTS public band descriptors were referenced for assessment rubrics."
        }

    @classmethod
    def evaluate_speaking(
        cls,
        fc_score: float,
        lr_score: float,
        gra_score: float,
        p_score: float,
        fluency_metrics: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        raw_avg = (fc_score + lr_score + gra_score + p_score) / 4.0
        final_band = BandCalculator.round_band(raw_avg)

        return {
            "estimated_band": final_band,
            "raw_average": round(raw_avg, 2),
            "criteria": {
                "Fluency and Coherence": round(fc_score, 1),
                "Lexical Resource": round(lr_score, 1),
                "Grammatical Range and Accuracy": round(gra_score, 1),
                "Pronunciation": round(p_score, 1)
            },
            "fluency_metrics": fluency_metrics or {},
            "disclaimer": BandCalculator.DISCLAIMER,
            "notice": "Official IELTS public band descriptors were referenced for assessment rubrics."
        }
