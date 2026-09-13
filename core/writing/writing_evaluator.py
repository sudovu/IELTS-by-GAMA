"""
Writing Evaluator for IELTS by GAMA.
Evaluates Academic Task 1 & 2 and General Training Task 1 & 2 according to
official IELTS band descriptor rubrics:
- Task Response / Achievement (TR/TA)
- Coherence and Cohesion (CC)
- Lexical Resource (LR)
- Grammatical Range and Accuracy (GRA)
Includes the formative 'Teach Through Correction' feedback suite.
"""

import re
from typing import Dict, Any, List, Optional
from .formative_feedback import FormativeFeedback
from ..scoring.criteria_evaluator import CriteriaEvaluator


class WritingEvaluator:
    """Automated IELTS writing diagnostic and rubric evaluator."""

    ORIGINAL_PROMPTS = {
        "acad_t1_energy": {
            "id": "acad_t1_energy",
            "task_type": "task_1",
            "track": "Academic",
            "title": "Renewable Energy Investment (2010–2020)",
            "prompt": (
                "The bar chart below shows government investments in solar, wind, and hydroelectric energy "
                "across four nations between 2010 and 2020.\n\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\n"
                "Write at least 150 words."
            )
        },
        "acad_t2_stem": {
            "id": "acad_t2_stem",
            "task_type": "task_2",
            "track": "Academic",
            "title": "STEM vs Humanities in Secondary Education",
            "prompt": (
                "Some educationalists argue that high school curricula should prioritize STEM subjects "
                "(Science, Technology, Engineering, and Mathematics) over creative arts and literature to ensure economic competitiveness. "
                "Others believe that artistic subjects are equally vital for developing well-rounded citizens.\n\n"
                "Discuss both views and give your own opinion.\n"
                "Write at least 250 words."
            )
        },
        "gen_t1_complaint": {
            "id": "gen_t1_complaint",
            "task_type": "task_1",
            "track": "General Training",
            "title": "Letter to Residential Landlord",
            "prompt": (
                "You recently moved into a new rental apartment and discovered that the central heating system is malfunctioning.\n"
                "Write a formal letter to your property manager. In your letter:\n"
                "• Explain the problem with the heating\n"
                "• Describe how this has affected your living situation\n"
                "• State clearly what action you expect them to take and when.\n"
                "Write at least 150 words."
            )
        },
        "gen_t2_remote_work": {
            "id": "gen_t2_remote_work",
            "task_type": "task_2",
            "track": "General Training",
            "title": "Advantages and Disadvantages of Remote Work",
            "prompt": (
                "An increasing number of employees now work remotely from home rather than in traditional office spaces. "
                "Do the advantages of remote working outweigh the disadvantages?\n\n"
                "Give reasons for your answer and include relevant examples from your own knowledge or experience.\n"
                "Write at least 250 words."
            )
        }
    }

    ACADEMIC_WORDS = {
        "substantial", "significant", "furthermore", "moreover", "consequently",
        "nevertheless", "predominantly", "demonstrate", "illustrate", "proportion",
        "fluctuate", "stabilize", "constitute", "concur", "perspective", "advocate",
        "phenomenon", "empirical", "methodology", "infrastructure"
    }

    COHESIVE_LINKERS = [
        "furthermore", "moreover", "in addition", "consequently", "therefore",
        "however", "on the other hand", "in contrast", "nevertheless", "to begin with",
        "ultimately", "in conclusion", "for instance", "for example"
    ]

    @classmethod
    def get_prompt(cls, prompt_id: str = "acad_t2_stem") -> Optional[Dict[str, Any]]:
        return cls.ORIGINAL_PROMPTS.get(prompt_id)

    @classmethod
    def evaluate_essay(
        cls,
        prompt_id: str,
        essay_text: str
    ) -> Dict[str, Any]:
        prompt_data = cls.get_prompt(prompt_id) or cls.ORIGINAL_PROMPTS["acad_t2_stem"]
        task_type = prompt_data["task_type"]
        track = prompt_data["track"]

        words = essay_text.strip().split()
        word_count = len(words)
        paragraphs = [p.strip() for p in essay_text.strip().split("\n\n") if p.strip()]
        para_count = len(paragraphs)

        # Baseline criteria starting around Band 6.0
        # 1. Task Response / Task Achievement
        min_words = 150 if task_type == "task_1" else 250
        tr_score = 6.0
        if word_count >= min_words:
            tr_score += 0.5
        if para_count >= 3:
            tr_score += 0.5
        if task_type == "task_2" and ("in conclusion" in essay_text.lower() or "to conclude" in essay_text.lower()):
            tr_score += 0.5
        tr_score = min(8.5, max(4.0, tr_score))

        # 2. Coherence and Cohesion
        cc_score = 6.0
        found_linkers = [l for l in cls.COHESIVE_LINKERS if l in essay_text.lower()]
        if len(found_linkers) >= 4:
            cc_score += 0.5
        if len(found_linkers) >= 7:
            cc_score += 0.5
        if para_count in [4, 5]:
            cc_score += 0.5
        cc_score = min(8.5, max(4.0, cc_score))

        # 3. Lexical Resource
        lr_score = 6.0
        words_lower = set([w.lower().strip(".,;:!?()") for w in words])
        academic_hits = words_lower.intersection(cls.ACADEMIC_WORDS)
        if len(academic_hits) >= 3:
            lr_score += 0.5
        if len(academic_hits) >= 6:
            lr_score += 1.0
        lr_score = min(8.5, max(4.0, lr_score))

        # 4. Grammatical Range and Accuracy
        formative_errors = FormativeFeedback.generate_formative_items(essay_text)
        gra_score = 6.5
        # Complex sentence check (subordinators)
        subordinators = ["although", "while", "whereas", "because", "since", "unless", "provided that"]
        has_complex = any(s in essay_text.lower() for s in subordinators)
        if has_complex:
            gra_score += 0.5
        if len(formative_errors) > 2:
            gra_score -= 1.0
        elif len(formative_errors) == 1:
            gra_score -= 0.5
        gra_score = min(8.5, max(4.0, gra_score))

        crit_feedback = {
            "Task Response / Achievement": f"Addressed prompt with {word_count} words across {para_count} paragraphs.",
            "Coherence and Cohesion": f"Identified {len(found_linkers)} discourse marker(s) ({', '.join(found_linkers[:4])}).",
            "Lexical Resource": f"Utilized {len(academic_hits)} high-utility academic term(s): {', '.join(academic_hits)}.",
            "Grammatical Range and Accuracy": f"Detected {len(formative_errors)} significant structural issue(s)."
        }

        eval_result = CriteriaEvaluator.evaluate_writing(
            task_type=task_type,
            track=track,
            text=essay_text,
            tr_score=tr_score,
            cc_score=cc_score,
            lr_score=lr_score,
            gra_score=gra_score,
            word_count=word_count,
            feedback_notes=crit_feedback
        )

        eval_result["formative_corrections"] = formative_errors
        eval_result["prompt_title"] = prompt_data["title"]
        return eval_result
