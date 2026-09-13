"""
Listening Engine for IELTS by GAMA.
Delivers original audio transcripts, section exercises, and distractor analyses.
Transcripts are protected and only shown upon explicit learner request or test completion.
"""

from typing import Dict, Any, List, Optional
from .answer_checker import ListeningAnswerChecker
from ..scoring.band_calculator import BandCalculator


class ListeningEngine:
    """Manages listening exercises, distractor identification, and score calculation."""

    SECTIONS = {
        "sec_1": {
            "id": "sec_1",
            "section_number": 1,
            "title": "University Campus Accommodation Booking",
            "audio_script": (
                "OFFICER: Good morning, Campus Housing Office. How can I help you today?\n"
                "STUDENT: Hello. I'd like to inquire about booking a room in the university halls for the upcoming semester.\n"
                "OFFICER: Certainly. Could I first take your full name, please?\n"
                "STUDENT: Yes, it's Julian Sterling. That's S-T-E-R-L-I-N-G.\n"
                "OFFICER: Thank you, Julian. And what faculty are you enrolled in?\n"
                "STUDENT: I'm starting a master's program in Biomedical Science.\n"
                "OFFICER: Excellent. Now, regarding room preferences, we have standard single rooms with shared facilities "
                "or en-suite studio rooms.\n"
                "STUDENT: I'd strongly prefer an en-suite room if possible. I need a quiet study environment.\n"
                "OFFICER: Right. An en-suite room in Oakwood Lodge is available. The standard price is 240 pounds per week, "
                "but because you are booking for the full academic term, a student subsidy applies, bringing it down to 210 pounds per week.\n"
                "STUDENT: 210 pounds sounds very reasonable. And when would the tenancy officially commence?\n"
                "OFFICER: Key collection starts on the 18th of September, though orientation begins three days earlier.\n"
                "STUDENT: Wonderful. I'll reserve that."
            ),
            "questions": [
                {
                    "num": 1,
                    "prompt": "Applicant's surname: _____",
                    "acceptable": ["Sterling"],
                    "max_words": 1,
                    "distractor_note": "Spelled out clearly by the applicant as S-T-E-R-L-I-N-G."
                },
                {
                    "num": 2,
                    "prompt": "Preferred room type: _____ room",
                    "acceptable": ["en-suite", "ensuite"],
                    "max_words": 1,
                    "distractor_note": "The officer mentioned standard single rooms first, but the student specifically selected en-suite."
                },
                {
                    "num": 3,
                    "prompt": "Discounted weekly rent: £_____",
                    "acceptable": ["210"],
                    "max_words": 1,
                    "distractor_note": "CLASSIC IELTS DISTRACTOR: The officer initially states £240, but immediately corrects to £210 due to the full-term subsidy."
                },
                {
                    "num": 4,
                    "prompt": "Date of key collection: 18th of _____",
                    "acceptable": ["September"],
                    "max_words": 1,
                    "distractor_note": "Orientation begins earlier, but key collection is specifically on the 18th of September."
                }
            ]
        }
    }

    @classmethod
    def get_section(cls, section_id: str = "sec_1", show_transcript: bool = False) -> Optional[Dict[str, Any]]:
        sec = cls.SECTIONS.get(section_id)
        if not sec:
            return None
        data = {
            "id": sec["id"],
            "section_number": sec["section_number"],
            "title": sec["title"],
            "questions": [
                {"num": q["num"], "prompt": q["prompt"], "max_words": q["max_words"]}
                for q in sec["questions"]
            ]
        }
        if show_transcript:
            data["audio_script"] = sec["audio_script"]
        return data

    @classmethod
    def get_audio_script(cls, section_id: str = "sec_1") -> str:
        """Exposes the audio script text for local speech synthesizer playback."""
        sec = cls.SECTIONS.get(section_id)
        return sec["audio_script"] if sec else ""

    @classmethod
    def evaluate_submission(
        cls,
        section_id: str,
        user_answers: Dict[int, str]
    ) -> Dict[str, Any]:
        sec = cls.SECTIONS.get(section_id)
        if not sec:
            raise ValueError(f"Section {section_id} not found")

        total = len(sec["questions"])
        correct_count = 0
        breakdown = []

        for q in sec["questions"]:
            qnum = q["num"]
            ans = user_answers.get(qnum, "")
            is_correct, msg = ListeningAnswerChecker.check_answer(
                user_input=ans,
                acceptable_answers=q["acceptable"],
                max_words=q["max_words"]
            )
            if is_correct:
                correct_count += 1

            breakdown.append({
                "question_num": qnum,
                "prompt": q["prompt"],
                "user_answer": ans,
                "correct_answer": q["acceptable"][0],
                "is_correct": is_correct,
                "distractor_analysis": q["distractor_note"]
            })

        band = BandCalculator.raw_to_band_listening(correct_count, total_questions=total)

        return {
            "section_id": section_id,
            "title": sec["title"],
            "correct_answers": correct_count,
            "total_questions": total,
            "estimated_band": band,
            "results": breakdown,
            "listening_strategies": [
                "Always look ahead at the next question during the preparation interval.",
                "Listen out for correction cues ('actually', 'however', 'rather than') indicating a distractor was superseded."
            ],
            "disclaimer": BandCalculator.DISCLAIMER,
            "copyright_notice": "AI-generated original IELTS-style listening exercise."
        }
