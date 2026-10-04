"""
Writing Evaluator for IELTS by GAMA.
Evaluates Academic Task 1 & 2 and General Training Task 1 & 2 according to
official IELTS band descriptor rubrics:
- Task Response / Achievement (TR/TA)
- Coherence and Cohesion (CC)
- Lexical Resource (LR)
- Grammatical Range and Accuracy (GRA)
Includes the formative 'Teach Through Correction' feedback suite and
IELTS Advantage Question Analysis, PEEL Blueprint, and 10-Point Self-Assessment Questionnaire.
"""

import re
from typing import Dict, Any, List, Optional
from .formative_feedback import FormativeFeedback
from ..scoring.criteria_evaluator import CriteriaEvaluator


class WritingEvaluator:
    """Automated IELTS writing diagnostic, questionnaire, and rubric evaluator."""

    ORIGINAL_PROMPTS = {
        "acad_t2_stem": {
            "id": "acad_t2_stem",
            "task_type": "task_2",
            "question_type": "Discuss Both Views & Give Opinion",
            "track": "Academic",
            "title": "STEM vs Creative Arts in High School Curricula",
            "prompt": (
                "Some educationalists argue that high school curricula should prioritize STEM subjects "
                "(Science, Technology, Engineering, and Mathematics) over creative arts and literature to ensure economic competitiveness. "
                "Others believe that artistic subjects are equally vital for developing well-rounded citizens.\n\n"
                "Discuss both views and give your own opinion.\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Education & Curriculum Design",
                "micro_topic": "Whether secondary schools should prioritize STEM over Arts or maintain balance",
                "task_words": "Discuss BOTH views and GIVE YOUR OWN OPINION",
                "coffee_shop_idea": "STEM drives economic innovation and tech careers, but the arts foster creative problem-solving and emotional intelligence. Both are essential in modern society.",
                "peel_blueprint": {
                    "body_1": "Point: STEM disciplines directly power technological modernization. Explain: Industry demands engineers and data analysts. Example: Developing nations investing in tech hubs witnessed 15% faster GDP growth. Link: Therefore, STEM merits robust institutional funding.",
                    "body_2": "Point: Conversely, creative arts nurture lateral thinking and emotional intelligence. Explain: Pure technical knowledge without creativity limits innovation. Example: Pioneering tech firms specifically recruit designers and humanists. Link: Thus, neglecting artistic disciplines produces an imbalanced workforce."
                }
            }
        },
        "acad_t2_ubi": {
            "id": "acad_t2_ubi",
            "task_type": "task_2",
            "question_type": "Agree or Disagree (Opinion)",
            "track": "Academic",
            "title": "Universal Basic Income & Workplace Automation",
            "prompt": (
                "As artificial intelligence and robotics automate routine workplace tasks, some economists propose that governments "
                "should introduce a guaranteed Universal Basic Income (UBI) for all adult citizens to eradicate poverty.\n\n"
                "To what extent do you agree or disagree with this proposal?\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Technology, Economics & Social Welfare",
                "micro_topic": "Whether automated job displacement warrants a state-funded Universal Basic Income",
                "task_words": "To what extent do you agree or disagree (Clear position throughout required)",
                "coffee_shop_idea": "I agree to a substantial extent because AI will displace entry-level workers faster than new industries can retrain them, and UBI prevents societal destitution.",
                "peel_blueprint": {
                    "body_1": "Point: Automation is displacing routine white-collar and manual jobs at unprecedented scale. Explain: Displaced workers cannot retrain overnight without subsistence support. Example: Autonomous transport and logistics could eliminate millions of driving jobs within a decade. Link: UBI provides an indispensable financial safety net.",
                    "body_2": "Point: Skeptics argue UBI disincentivizes work, but empirical trials refute this. Explain: Basic security enables citizens to pursue education, caregiving, or entrepreneurial ventures. Example: Finnish pilot programs demonstrated participants suffered no loss of motivation while mental wellness improved. Link: Consequently, UBI bolsters rather than undermines civic productivity."
                }
            }
        },
        "acad_t2_tourism": {
            "id": "acad_t2_tourism",
            "task_type": "task_2",
            "question_type": "Advantages vs Disadvantages",
            "track": "Academic",
            "title": "International Mass Tourism & Cultural Preservation",
            "prompt": (
                "In many regions across the globe, international mass tourism has become the primary source of economic revenue, "
                "yet it frequently leads to environmental degradation and the commercialization of local cultures.\n\n"
                "Do the advantages of international tourism outweigh the disadvantages?\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Tourism & Cultural Heritage",
                "micro_topic": "Whether economic dividends of mass tourism exceed its environmental and cultural costs",
                "task_words": "Do advantages OUTWEIGH disadvantages (Must compare weight and make explicit judgment)",
                "coffee_shop_idea": "Tourism brings huge money and jobs, but unmanaged tourism ruins fragile monuments and drives locals out. On balance, advantages outweigh only if strictly regulated.",
                "peel_blueprint": {
                    "body_1": "Point: Tourism generates massive foreign exchange and infrastructure investment. Explain: Remote heritage sites obtain funds that regional governments could not otherwise allocate. Example: Island economies in Southeast Asia finance coastal conservation largely through eco-tourism levies. Link: This economic catalyst is indispensable.",
                    "body_2": "Point: However, uncontrolled overtourism causes severe gentrification and environmental damage. Explain: Skyrocketing rents displace indigenous populations and fragile ecosystems suffer degradation. Example: Cities like Venice and Barcelona have imposed tourist caps to prevent cultural erosion. Link: Therefore, while advantages predominate, stringent visitor management is imperative."
                }
            }
        },
        "acad_t2_traffic": {
            "id": "acad_t2_traffic",
            "task_type": "task_2",
            "question_type": "Causes & Solutions",
            "track": "Academic",
            "title": "Urban Traffic Congestion & Environmental Mitigation",
            "prompt": (
                "Traffic congestion in major metropolitan centers has reached critical levels, leading to severe air pollution, "
                "reduced economic productivity, and chronic public health issues.\n\n"
                "What are the primary causes of this phenomenon, and what effective measures can municipal authorities adopt to resolve it?\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Urban Planning & Environmental Health",
                "micro_topic": "Causes of urban vehicle gridlock and practical municipal solutions",
                "task_words": "What are CAUSES and what are EFFECTIVE MEASURES (Both must be thoroughly developed)",
                "coffee_shop_idea": "People drive because public transit is unreliable or expensive, and cities expand without proper planning. Solutions: heavy congestion pricing and investing in clean, reliable metro rail.",
                "peel_blueprint": {
                    "body_1": "Point: The root cause of congestion is inadequate public transit combined with low fuel taxation. Explain: Commuters default to private automobiles when trains are crowded, unreliable, or nonexistent. Example: Car ownership in suburban commuter belts surged by 35% where bus networks were pruned. Link: This directly fuels daily urban gridlock.",
                    "body_2": "Point: The most potent remedy is introducing dynamic congestion charges alongside subsidized rail transit. Explain: Financial penalties disincentivize discretionary car trips while fare subsidies make public transit the rational choice. Example: London's congestion charge reduced inner-city vehicle traffic by 20% within two years. Link: Sustained municipal commitment to transit infrastructure resolves the crisis."
                }
            }
        },
        "acad_t2_fast_fashion": {
            "id": "acad_t2_fast_fashion",
            "task_type": "task_2",
            "question_type": "Two-Part Direct Questions",
            "track": "Academic",
            "title": "Fast Fashion, Consumer Culture & Global Sustainability",
            "prompt": (
                "Consumers worldwide are purchasing substantially more inexpensive, short-lived clothing than previous generations, "
                "a trend widely known as 'fast fashion'.\n\n"
                "Why has this phenomenon emerged, and is this a positive or negative development for society?\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Consumerism, Industry & Environment",
                "micro_topic": "Reasons for the rise of fast fashion and evaluation of whether it is beneficial or detrimental",
                "task_words": "WHY has this emerged? AND IS IT POSITIVE OR NEGATIVE? (Must answer both distinct questions)",
                "coffee_shop_idea": "It emerged because targeted social media ads and cheap overseas manufacturing make trendy clothes dirt cheap. It is overwhelmingly negative because of textile waste and sweatshop labor.",
                "peel_blueprint": {
                    "body_1": "Point: Fast fashion expanded due to digital influencer marketing and low-cost overseas supply chains. Explain: Social media algorithms create micro-trends, inducing consumers to feel outdated after a single wear. Example: Retail platforms refresh clothing lines weekly at negligible prices. Link: These technological and commercial factors ignited runaway consumption.",
                    "body_2": "Point: This development is unequivocally negative due to catastrophic environmental and ethical fallout. Explain: Synthetic textiles shed microplastics into waterways, and massive garment dumps pollute landfills in developing nations. Example: The fashion sector accounts for roughly 10% of global carbon emissions and fosters exploitative sweatshops. Link: Consequently, the transient pleasure of cheap clothing carries an unacceptable societal toll."
                }
            }
        },
        "acad_t1_energy": {
            "id": "acad_t1_energy",
            "task_type": "task_1",
            "question_type": "Data Report (Bar Chart)",
            "track": "Academic",
            "title": "Renewable Energy Investment (2010–2020)",
            "prompt": (
                "The bar chart below shows government investments in solar, wind, and hydroelectric energy "
                "across four nations between 2010 and 2020.\n\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Energy Economics",
                "micro_topic": "Comparative government investments in renewable energy sectors",
                "task_words": "Select and report main features, make comparisons (Do NOT give personal opinions)",
                "coffee_shop_idea": "Solar grew the fastest in country A and B, wind was steady, and hydro remained flat. Country C invested the most overall.",
                "peel_blueprint": {
                    "body_1": "Overview: Solar investment experienced exponential growth across all nations, while hydroelectric remained static.",
                    "body_2": "Details: Key numerical comparisons highlighting the initial and final decade values."
                }
            }
        }
    }

    ACADEMIC_WORDS = {
        "substantial", "significant", "furthermore", "moreover", "consequently",
        "nevertheless", "predominantly", "demonstrate", "illustrate", "proportion",
        "fluctuate", "stabilize", "constitute", "concur", "perspective", "advocate",
        "phenomenon", "empirical", "methodology", "infrastructure", "disparity",
        "paramount", "detrimental", "catalyst", "substantiate", "ameliorate"
    }

    COHESIVE_LINKERS = [
        "furthermore", "moreover", "in addition", "consequently", "therefore",
        "however", "on the other hand", "in contrast", "nevertheless", "to begin with",
        "ultimately", "in conclusion", "for instance", "for example", "notwithstanding",
        "on balance", "in stark contrast", "a compelling case in point"
    ]

    @classmethod
    def list_prompts(cls) -> List[Dict[str, Any]]:
        return [
            {
                "id": p["id"],
                "title": p["title"],
                "task_type": p["task_type"],
                "question_type": p.get("question_type", "Essay"),
                "track": p["track"]
            }
            for p in cls.ORIGINAL_PROMPTS.values()
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

        # 1. Task Response / Task Achievement
        min_words = 150 if task_type == "task_1" else 250
        tr_score = 6.0
        if word_count >= min_words:
            tr_score += 0.5
        if para_count >= 3:
            tr_score += 0.5
        if task_type == "task_2" and ("in conclusion" in essay_text.lower() or "to conclude" in essay_text.lower() or "on balance" in essay_text.lower()):
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
        subordinators = ["although", "while", "whereas", "because", "since", "unless", "provided that"]
        has_complex = any(s in essay_text.lower() for s in subordinators)
        if has_complex:
            gra_score += 0.5
        if len(formative_errors) > 2:
            gra_score -= 1.0
        elif len(formative_errors) == 1:
            gra_score -= 0.5
        gra_score = min(8.5, max(4.0, gra_score))

        # IELTS Advantage Questionnaire Checklist
        checklist = [
            {"item": "Answered all parts of the question prompt", "passed": word_count >= min_words and para_count >= 3},
            {"item": "Clear thesis position stated in introduction and conclusion", "passed": any(k in essay_text.lower() for k in ["i argue", "i believe", "my opinion", "in conclusion", "to conclude", "on balance"])},
            {"item": "Paragraph structure: 4-5 well-developed paragraphs", "passed": para_count in [4, 5]},
            {"item": "Substantial word count (above minimum threshold)", "passed": word_count >= min_words},
            {"item": "Cohesive linkers and discourse signposts present", "passed": len(found_linkers) >= 4},
            {"item": "Band 7+ academic topic vocabulary utilized", "passed": len(academic_hits) >= 3},
            {"item": "Complex subordinate clauses and conditionals present", "passed": has_complex},
            {"item": "Grammatical accuracy without basic subject-verb errors", "passed": len(formative_errors) == 0}
        ]

        passed_checks = sum(1 for c in checklist if c["passed"])

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
        eval_result["question_type"] = prompt_data.get("question_type", "Essay")
        eval_result["advantage_checklist"] = checklist
        eval_result["passed_checklist_count"] = passed_checks
        eval_result["advantage_analysis"] = prompt_data.get("advantage_analysis", {})
        return eval_result
