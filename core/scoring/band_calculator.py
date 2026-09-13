"""
IELTS Band Score Calculator for IELTS by GAMA.
Implements official standard rounding rules and raw score to band conversion
for Academic and General Training modules.
"""

from typing import Dict, Any, Optional


class BandCalculator:
    """Calculates individual module bands and composite overall IELTS band."""

    DISCLAIMER = "Practice estimate only. Not an official IELTS result."

    @staticmethod
    def round_band(raw_score: float) -> float:
        """
        IELTS standard rounding rule:
        - If fractional part < 0.25 -> round down to whole band (e.g. 6.125 -> 6.0)
        - If fractional part >= 0.25 and < 0.75 -> round to half band (e.g. 6.25 -> 6.5, 6.625 -> 6.5)
        - If fractional part >= 0.75 -> round up to next whole band (e.g. 6.75 -> 7.0)
        """
        raw_score = max(0.0, min(9.0, raw_score))
        whole = int(raw_score)
        fraction = raw_score - whole
        if fraction < 0.25:
            return float(whole)
        elif fraction < 0.75:
            return float(whole) + 0.5
        else:
            return float(whole + 1)

    @classmethod
    def calculate_overall(
        cls,
        listening: float,
        reading: float,
        writing: float,
        speaking: float
    ) -> Dict[str, Any]:
        mean = (listening + reading + writing + speaking) / 4.0
        overall = cls.round_band(mean)
        return {
            "overall_band": overall,
            "raw_average": round(mean, 3),
            "breakdown": {
                "listening": listening,
                "reading": reading,
                "writing": writing,
                "speaking": speaking
            },
            "disclaimer": cls.DISCLAIMER
        }

    @classmethod
    def raw_to_band_listening(cls, correct_answers: int, total_questions: int = 40) -> float:
        """Scales raw listening score out of 40 to IELTS band (Academic & GT identical)."""
        score = int(round((correct_answers / max(1, total_questions)) * 40))
        if score >= 39:
            return 9.0
        elif score >= 37:
            return 8.5
        elif score >= 35:
            return 8.0
        elif score >= 32:
            return 7.5
        elif score >= 30:
            return 7.0
        elif score >= 26:
            return 6.5
        elif score >= 23:
            return 6.0
        elif score >= 18:
            return 5.5
        elif score >= 16:
            return 5.0
        elif score >= 13:
            return 4.5
        elif score >= 10:
            return 4.0
        else:
            return 3.5

    @classmethod
    def raw_to_band_reading(cls, correct_answers: int, track: str = "Academic", total_questions: int = 40) -> float:
        """Raw reading score to band conversion for Academic vs General Training."""
        score = int(round((correct_answers / max(1, total_questions)) * 40))
        if track.lower().startswith("gen"):
            # General Training reading scales higher raw thresholds
            if score >= 40:
                return 9.0
            elif score >= 39:
                return 8.5
            elif score >= 37:
                return 8.0
            elif score >= 36:
                return 7.5
            elif score >= 34:
                return 7.0
            elif score >= 32:
                return 6.5
            elif score >= 30:
                return 6.0
            elif score >= 27:
                return 5.5
            elif score >= 23:
                return 5.0
            elif score >= 19:
                return 4.5
            elif score >= 15:
                return 4.0
            else:
                return 3.5
        else:
            # Academic reading scale
            if score >= 39:
                return 9.0
            elif score >= 37:
                return 8.5
            elif score >= 35:
                return 8.0
            elif score >= 33:
                return 7.5
            elif score >= 30:
                return 7.0
            elif score >= 27:
                return 6.5
            elif score >= 23:
                return 6.0
            elif score >= 19:
                return 5.5
            elif score >= 15:
                return 5.0
            elif score >= 13:
                return 4.5
            elif score >= 10:
                return 4.0
            else:
                return 3.5
