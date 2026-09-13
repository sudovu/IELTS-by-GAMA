"""
Grammar Engine for IELTS by GAMA.
Covers 24 foundational English grammar categories, diagnoses common errors,
and formats formative feedback following the 'Teach Through Correction' paradigm:
ORIGINAL -> CORRECTION -> WHY -> BETTER ALTERNATIVE -> PRACTICE EXERCISE.
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
                    "Third: 'If the team had verified the samples, errors would have been prevented.' (Unreal past)"
                ],
                "academic_tip": "Using second and third conditionals in IELTS Writing Task 2 demonstrates Grammatical Range for Band 7+."
            }
        }
        return lessons.get(topic_name, {
            "title": f"Mastery Guide: {topic_name}",
            "rules": [f"Understand the structural function of {topic_name} in formal academic communication."],
            "academic_tip": f"Maintain precision and grammatical accuracy when utilizing {topic_name} under IELTS exam conditions."
        })
