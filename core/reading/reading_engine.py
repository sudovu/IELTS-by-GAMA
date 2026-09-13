"""
Reading Engine for IELTS by GAMA.
Delivers 100% original, copyright-compliant IELTS-style reading passages and exercises.
Analyzes skimming, scanning, distractor traps, and keyword matching.
"""

from typing import Dict, Any, List, Optional
from .question_types import ReadingQuestionTypes
from ..scoring.band_calculator import BandCalculator


class ReadingEngine:
    """Manages original IELTS Academic and General Training reading tests."""

    ORIGINAL_PASSAGES = {
        "acad_p1": {
            "id": "acad_p1",
            "track": "Academic",
            "title": "The Architecture of Deep-Sea Hydrothermal Ecosystems",
            "text": (
                "Deep-sea hydrothermal vents, discovered in 1977 along the Galapagos Rift, represent one of the most "
                "remarkable biological frontiers on Earth. Located thousands of meters beneath the oceanic surface where "
                "sunlight cannot penetrate, these geological formations dispel the historical assumption that all complex "
                "ecosystems rely fundamentally on solar photosynthesis. Instead, these abyssal biomes are sustained through "
                "chemosynthesis, a process mediated by specialized extremophilic bacteria.\n\n"
                "As tectonic plates diverge, seawater infiltrates subterranean fissures, reaching temperatures exceeding "
                "400 degrees Celsius near magma chambers. Saturated with dissolved minerals—predominantly hydrogen sulfide, "
                "iron, and copper—the superheated water precipitates violently upon encountering the frigid, near-freezing ambient "
                "ocean. This reaction constructs towering mineralized chimneys colloquially known as 'black smokers'.\n\n"
                "The organisms flourishing around these vents exhibit astounding biological adaptations. Giant tube worms "
                "(Riftia pachyptila), which can reach lengths of over two meters, completely lack a digestive tract, mouth, or gut. "
                "Instead, they harbor billions of symbiotic sulfur-oxidizing bacteria within an organ called the trophosome. "
                "The tube worms extract hydrogen sulfide and oxygen from the hydrothermal fluid using vascularized red plumes, "
                "transferring these compounds to the endosymbionts, which synthesize organic nourishment for the host.\n\n"
                "Nevertheless, these thriving oasis communities are exceptionally ephemeral. Because tectonic shifts and volcanic "
                "eruptions routinely seal hydrothermal conduits or open new subterranean fractures, vents can abruptly shut down within "
                "a matter of decades. Consequently, hydrothermal vent fauna have developed rapid larval dispersion mechanisms capable "
                "of traversing vast expanses of inhospitable abyssal desert to locate newly forming vents."
            ),
            "questions": [
                {
                    "num": 1,
                    "type": "TFNG",
                    "prompt": "Deep-sea hydrothermal ecosystems require solar radiation to produce fundamental nutrients.",
                    "correct": "False",
                    "evidence": "these abyssal biomes are sustained through chemosynthesis, a process mediated by specialized extremophilic bacteria [rather than photosynthesis]",
                    "explanation": "The text states vents rely on chemosynthesis rather than solar photosynthesis, directly contradicting the statement."
                },
                {
                    "num": 2,
                    "type": "TFNG",
                    "prompt": "Giant tube worms absorb nourishment directly through their mouths.",
                    "correct": "False",
                    "evidence": "Giant tube worms... completely lack a digestive tract, mouth, or gut.",
                    "explanation": "The passage confirms that tube worms possess no mouth or digestive tract."
                },
                {
                    "num": 3,
                    "type": "TFNG",
                    "prompt": "Vents remain active continuously for millions of years in the same location.",
                    "correct": "False",
                    "evidence": "vents can abruptly shut down within a matter of decades.",
                    "explanation": "The text explains vents are ephemeral and often shut down within decades."
                },
                {
                    "num": 4,
                    "type": "Completion",
                    "max_words": 2,
                    "prompt": "The mineral chimneys formed by superheated hydrothermal fluids are colloquially called _____.",
                    "acceptable": ["black smokers"],
                    "evidence": "This reaction constructs towering mineralized chimneys colloquially known as 'black smokers'.",
                    "explanation": "The text explicitly names the chimneys 'black smokers'."
                }
            ]
        }
    }

    @classmethod
    def get_passage(cls, passage_id: str = "acad_p1") -> Optional[Dict[str, Any]]:
        return cls.ORIGINAL_PASSAGES.get(passage_id)

    @classmethod
    def evaluate_test(cls, passage_id: str, user_answers: Dict[int, str]) -> Dict[str, Any]:
        """
        user_answers: {question_num: string_answer}
        """
        passage = cls.get_passage(passage_id)
        if not passage:
            raise ValueError(f"Passage {passage_id} not found")

        total = len(passage["questions"])
        correct_count = 0
        detailed_eval = []

        for q in passage["questions"]:
            qnum = q["num"]
            ans = user_answers.get(qnum, "")
            qtype = q["type"]

            if qtype == "TFNG":
                res = ReadingQuestionTypes.grade_tfng(
                    user_answer=ans,
                    correct_answer=q["correct"],
                    passage_evidence=q["evidence"],
                    explanation=q["explanation"]
                )
            elif qtype == "Completion":
                res = ReadingQuestionTypes.grade_completion(
                    user_answer=ans,
                    acceptable_answers=q["acceptable"],
                    max_words=q.get("max_words", 2),
                    passage_evidence=q["evidence"],
                    explanation=q["explanation"]
                )
            else:
                res = {
                    "type": qtype,
                    "user_answer": ans,
                    "correct_answer": q.get("correct", ""),
                    "is_correct": ans.strip().lower() == q.get("correct", "").strip().lower(),
                    "passage_evidence": q.get("evidence", ""),
                    "explanation": q.get("explanation", "")
                }

            res["question_num"] = qnum
            res["prompt"] = q["prompt"]
            if res["is_correct"]:
                correct_count += 1
            detailed_eval.append(res)

        # Scale band score based on Academic track
        band = BandCalculator.raw_to_band_reading(correct_count, track=passage["track"], total_questions=total)

        return {
            "passage_id": passage_id,
            "title": passage["title"],
            "track": passage["track"],
            "correct_answers": correct_count,
            "total_questions": total,
            "estimated_band": band,
            "results": detailed_eval,
            "reading_strategy_tips": [
                "Scan specifically for proper nouns, numbers, and technical terms (e.g. 'trophosome', '1977').",
                "Watch out for absolute qualifiers ('all', 'exclusively') which frequently flag 'False' statements."
            ],
            "disclaimer": BandCalculator.DISCLAIMER,
            "copyright_notice": "AI-generated original IELTS-style practice passage."
        }
