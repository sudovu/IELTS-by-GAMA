"""
Initial CEFR Diagnostic & English Assessment Engine for IELTS by GAMA.
Delivers comprehensive baseline assessment across skills and establishes personalized learning targets.
Expanded to 12 diagnostic assessment questions incorporating IELTS Advantage question analysis principles.
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
            "id": "diag_g3",
            "skill": "grammar",
            "category": "Inversion for Band 8+",
            "prompt": "Not only _____ the new policy reduce carbon emissions, but it also stimulated clean tech employment.",
            "options": ["did", "does", "had", "will"],
            "correct": "did",
            "explanation": "Past tense negative adverbial inversion: 'Not only did the new policy reduce...' requires auxiliary 'did' before the subject."
        },
        {
            "id": "diag_g4",
            "skill": "grammar",
            "category": "Articles & Countability",
            "prompt": "The academic supervisor offered invaluable _____ regarding the thesis methodology.",
            "options": ["advice", "an advice", "advices", "a piece of advices"],
            "correct": "advice",
            "explanation": "'Advice' is an uncountable noun that takes zero article in general reference and never adds '-s'."
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
            "id": "diag_v3",
            "skill": "vocabulary",
            "category": "Lexical Upgrades (Band 8+)",
            "prompt": "Which phrasing represents a Band 8+ academic upgrade for 'a big change' in IELTS Writing?",
            "options": ["a substantial transformation", "a huge difference", "a super big shift", "a massive modification"],
            "correct": "a substantial transformation",
            "explanation": "'Substantial transformation' or 'marked disparity' is precise formal academic register."
        },
        {
            "id": "diag_v4",
            "skill": "vocabulary",
            "category": "Academic Verb Collocations",
            "prompt": "Wind and solar energy now _____ for approximately 28% of national electrical capacity.",
            "options": ["account", "amount", "constitute for", "represent of"],
            "correct": "account",
            "explanation": "'Account for' is the established academic collocation meaning 'to make up or constitute a proportion'."
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
            "id": "diag_r2",
            "skill": "reading",
            "category": "TFNG Distractor Traps",
            "prompt": "Passage: 'The high-speed rail line opened in 2021 and carries 50,000 commuters daily.' True, False, or Not Given: The high-speed rail line is faster than previous diesel engines.",
            "options": ["Not Given", "True", "False"],
            "correct": "Not Given",
            "explanation": "Although likely true in real life, the passage mentions opening date and passenger volume, with NO comparison to diesel engines."
        },
        {
            "id": "diag_l1",
            "skill": "listening",
            "category": "Form Completion & Spelling",
            "prompt": "Speaker: 'The seminar will take place in the Henderson Auditorium on Thursday, 14th of October.' Question: The venue is the Henderson _____.",
            "options": ["Auditorium", "Hall", "Library", "Center"],
            "correct": "Auditorium",
            "explanation": "The speaker identified the venue as the Henderson Auditorium."
        },
        {
            "id": "diag_m1",
            "skill": "methodology",
            "category": "IELTS Advantage Question Analysis",
            "prompt": "According to the IELTS Advantage methodology, what is the crucial first step before writing any Task 2 essay?",
            "options": [
                "Analyze the general topic, micro-topic, and task instruction words",
                "Immediately start writing introductory sentences to save time",
                "Memorize 10 complicated idioms to impress the examiner",
                "Write down as many synonyms as possible"
            ],
            "correct": "Analyze the general topic, micro-topic, and task instruction words",
            "explanation": "IELTS Advantage emphasizes that 50% of Task Response success lies in analyzing the precise micro-topic and task instruction words."
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

        accuracy_pct = (correct_count / total) * 100.0 if total > 0 else 0.0

        # Map accuracy percentage to CEFR and IELTS baseline
        if accuracy_pct >= 90.0:
            cefr = "C1"
            estimated_band = 7.5
            range_str = "7.5 - 8.5"
        elif accuracy_pct >= 75.0:
            cefr = "B2"
            estimated_band = 6.5
            range_str = "6.5 - 7.5"
        elif accuracy_pct >= 55.0:
            cefr = "B1"
            estimated_band = 5.5
            range_str = "5.5 - 6.5"
        elif accuracy_pct >= 35.0:
            cefr = "A2"
            estimated_band = 4.5
            range_str = "4.5 - 5.5"
        else:
            cefr = "A1"
            estimated_band = 3.5
            range_str = "3.5 - 4.5"

        # Identify strengths and priorities
        strengths = []
        priorities = []
        for sk, sc in skill_scores.items():
            rate = sc["correct"] / sc["total"] if sc["total"] > 0 else 0.0
            capitalized_skill = sk.capitalize()
            if rate >= 0.7:
                strengths.append(capitalized_skill)
            else:
                priorities.append(capitalized_skill)

        if not priorities:
            priorities = ["Band 8+ Rhetorical Inversion", "Advanced Lexical Collocations"]

        return {
            "accuracy_percent": round(accuracy_pct, 1),
            "correct_count": correct_count,
            "total_questions": total,
            "estimated_cefr": cefr,
            "estimated_ielts_range": range_str,
            "estimated_band": estimated_band,
            "skill_breakdown": skill_scores,
            "strengths": strengths,
            "priority_skills": priorities,
            "mistakes_to_record": mistakes,
            "recommended_study_plan": (
                f"Based on your {cefr} baseline (Band ~{estimated_band}), prioritize {', '.join(priorities)}. "
                "Leverage the IELTS Advantage Question Analysis Questionnaire and daily SRS vocabulary flashcards."
            ),
            "disclaimer": BandCalculator.DISCLAIMER
        }
