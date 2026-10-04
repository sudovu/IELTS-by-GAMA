"""
Grammar Engine for IELTS by GAMA.
Covers 24 foundational English grammar categories, diagnoses common errors,
and formats formative feedback following the 'Teach Through Correction' paradigm:
ORIGINAL -> CORRECTION -> WHY -> BETTER ALTERNATIVE -> PRACTICE EXERCISE.
Includes interactive Grammar Fill-Up (Cloze) drills and sentence architecture drills.
"""

import re
from typing import Dict, Any, List, Optional


class GrammarEngine:
    """Diagnoses grammatical errors and teaches underlying linguistic mechanics."""

    # 24 core grammatical syllabus areas
    TOPICS = [
        "Parts of Speech", "Articles", "Tenses", "Subject-Verb Agreement",
        "Pronouns", "Prepositions", "Modal Verbs", "Conditionals",
        "Passive Voice", "Reported Speech", "Relative Clauses", "Gerunds & Infinitives",
        "Comparatives & Superlatives", "Question Formation", "Word Order", "Determiners & Quantifiers",
        "Adverbial Clauses", "Complex Sentences", "Compound Sentences", "Punctuation",
        "Parallel Structure", "Inversion", "Subjunctive & Unreal Past", "Cohesive Linkers"
    ]

    # Heuristic diagnostic patterns
    ERROR_RULES = [
        {
            "pattern": r"\b(i|we|they|you)\s+am\s+agree\b",
            "category": "Subject-Verb Agreement",
            "correction_sub": r"\1 agree",
            "why": "'Agree' is an action verb in English and does not use the auxiliary 'am' in the simple present tense.",
            "better_alternative": "I strongly concur with this perspective.",
            "exercise": "Fill in the blank: 'Many economists _____ (agree / are agree) with this forecast.' (Answer: agree)"
        },
        {
            "pattern": r"\ba\s+information\b",
            "category": "Articles",
            "correction_sub": "information (or 'a piece of information')",
            "why": "'Information' is an uncountable noun and cannot be preceded by the indefinite article 'a'.",
            "better_alternative": "a crucial piece of evidence / empirical data",
            "exercise": "Correct this phrase: 'He gave me a good advice.' -> 'He gave me _____ (good advice / a good advice)' (Answer: good advice)"
        },
        {
            "pattern": r"\b(each|every)\s+of\s+the\s+students\s+are\b",
            "category": "Subject-Verb Agreement",
            "correction_sub": r"\1 of the students is",
            "why": "'Each' and 'every' take a singular verb when acting as the head subject.",
            "better_alternative": "Every participant exhibits...",
            "exercise": "Choose the correct verb: 'Each of the experiments _____ (was / were) conclusive.' (Answer: was)"
        },
        {
            "pattern": r"\bmore\s+easier\b",
            "category": "Comparatives & Superlatives",
            "correction_sub": "easier",
            "why": "Two comparative markers ('more' and '-er') cannot be applied to the same adjective.",
            "better_alternative": "considerably more straightforward",
            "exercise": "Correct: 'This method is more faster.' -> 'This method is _____.' (Answer: faster)"
        },
        {
            "pattern": r"\bdiscuss\s+about\b",
            "category": "Prepositions",
            "correction_sub": "discuss",
            "why": "'Discuss' is a transitive verb that takes a direct object without the preposition 'about'.",
            "better_alternative": "deliberate on / explore the nuances of",
            "exercise": "Correct: 'We need to discuss about the budget.' -> 'We need to discuss _____.' (Answer: the budget)"
        },
        {
            "pattern": r"\bdespite\s+of\b",
            "category": "Prepositions",
            "correction_sub": "despite (or 'in spite of')",
            "why": "'Despite' is a preposition used without 'of'. 'In spite of' requires 'of'.",
            "better_alternative": "notwithstanding / despite the prevailing challenges",
            "exercise": "Choose: '_____ (Despite / In spite) of the rainfall, the match continued.' (Answer: In spite)"
        },
        {
            "pattern": r"\bresponsible\s+of\b",
            "category": "Prepositions",
            "correction_sub": "responsible for",
            "why": "The adjective 'responsible' takes the dependent preposition 'for' when indicating duty or cause.",
            "better_alternative": "held accountable for / tasked with overseeing",
            "exercise": "Fill in the preposition: 'Governments are responsible _____ public health.' (Answer: for)"
        }
    ]

    FILL_UP_DRILLS = [
        {
            "id": "fill_cond_1",
            "category": "Conditionals",
            "prompt": "If municipal authorities _____ (invest) in efficient light rail a decade ago, traffic congestion would not be so acute today.",
            "acceptable": ["had invested"],
            "explanation": "Mixed conditional: Past condition ('had invested') producing a present result ('would not be so acute').",
            "band_note": "Mixed conditionals demonstrate Band 8+ Grammatical Range and Accuracy."
        },
        {
            "id": "fill_cond_2",
            "category": "Conditionals",
            "prompt": "If the government were to raise carbon taxes, corporations _____ (seek) cleaner manufacturing alternatives.",
            "acceptable": ["would seek"],
            "explanation": "Second conditional (unreal/hypothetical): 'were to + verb' in the if-clause requires 'would + base verb' in the main clause.",
            "band_note": "Ideal for proposing policy recommendations in IELTS Writing Task 2."
        },
        {
            "id": "fill_pass_1",
            "category": "Passive Voice & Impersonal Structures",
            "prompt": "It is widely _____ (argue) by sociologists that early childhood education bridges socioeconomic divides.",
            "acceptable": ["argued", "contended", "believed"],
            "explanation": "Impersonal passive reporting: 'It is + past participle + that-clause' establishes objective academic tone.",
            "band_note": "Replaces informal 'People think that' with Band 7+ academic objectivity."
        },
        {
            "id": "fill_pass_2",
            "category": "Passive Voice & Impersonal Structures",
            "prompt": "Comprehensive clinical trials must be _____ (carry out) before new vaccines receive regulatory approval.",
            "acceptable": ["carried out", "conducted"],
            "explanation": "Modal passive: 'must be + past participle'. Note 'carried out' is the past participle of the phrasal verb 'carry out'.",
            "band_note": "Modal passives add precision when discussing regulations and mandates."
        },
        {
            "id": "fill_sva_1",
            "category": "Subject-Verb Agreement",
            "prompt": "The rapid expansion of metropolitan rail networks _____ (have / has) reduced average commuting times.",
            "acceptable": ["has"],
            "explanation": "The head subject is 'The rapid expansion' (singular), not the intervening plural noun 'networks'.",
            "band_note": "Classic IELTS distractor: do not let intervening plural nouns mislead your verb concord."
        },
        {
            "id": "fill_sva_2",
            "category": "Subject-Verb Agreement",
            "prompt": "Each of the experimental samples _____ (was / were) preserved at sub-zero temperatures.",
            "acceptable": ["was"],
            "explanation": "'Each of + plural noun' always takes a singular verb in standard formal English.",
            "band_note": "Essential precision rule for both Academic Task 1 and Task 2."
        },
        {
            "id": "fill_inv_1",
            "category": "Inversion",
            "prompt": "Not only _____ (do / does / did) automated robotics increase production velocity, but they also minimize industrial accidents.",
            "acceptable": ["do"],
            "explanation": "Negative/restrictive adverbial inversion: 'Not only + auxiliary verb (do) + plural subject (robotics) + main verb'.",
            "band_note": "Inversion structures are an explicit descriptor indicator for Band 8+ Grammatical Range."
        },
        {
            "id": "fill_inv_2",
            "category": "Inversion",
            "prompt": "Seldom _____ (have / has / do) researchers witnessed such rapid biodiversity recovery in a protected reserve.",
            "acceptable": ["have"],
            "explanation": "Adverbial inversion with 'Seldom': auxiliary 'have' precedes the plural subject 'researchers'.",
            "band_note": "Dramatic emphasis structure that stands out to examiners in essays."
        },
        {
            "id": "fill_rel_1",
            "category": "Relative & Participle Clauses",
            "prompt": "_____ (Having / Have / Had) scrutinized the financial telemetry, the board authorized the merger.",
            "acceptable": ["Having"],
            "explanation": "Perfect participle clause ('Having + past participle') indicates an action completed before the main clause verb.",
            "band_note": "Combines two sentences seamlessly without overusing basic connectors like 'and' or 'so'."
        },
        {
            "id": "fill_prep_1",
            "category": "Prepositions & Concordance",
            "prompt": "Heavy commercial vehicle emissions exert a profoundly detrimental impact _____ (on / in / at) air quality.",
            "acceptable": ["on", "upon"],
            "explanation": "The noun 'impact' takes the dependent preposition 'on' (or 'upon').",
            "band_note": "Collocational prepositions must be exact to secure Band 7+ Lexical and Grammatical accuracy."
        },
        {
            "id": "fill_hedge_1",
            "category": "Hedging & Modality",
            "prompt": "The empirical findings tend to _____ (suggest / suggests / suggesting) that remote work improves employee retention.",
            "acceptable": ["suggest"],
            "explanation": "'Tend to + base infinitive verb' is an academic hedging device preventing unsubstantiated over-generalization.",
            "band_note": "IELTS examiners penalize sweeping absolutes. Hedging with 'tends to suggest' aligns with Band 8+ academic style."
        },
        {
            "id": "fill_art_1",
            "category": "Articles & Countability",
            "prompt": "Professor Vance provided invaluable _____ (advice / advices) regarding methodology design.",
            "acceptable": ["advice"],
            "explanation": "'Advice' is strictly uncountable in English and can never take a plural '-s' or indefinite 'an'.",
            "band_note": "Common error among non-native candidates; examiners penalize 'an advice' or 'advices'."
        }
    ]

    @classmethod
    def get_fill_up_drills(cls, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns cloze fill-up drills filtered by category or all drills."""
        if category:
            return [d for d in cls.FILL_UP_DRILLS if d["category"].lower() == category.lower()]
        return cls.FILL_UP_DRILLS

    @classmethod
    def evaluate_fill_up(cls, drill_id: str, user_answer: str) -> Dict[str, Any]:
        """Validates a learner's fill-in-the-blank answer."""
        drill = next((d for d in cls.FILL_UP_DRILLS if d["id"] == drill_id), None)
        if not drill:
            return {"is_correct": False, "error": f"Drill {drill_id} not found"}

        cleaned_user = user_answer.strip().lower()
        is_correct = any(cleaned_user == acc.lower() for acc in drill["acceptable"])

        return {
            "drill_id": drill_id,
            "category": drill["category"],
            "user_answer": user_answer,
            "is_correct": is_correct,
            "acceptable_answers": drill["acceptable"],
            "explanation": drill["explanation"],
            "band_note": drill.get("band_note", "")
        }

    @classmethod
    def check_sentence(cls, sentence: str) -> List[Dict[str, Any]]:
        """Scans sentence for grammatical errors and returns structured formative feedback."""
        diagnoses = []
        for rule in cls.ERROR_RULES:
            match = re.search(rule["pattern"], sentence, flags=re.IGNORECASE)
            if match:
                matched_str = match.group(0)
                corrected_str = re.sub(rule["pattern"], rule["correction_sub"], matched_str, flags=re.IGNORECASE)
                diagnoses.append({
                    "original": matched_str,
                    "full_sentence": sentence,
                    "category": rule["category"],
                    "correction": corrected_str,
                    "why": rule["why"],
                    "better_alternative": rule["better_alternative"],
                    "practice_exercise": rule["exercise"]
                })
        return diagnoses

    @classmethod
    def format_teach_through_correction(cls, error_dict: Dict[str, Any]) -> str:
        """Renders the prompt-mandated 5-point formative explanation."""
        return (
            f"**ORIGINAL:**\n\"{error_dict['original']}\"\n\n"
            f"**CORRECTION:**\n\"{error_dict['correction']}\"\n\n"
            f"**WHY:**\n{error_dict['why']}\n\n"
            f"**BETTER ALTERNATIVE (IELTS Band 7+):**\n{error_dict['better_alternative']}\n\n"
            f"**PRACTICE EXERCISE:**\n{error_dict['practice_exercise']}"
        )

    @classmethod
    def get_topic_lesson(cls, topic_name: str) -> Dict[str, Any]:
        """Provides curriculum outline and reference explanation for a grammar topic."""
        lessons = {
            "Articles": {
                "title": "Articles: Definite (The), Indefinite (A/An), and Zero Article",
                "rules": [
                    "Use 'a/an' with singular countable nouns mentioned for the first time.",
                    "Use 'the' when both speaker and listener know the specific referent, or with unique entities ('the sun', 'the government').",
                    "Use zero article with plural countable and uncountable nouns used in a general sense ('Water is essential', 'Students need sleep')."
                ],
                "academic_tip": "In IELTS Writing Task 1, always use 'the' with trends and figures: 'The proportion of students...', 'The number of vehicles...'"
            },
            "Subject-Verb Agreement": {
                "title": "Subject-Verb Agreement in Complex Academic Clauses",
                "rules": [
                    "Intervening prepositional phrases do not change the subject number: 'The quality of the research papers is high.'",
                    "Indefinite pronouns ('each', 'everyone', 'neither') take singular verbs.",
                    "Compound subjects joined by 'and' take plural verbs ('Poverty and unemployment contribute...')."
                ],
                "academic_tip": "Check sentences where the noun closest to the verb is plural but the true subject is singular."
            },
            "Conditionals": {
                "title": "Conditionals for Argumentation (Zero, First, Second, Third, Mixed)",
                "rules": [
                    "Zero: 'If temperature rises, ice melts.' (Universal truth)",
                    "First: 'If policies change, society will benefit.' (Real future condition)",
                    "Second: 'If governments banned fossil fuels, emissions would drop.' (Hypothetical present/future)",
                    "Third: 'If the team had verified the samples, errors would have been prevented.' (Unreal past)",
                    "Mixed: 'If authorities had planned earlier, the city would not face gridlock today.' (Past action -> Present result)"
                ],
                "academic_tip": "Using second and third conditionals in IELTS Writing Task 2 demonstrates Grammatical Range for Band 7+."
            },
            "Inversion": {
                "title": "Adverbial Inversion for Band 8+ Rhetorical Precision",
                "rules": [
                    "Front negative or limiting adverbials ('Not only', 'Seldom', 'Rarely', 'Under no circumstances').",
                    "Place the auxiliary verb immediately after the adverbial: 'Not only does automation save time...'",
                    "Never invert the main verb directly unless it is a form of 'be'."
                ],
                "academic_tip": "Use inversion sparingly (1-2 times per essay) to accentuate high-impact arguments without sounding artificial."
            },
            "Passive Voice": {
                "title": "Academic Passive Voice and Impersonal Reporting",
                "rules": [
                    "Form with appropriate tense of 'be' + past participle ('has been archived', 'were investigated').",
                    "Use impersonal reporting structures: 'It is widely contended that...', 'X is believed to have...'",
                    "Omit the agent ('by someone') when the agent is irrelevant, unknown, or obvious."
                ],
                "academic_tip": "Essential for Academic Writing Task 1 process diagrams and Task 2 objective argument development."
            }
        }
        return lessons.get(topic_name, {
            "title": f"Mastery Guide: {topic_name}",
            "rules": [f"Understand the structural function of {topic_name} in formal academic communication."],
            "academic_tip": f"Maintain precision and grammatical accuracy when utilizing {topic_name} under IELTS exam conditions."
        })
