"""
Initial CEFR Diagnostic & English Assessment Engine for IELTS by GAMA.
Delivers comprehensive baseline assessment across skills and establishes personalized learning targets.
"""

from typing import Dict, Any, List
from .band_calculator import BandCalculator


class CEFRDiagnostic:
    """Diagnoses CEFR level, maps to IELTS band range, and identifies strengths/weaknesses."""

    DIAGNOSTIC_QUESTIONS = [
        {
            "id": "diag_g1",
            "skill": "grammar",
            "category": "Tenses & Conditionals",
            "prompt": "If government funding _____ (increase) next year, researchers will expand their clinical trials.",
            "options": ["increases", "will increase", "increased", "would increase"],
            "correct": "increases",
            "explanation": "First conditional uses present simple in the if-clause ('if funding increases')."
        },
        {
            "id": "diag_g2",
            "skill": "grammar",
            "category": "Subject-Verb Agreement",
            "prompt": "The collection of historical artifacts _____ (have/has) been preserved in the national archives.",
            "options": ["has", "have", "are having", "were"],
            "correct": "has",
            "explanation": "The subject is the singular collective noun 'The collection', so singular verb 'has' is required."
        },
        {
            "id": "diag_v1",
            "skill": "vocabulary",
            "category": "Academic Collocations",
            "prompt": "The statistical analysis revealed a _____ (profound / deep) discrepancy in the demographic data.",
            "options": ["profound", "deep", "heavy", "dense"],
            "correct": "profound",
            "explanation": "'Profound discrepancy' or 'significant discrepancy' is a standard academic collocation."
        },
        {
            "id": "diag_v2",
            "skill": "vocabulary",
            "category": "Phrasal Verbs & Precision",
            "prompt": "The university committee decided to _____ (account for / carry out) the new campus sustainability guidelines.",
            "options": ["carry out", "account for", "give in", "look into"],
            "correct": "carry out",
            "explanation": "'Carry out' means to execute or implement a plan/policy."
        },
        {
            "id": "diag_r1",
            "skill": "reading",
            "category": "Inference & Skimming",
            "prompt": "Passage: 'While solar energy adoption surged by 40% in urban regions, rural electrification still predominantly relies on biomass.' True, False, or Not Given: Rural areas primarily use solar power.",
            "options": ["False", "True", "Not Given"],
            "correct": "False",
            "explanation": "The passage explicitly states rural electrification still predominantly relies on biomass, contradicting the statement."
        },
        {
            "id": "diag_l1",
            "skill": "listening",
            "category": "Form Completion & Spelling",
            "prompt": "Speaker: 'The seminar will take place in the Henderson Auditorium on Thursday, 14th of October.' Question: The venue is the Henderson _____.",
            "options": ["Auditorium", "Hall", "Library", "Center"],
            "correct": "Auditorium",
            "explanation": "The speaker identified the venue as the Henderson Auditorium."
        }
    ]

    @classmethod
    def grade_diagnostic(cls, user_answers: Dict[str, str]) -> Dict[str, Any]:
        """
        Grades diagnostic responses and returns full diagnostic profile.
        user_answers: dict of {question_id: selected_option}
        """
        total = len(cls.DIAGNOSTIC_QUESTIONS)
        correct_count = 0
        skill_scores: Dict[str, Dict[str, int]] = {}
        mistakes: List[Dict[str, Any]] = []

        for q in cls.DIAGNOSTIC_QUESTIONS:
            qid = q["id"]
            skill = q["skill"]
            if skill not in skill_scores:
                skill_scores[skill] = {"correct": 0, "total": 0}
            skill_scores[skill]["total"] += 1

            ans = user_answers.get(qid, "").strip().lower()
            correct_ans = q["correct"].strip().lower()

            if ans == correct_ans:
                correct_count += 1
                skill_scores[skill]["correct"] += 1
            else:
                mistakes.append({
                    "skill": skill,
                    "category": q["category"],
                    "prompt": q["prompt"],
                    "user_answer": user_answers.get(qid, "No answer"),
                    "correct_answer": q["correct"],
                    "explanation": q["explanation"]
                })

        accuracy = correct_count / max(1, total)

        # CEFR Mapping
        if accuracy >= 0.85:
            cefr = "C1"
            ielts_range = "7.0 - 7.5"
            est_band = 7.0
        elif accuracy >= 0.65:
            cefr = "B2"
            ielts_range = "6.0 - 6.5"
            est_band = 6.0
        elif accuracy >= 0.45:
            cefr = "B1"
            ielts_range = "5.0 - 5.5"
            est_band = 5.0
        elif accuracy >= 0.25:
            cefr = "A2"
            ielts_range = "4.0 - 4.5"
            est_band = 4.0
        else:
            cefr = "A1"
            ielts_range = "3.0 - 3.5"
            est_band = 3.5

        strengths = []
        weaknesses = []
        for s, stats in skill_scores.items():
            rate = stats["correct"] / max(1, stats["total"])
            if rate >= 0.75:
                strengths.append(s.capitalize())
            else:
                weaknesses.append(s.capitalize())

        priority = weaknesses[0] if weaknesses else "Academic Vocabulary & Writing Task 2"

        return {
            "correct_count": correct_count,
            "total_questions": total,
            "accuracy_percent": round(accuracy * 100, 1),
            "estimated_cefr": cefr,
            "estimated_ielts_range": ielts_range,
            "estimated_band": est_band,
            "strengths": strengths or ["General Comprehension"],
            "weaknesses": weaknesses or ["None identified in preliminary screen"],
            "priority_skills": [priority],
            "recommended_study_plan": f"Daily 30-minute focus on {priority}, followed by Spaced Repetition vocabulary and Writing Task 2 practice.",
            "mistakes_to_record": mistakes,
            "disclaimer": BandCalculator.DISCLAIMER
        }
