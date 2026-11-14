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
                "STUDENT: Wonderful. What meal provision plans are included?\n"
                "OFFICER: The Oakwood accommodation is fully self-catered, but there is a shared communal kitchen on each floor.\n"
                "STUDENT: That suits me well. Is there a deposit required to secure the reservation?\n"
                "OFFICER: Yes, a refundable security deposit of 350 pounds is required within forty-eight hours.\n"
                "STUDENT: Perfect. Could you give me your office contact extension in case I have queries?\n"
                "OFFICER: Of course. You can reach my desk at extension 4829, or email accommodation@campus.ac.uk.\n"
                "STUDENT: Great, and what identification documents should I bring to check in?\n"
                "OFFICER: Please bring your official university acceptance letter and a valid passport.\n"
                "STUDENT: Thank you very much for your assistance."
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
                },
                {
                    "num": 5,
                    "prompt": "Field of postgraduate study: Biomedical _____",
                    "acceptable": ["Science", "science"],
                    "max_words": 1,
                    "distractor_note": "Directly stated as master's in Biomedical Science."
                },
                {
                    "num": 6,
                    "prompt": "Catering arrangement: fully _____-catered",
                    "acceptable": ["self"],
                    "max_words": 1,
                    "distractor_note": "Confirmed as fully self-catered with communal kitchens."
                },
                {
                    "num": 7,
                    "prompt": "Required security deposit: £_____",
                    "acceptable": ["350"],
                    "max_words": 1,
                    "distractor_note": "Stated as refundable deposit of 350 pounds."
                },
                {
                    "num": 8,
                    "prompt": "Deposit payment deadline: within _____ hours",
                    "acceptable": ["48", "forty-eight"],
                    "max_words": 1,
                    "distractor_note": "Officer specifies within 48 hours."
                },
                {
                    "num": 9,
                    "prompt": "Direct office telephone extension: _____",
                    "acceptable": ["4829"],
                    "max_words": 1,
                    "distractor_note": "Extension numbers are a frequent Section 1 numerical listening test."
                },
                {
                    "num": 10,
                    "prompt": "Required document for key collection: valid _____",
                    "acceptable": ["passport"],
                    "max_words": 1,
                    "distractor_note": "Acceptance letter and valid passport required."
                }
            ]
        },
        "sec_2": {
            "id": "sec_2",
            "section_number": 2,
            "title": "Greendale Community Arts Centre & Gallery Tour",
            "audio_script": (
                "GUIDE: Good afternoon everyone, and welcome to Greendale Arts Centre. "
                "Before we tour the studios, let me outline key visitor details and opening schedules. "
                "The centre was founded in 1994, although major renovations took place in 2018. "
                "Our ceramic pottery workshop is located on the ground floor directly adjacent to the courtyard garden. "
                "Opening hours on weekdays are 9 AM to 8 PM, while weekend entry closes earlier at 6 PM. "
                "Membership for local residents costs 45 pounds annually, which grants free admission to special exhibitions. "
                "Non-members pay an entry fee of 8 pounds per exhibition gallery. "
                "For visitors arriving by public transport, bus route number 14 stops directly in front of the main entrance. "
                "If you are driving, the underground visitor car park is situated on Elm Street, with three electric vehicle charging points. "
                "Our popular community printmaking classes take place on Wednesday evenings, and all materials, including organic inks, are provided free of charge. "
                "Finally, our rooftop cafe serves locally sourced refreshments from 10 AM until 5 PM daily."
            ),
            "questions": [
                {
                    "num": 11,
                    "prompt": "Year of major centre renovations: _____",
                    "acceptable": ["2018"],
                    "max_words": 1,
                    "distractor_note": "Founded in 1994, but major renovations occurred in 2018."
                },
                {
                    "num": 12,
                    "prompt": "Pottery workshop location: next to the _____ garden",
                    "acceptable": ["courtyard"],
                    "max_words": 1,
                    "distractor_note": "Directly mentioned as courtyard garden on the ground floor."
                },
                {
                    "num": 13,
                    "prompt": "Weekend closing time: _____ PM",
                    "acceptable": ["6", "6:00"],
                    "max_words": 1,
                    "distractor_note": "Weekday closing is 8 PM, but weekend entry closes at 6 PM."
                },
                {
                    "num": 14,
                    "prompt": "Annual local resident membership fee: £_____",
                    "acceptable": ["45"],
                    "max_words": 1,
                    "distractor_note": "Non-member fee is £8, while annual membership is £45."
                },
                {
                    "num": 15,
                    "prompt": "Non-member single exhibition entry fee: £_____",
                    "acceptable": ["8"],
                    "max_words": 1,
                    "distractor_note": "Stated as £8 per exhibition gallery."
                },
                {
                    "num": 16,
                    "prompt": "Direct bus route number: _____",
                    "acceptable": ["14"],
                    "max_words": 1,
                    "distractor_note": "Bus route 14 stops directly at main entrance."
                },
                {
                    "num": 17,
                    "prompt": "Visitor car park location: _____ Street",
                    "acceptable": ["Elm", "elm"],
                    "max_words": 1,
                    "distractor_note": "Located on Elm Street."
                },
                {
                    "num": 18,
                    "prompt": "Number of electric vehicle chargers available: _____",
                    "acceptable": ["three", "3"],
                    "max_words": 1,
                    "distractor_note": "Specifically stated as three charging points."
                },
                {
                    "num": 19,
                    "prompt": "Printmaking evening classes held on _____ evenings",
                    "acceptable": ["Wednesday", "wednesday"],
                    "max_words": 1,
                    "distractor_note": "Printmaking classes scheduled for Wednesday evenings."
                },
                {
                    "num": 20,
                    "prompt": "Rooftop cafe morning opening time: _____ AM",
                    "acceptable": ["10", "10:00"],
                    "max_words": 1,
                    "distractor_note": "Centre opens at 9 AM, but rooftop cafe specifically opens at 10 AM."
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
                "TUTOR: Excellent. And what sampling frequency have you programmed into the automated loggers? "
                "LIAM: The telemetry sensors record voltage and temperature readings every fifteen minutes. "
                "TUTOR: Very thorough. Keep in mind that your interim progress report must be submitted by November 12th. "
                "CLARA: We have already structured the comparative literature review section. "
                "TUTOR: Good. Make sure you compare your findings with Dr. Chen's 2023 baseline dataset on lithium-ion degradation. "
                "LIAM: Right. We will also incorporate life-cycle carbon emission calculations into the financial analysis. "
                "TUTOR: Excellent. Meet me again in room 405 next Tuesday for your ethical approval sign-off."
            ),
            "questions": [
                {
                    "num": 21,
                    "prompt": "Chosen renewable technology: solar _____ panels",
                    "acceptable": ["photovoltaic"],
                    "max_words": 1,
                    "distractor_note": "Wind turbines were initially considered, but solar photovoltaic was chosen."
                },
                {
                    "num": 22,
                    "prompt": "Trial duration period: _____ months",
                    "acceptable": ["six", "6"],
                    "max_words": 1,
                    "distractor_note": "Stated as six-month trial."
                },
                {
                    "num": 23,
                    "prompt": "Primary measured variable: peak storage _____",
                    "acceptable": ["efficiency"],
                    "max_words": 1,
                    "distractor_note": "Specifically stated as peak storage efficiency."
                },
                {
                    "num": 24,
                    "prompt": "Sensor recording interval: every _____ minutes",
                    "acceptable": ["15", "fifteen"],
                    "max_words": 1,
                    "distractor_note": "Loggers record readings every fifteen minutes."
                },
                {
                    "num": 25,
                    "prompt": "Interim report deadline: _____ 12th",
                    "acceptable": ["November"],
                    "max_words": 1,
                    "distractor_note": "Tutor explicitly mandates November 12th."
                },
                {
                    "num": 26,
                    "prompt": "Comparative dataset author: Dr. _____",
                    "acceptable": ["Chen", "chen"],
                    "max_words": 1,
                    "distractor_note": "Specifically cites Dr. Chen's 2023 dataset."
                },
                {
                    "num": 27,
                    "prompt": "Battery degradation chemistry analyzed: lithium-_____",
                    "acceptable": ["ion"],
                    "max_words": 1,
                    "distractor_note": "Stated as lithium-ion degradation."
                },
                {
                    "num": 28,
                    "prompt": "Additional calculation incorporated: life-cycle _____ emissions",
                    "acceptable": ["carbon"],
                    "max_words": 1,
                    "distractor_note": "Liam states life-cycle carbon emission calculations."
                },
                {
                    "num": 29,
                    "prompt": "Meeting room for next tutorial: Room _____",
                    "acceptable": ["405"],
                    "max_words": 1,
                    "distractor_note": "Room number 405 for ethical approval."
                },
                {
                    "num": 30,
                    "prompt": "Purpose of upcoming meeting: _____ approval sign-off",
                    "acceptable": ["ethical"],
                    "max_words": 1,
                    "distractor_note": "Specifically ethical approval sign-off."
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
                "These high-frequency echolocation trains allow cetaceans to construct detailed spatial topographies beneath dense sea ice. "
                "Recent bioacoustic telemetry indicates that anthropogenic noise from commercial shipping vessels causes significant acoustic masking, "
                "which forces pods to increase their call amplitude—a physiological adaptation known as the Lombard effect. "
                "Furthermore, the retreat of multi-year sea ice has accelerated ambient underwater noise levels by nearly three decibels per decade. "
                "Industrial seismic surveys utilizing airgun arrays introduce low-frequency acoustic pulses that can disorient migrating juveniles up to fifty kilometers away. "
                "To mitigate physiological trauma, marine conservationists recommend establishing acoustic sanctuaries where commercial transit speeds are capped at ten knots."
            ),
            "questions": [
                {
                    "num": 31,
                    "prompt": "Primary sensory modality in Arctic waters: _____ waves",
                    "acceptable": ["sound"],
                    "max_words": 1,
                    "distractor_note": "Sound waves serve as the primary sensory modality."
                },
                {
                    "num": 32,
                    "prompt": "Target Arctic species examined: belugas and _____",
                    "acceptable": ["narwhals"],
                    "max_words": 1,
                    "distractor_note": "Lecturer explicitly introduces belugas and narwhals."
                },
                {
                    "num": 33,
                    "prompt": "Maximum frequency of beluga ultrasonic clicks: _____ kilohertz",
                    "acceptable": ["120"],
                    "max_words": 1,
                    "distractor_note": "Stated as reaching 120 kilohertz."
                },
                {
                    "num": 34,
                    "prompt": "High-frequency echolocation enables mapping beneath sea _____",
                    "acceptable": ["ice"],
                    "max_words": 1,
                    "distractor_note": "Constructs spatial topographies beneath dense sea ice."
                },
                {
                    "num": 35,
                    "prompt": "Vocal elevation under ambient noise is known as the _____ effect",
                    "acceptable": ["Lombard"],
                    "max_words": 1,
                    "distractor_note": "Physiological adaptation known as the Lombard effect."
                },
                {
                    "num": 36,
                    "prompt": "Ambient noise decibel increase per decade: _____ decibels",
                    "acceptable": ["three", "3"],
                    "max_words": 1,
                    "distractor_note": "Accelerated underwater noise by nearly three decibels per decade."
                },
                {
                    "num": 37,
                    "prompt": "Industrial surveys use _____ arrays that generate acoustic pulses",
                    "acceptable": ["airgun"],
                    "max_words": 1,
                    "distractor_note": "Stated as airgun arrays."
                },
                {
                    "num": 38,
                    "prompt": "Distance at which juveniles can be disoriented: up to _____ kilometers",
                    "acceptable": ["50", "fifty"],
                    "max_words": 1,
                    "distractor_note": "Can disorient juveniles up to fifty kilometers away."
                },
                {
                    "num": 39,
                    "prompt": "Recommended protected zones are called acoustic _____",
                    "acceptable": ["sanctuaries"],
                    "max_words": 1,
                    "distractor_note": "Conservationists recommend establishing acoustic sanctuaries."
                },
                {
                    "num": 40,
                    "prompt": "Recommended commercial vessel speed limit: _____ knots",
                    "acceptable": ["10", "ten"],
                    "max_words": 1,
                    "distractor_note": "Commercial transit speeds capped at ten knots."
                }
            ]
        }
    }

    @classmethod
    def list_sections(cls) -> List[Dict[str, Any]]:
        """Lists metadata for all 4 IELTS listening sections."""
        return [
            {
                "id": s["id"],
                "section_number": s["section_number"],
                "title": s["title"],
                "question_count": len(s["questions"])
            }
            for s in cls.SECTIONS.values()
        ]

    @classmethod
    def generate_full_listening_mock(cls, show_transcripts: bool = False) -> Dict[str, Any]:
        """Generates a complete 4-section, 40-question listening mock examination."""
        sections = [cls.get_section(f"sec_{i}", show_transcript=show_transcripts) for i in range(1, 5)]
        return {
            "mock_id": "mock_listening_full",
            "time_limit_minutes": 30,
            "total_questions": 40,
            "sections": sections,
            "activity_type": "transcript_strategy_practice_and_synthesis",
            "audio_asset_status": "speech_synthesis_ready (pre-recorded studio audio files not bundled)",
            "exam_concealment_mode": not show_transcripts,
            "instructions": "Practice note-taking and question answering from spoken dialogue scripts. Transcripts are concealed during test mode."
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
            "activity_type": "transcript_strategy_practice",
            "audio_asset_status": "speech_synthesis_ready",
            "exam_concealment_mode": not show_transcript,
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
        user_answers: Dict[Any, str]
    ) -> Dict[str, Any]:
        sec = cls.SECTIONS.get(section_id)
        if not sec:
            raise ValueError(f"Section {section_id} not found")

        total = len(sec["questions"])
        correct_count = 0
        breakdown = []

        for q in sec["questions"]:
            qnum = q["num"]
            # Look up by sequential number (e.g. 11..20) or relative section index (1..10)
            local_num = (qnum - 1) % 10 + 1
            ans = user_answers.get(qnum) or user_answers.get(str(qnum)) or user_answers.get(local_num) or user_answers.get(str(local_num)) or ""
            is_correct, msg = ListeningAnswerChecker.check_answer(
                user_input=str(ans),
                acceptable_answers=q["acceptable"],
                max_words=q["max_words"]
            )
            if is_correct:
                correct_count += 1

            breakdown.append({
                "question_num": qnum,
                "prompt": q["prompt"],
                "user_answer": str(ans),
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
