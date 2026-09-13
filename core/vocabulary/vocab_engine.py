"""
Vocabulary Engine for IELTS by GAMA.
Comprehensive vocabulary system covering:
- Lexical items with IPA, meaning, POS, examples, word forms, collocations
- Phrasal verbs with formal academic equivalents
- Pragmatic idioms with register safety warnings
- Word families (noun, verb, adjective, adverb, negative forms)
- Natural collocations and practice drills
"""

from typing import Dict, Any, List, Optional


class VocabEngine:
    """Manages academic and general vocabulary, collocations, phrasal verbs, and word families."""

    ACADEMIC_VOCAB = {
        "substantial": {
            "word": "substantial",
            "meaning": "Of considerable importance, size, or worth.",
            "pos": "adjective",
            "pronunciation": "/səbˈstæn.ʃəl/",
            "cefr": "C1",
            "band_tier": "Band 7-8",
            "example": "There has been a substantial increase in public transport usage over the last decade.",
            "word_family": {
                "noun": "substance",
                "verb": "substantiate",
                "adjective": "substantial",
                "adverb": "substantially",
                "negative": "insubstantial"
            },
            "collocations": ["substantial increase", "substantial evidence", "substantial portion", "substantial difference"],
            "synonyms": ["considerable", "significant", "sizeable", "momentous"],
            "antonyms": {
                "direct": "negligible",
                "contextual": "slight, minor, insubstantial"
            },
            "common_mistake": "Do not confuse with 'substantive' (which means having a firm basis in reality or essential).",
            "context": "Ideal for IELTS Writing Task 1 trends and Task 2 evidence presentation."
        },
        "fluctuate": {
            "word": "fluctuate",
            "meaning": "To rise and fall irregularly in number or amount.",
            "pos": "verb",
            "pronunciation": "/ˈflʌk.tʃu.eɪt/",
            "cefr": "B2/C1",
            "band_tier": "Band 7",
            "example": "Vegetable prices fluctuated wildly throughout the monsoon season.",
            "word_family": {
                "noun": "fluctuation",
                "verb": "fluctuate",
                "adjective": "fluctuating",
                "adverb": "fluctuatingly",
                "negative": "unfluctuating (rare)"
            },
            "collocations": ["fluctuate wildly", "fluctuate between X and Y", "fluctuate over time"],
            "synonyms": ["oscillate", "vary", "waver", "alternate"],
            "antonyms": {
                "direct": "stabilize",
                "contextual": "remain steady, plateau"
            },
            "common_mistake": "Say 'fluctuate between A and B', not 'fluctuate from A to B' when describing ongoing oscillation.",
            "context": "Essential for IELTS Academic Task 1 line graph descriptions."
        }
    }

    PHRASAL_VERBS = [
        {
            "phrasal_verb": "account for",
            "meaning": "To make up or form a specific proportion; or to explain the cause of something.",
            "example": "Renewable energy sources accounted for 28% of total electricity production in 2022.",
            "formal_alternative": "constitute / comprise / explain",
            "common_mistake": "Avoid forgetting the preposition 'for'; you cannot say 'accounted 28%'.",
            "academic_quiz": "In 2020, solar power _____ (accounted for / made for) 15% of national output."
        },
        {
            "phrasal_verb": "carry out",
            "meaning": "To execute, perform, or conduct a task or research.",
            "example": "The scientists carried out extensive laboratory investigations.",
            "formal_alternative": "conduct / execute / implement",
            "common_mistake": "In IELTS Task 2, 'conduct research' or 'execute a policy' often carries a more formal tone than 'carry out'.",
            "academic_quiz": "The university committee _____ (carried out / carried on) the initial survey."
        },
        {
            "phrasal_verb": "bring about",
            "meaning": "To cause something to happen.",
            "example": "The rapid advancement of artificial intelligence has brought about major societal shifts.",
            "formal_alternative": "precipitate / induce / engender",
            "common_mistake": "Do not confuse with 'bring up' (to raise a child or mention a topic).",
            "academic_quiz": "Urbanization has _____ (brought about / brought up) widespread changes in lifestyle."
        }
    ]

    COLLOCATIONS = [
        {
            "collocation": "make a decision",
            "unnatural": "do a decision",
            "type": "verb + noun",
            "example": "Policymakers must make a timely decision regarding renewable infrastructure.",
            "formal_upgrade": "reach a verdict / arrive at a resolution"
        },
        {
            "collocation": "take responsibility",
            "unnatural": "make responsibility",
            "type": "verb + noun",
            "example": "Corporations should take responsibility for their industrial emissions.",
            "formal_upgrade": "assume accountability"
        },
        {
            "collocation": "strong evidence",
            "unnatural": "hard evidence (less formal) / big evidence",
            "type": "adjective + noun",
            "example": "There is compelling and strong evidence to suggest that regular exercise improves cognitive longevity.",
            "formal_upgrade": "compelling empirical evidence"
        },
        {
            "collocation": "heavy traffic",
            "unnatural": "dense traffic / crowded cars / big traffic",
            "type": "adjective + noun",
            "example": "Commuters in metropolitan capitals frequently endure heavy traffic during peak hours.",
            "formal_upgrade": "severe traffic congestion"
        }
    ]

    IDIOMS = [
        {
            "idiom": "see eye to eye",
            "meaning": "To agree fully with someone.",
            "example": "Although the partners did not see eye to eye on every detail, they completed the project.",
            "register_warning": "Acceptable in IELTS Speaking (Part 1 and 3). Avoid in Academic Writing Task 1 and 2.",
            "writing_alternative": "concur / share common ground"
        },
        {
            "idiom": "a double-edged sword",
            "meaning": "A feature that has both favorable and unfavorable consequences.",
            "example": "Technological ubiquity is a double-edged sword for modern working parents.",
            "register_warning": "Widely accepted in IELTS Speaking and Writing Task 2 when used judiciously.",
            "writing_alternative": "a phenomenon fraught with both advantages and drawbacks"
        }
    ]

    @classmethod
    def get_word(cls, word: str) -> Optional[Dict[str, Any]]:
        return cls.ACADEMIC_VOCAB.get(word.strip().lower())

    @classmethod
    def get_all_words(cls) -> List[Dict[str, Any]]:
        return list(cls.ACADEMIC_VOCAB.values())

    @classmethod
    def get_collocation_exercise(cls) -> Dict[str, Any]:
        item = cls.COLLOCATIONS[0]
        return {
            "prompt": f"Identify the natural collocation: 'Citizens must _____ (make / do / hold) a decision.'",
            "correct": "make",
            "collocation": item["collocation"],
            "explanation": f"In English, the verb 'make' naturally collocates with 'decision', whereas 'do a decision' is an unnatural calque."
        }
