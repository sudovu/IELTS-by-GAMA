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
        },
        "sec_2": {
            "id": "sec_2",
            "section_number": 2,
            "title": "Greendale Community Arts Centre & Gallery Tour",
            "audio_script": (
                "GUIDE: Good afternoon everyone, and welcome to Greendale Arts Centre. "
                "Before we tour the studios, let me outline key visitor details. "
                "The centre was founded in 1994, although major renovations took place in 2018. "
                "Our ceramic pottery workshop is located on the ground floor next to the courtyard garden. "
                "Opening hours on weekdays are 9 AM to 8 PM, while weekend entry closes earlier at 6 PM. "
                "Membership for local residents costs 45 pounds annually, which grants free admission to special exhibitions. "
                "For visitors arriving by public transport, bus route number 14 stops directly in front of the main entrance."
            ),
            "questions": [
                {
                    "num": 1,
                    "prompt": "Year of major centre renovations: _____",
                    "acceptable": ["2018"],
                    "max_words": 1,
                    "distractor_note": "Founded in 1994, but major renovations took place in 2018."
                },
                {
                    "num": 2,
                    "prompt": "Pottery workshop location: next to the _____ garden",
                    "acceptable": ["courtyard"],
                    "max_words": 1,
                    "distractor_note": "Directly mentioned as courtyard garden on the ground floor."
                },
                {
                    "num": 3,
                    "prompt": "Weekend closing time: _____ PM",
                    "acceptable": ["6", "6:00"],
                    "max_words": 1,
                    "distractor_note": "Weekday closing is 8 PM, but weekend entry closes at 6 PM."
                },
                {
                    "num": 4,
                    "prompt": "Direct bus route number: _____",
                    "acceptable": ["14"],
                    "max_words": 1,
                    "distractor_note": "Bus route 14 stops directly at main entrance."
                }
            ]
        },
        "sec_3": {
            "id": "sec_3",
            "section_number": 3,
            "title": "Academic Tutorial: Renewable Microgrid Projects",
            "audio_script": (
                "TUTOR: Good afternoon, Liam and Clara. Let's discuss your engineering fieldwork proposal. "
                "CLARA: Thanks, Professor. We decided to investigate solar microgrids installed on university rooftops. "
                "LIAM: Yes, we initially thought about wind turbines, but building height regulations made solar photovoltaic panels far more viable. "
                "TUTOR: An astute decision. And what primary variable will you measure over the six-month trial? "
                "CLARA: We are analyzing peak storage efficiency, specifically measuring battery discharge rates under cloudy conditions. "
                "TUTOR: Excellent. Keep in mind that your interim progress report must be submitted by November 12th. "
                "LIAM: Understood. We have already calibrated our digital telemetry sensors."
            ),
            "questions": [
                {
                    "num": 1,
                    "prompt": "Chosen renewable technology: solar _____ panels",
                    "acceptable": ["photovoltaic"],
                    "max_words": 1,
                    "distractor_note": "Wind turbines were initially considered, but solar photovoltaic was chosen."
                },
                {
                    "num": 2,
                    "prompt": "Primary measured variable: peak storage _____",
                    "acceptable": ["efficiency"],
                    "max_words": 1,
                    "distractor_note": "Specifically stated as peak storage efficiency."
                },
                {
                    "num": 3,
                    "prompt": "Interim report deadline: _____ 12th",
                    "acceptable": ["November"],
                    "max_words": 1,
                    "distractor_note": "Tutor explicitly mandates November 12th."
                }
            ]
        },
        "sec_4": {
            "id": "sec_4",
            "section_number": 4,
            "title": "Academic Lecture: Cetacean Bioacoustics in Polar Oceans",
            "audio_script": (
                "PROFESSOR: Welcome back to Marine Biology 402. Today we examine acoustic communication in Arctic cetaceans, "
                "specifically beluga whales and narwhals. In frozen ocean environments where solar illumination is virtually absent for months, "
                "sound waves represent the primary sensory modality for navigation, social cohesion, and prey localization. "
                "Beluga vocalizations encompass a dynamic acoustic spectrum ranging from low-frequency groans to ultrasonic clicks reaching 120 kilohertz. "
                "Recent bioacoustic telemetry indicates that anthropogenic noise from commercial shipping vessels causes significant acoustic masking, "
                "which forces pods to increase their call amplitude—a physiological adaptation known as the Lombard effect. "
                "Furthermore, the warming of sea ice has accelerated ambient underwater noise levels by nearly three decibels per decade."
            ),
            "questions": [
                {
                    "num": 1,
                    "prompt": "Primary sensory modality in Arctic waters: _____ waves",
                    "acceptable": ["sound"],
                    "max_words": 1,
                    "distractor_note": "Sound waves serve as the primary sensory modality."
                },
                {
                    "num": 2,
                    "prompt": "Maximum frequency of beluga ultrasonic clicks: _____ kilohertz",
                    "acceptable": ["120"],
                    "max_words": 1,
                    "distractor_note": "Stated as reaching 120 kilohertz."
                },
                {
                    "num": 3,
                    "prompt": "Vocal elevation under ambient noise is known as the _____ effect",
                    "acceptable": ["Lombard"],
                    "max_words": 1,
                    "distractor_note": "Physiological adaptation known as the Lombard effect."
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
