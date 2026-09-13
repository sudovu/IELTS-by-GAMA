"""
Fluency and Coherence Tracker for IELTS by GAMA.
Measures speech rate (Words Per Minute), filler word frequency,
lexical repetition, and hesitation markers.
"""

import re
from typing import Dict, Any, List


class FluencyTracker:
    """Extracts objective fluency metrics from learner spoken transcripts."""

    FILLER_WORDS = {"um", "uh", "er", "ah", "like", "you know", "actually", "basically", "sort of", "kind of"}

    @classmethod
    def analyze_fluency(cls, speech_text: str, duration_seconds: float = 60.0) -> Dict[str, Any]:
        words = re.findall(r"\b[a-zA-Z']+\b", speech_text.lower())
        word_count = len(words)

        duration_minutes = max(0.1, duration_seconds / 60.0)
        wpm = round(word_count / duration_minutes, 1)

        # Detect fillers
        filler_counts: Dict[str, int] = {}
        total_fillers = 0
        for w in words:
            if w in cls.FILLER_WORDS:
                filler_counts[w] = filler_counts.get(w, 0) + 1
                total_fillers += 1

        filler_ratio = round((total_fillers / max(1, word_count)) * 100, 1)

        # Repetition check (adjacent repeating words)
        repetitions = 0
        for i in range(len(words) - 1):
            if words[i] == words[i + 1] and words[i] not in ["had", "that"]:
                repetitions += 1

        # Fluency Band heuristic: Ideal WPM for IELTS is 120-150 with < 5% fillers
        fc_score = 6.0
        if 115 <= wpm <= 165:
            fc_score += 1.0
        elif wpm < 90 or wpm > 185:
            fc_score -= 1.0

        if filler_ratio < 4.0:
            fc_score += 0.5
        elif filler_ratio > 10.0:
            fc_score -= 1.0

        if repetitions == 0:
            fc_score += 0.5
        elif repetitions > 3:
            fc_score -= 0.5

        fc_score = min(8.5, max(4.0, fc_score))

        return {
            "word_count": word_count,
            "duration_seconds": duration_seconds,
            "words_per_minute": wpm,
            "target_wpm_range": "120 - 150 WPM",
            "total_filler_words": total_fillers,
            "filler_percentage": filler_ratio,
            "filler_breakdown": filler_counts,
            "adjacent_repetitions": repetitions,
            "estimated_fc_band": fc_score,
            "feedback": (
                "Excellent speaking tempo and minimal hesitation." if fc_score >= 7.5 else
                ("Moderate flow, but reduce filler words such as 'like' or 'um'." if filler_ratio > 5.0 else
                 "Work on pacing and developing multi-clause compound thoughts without long pauses.")
            )
        }
