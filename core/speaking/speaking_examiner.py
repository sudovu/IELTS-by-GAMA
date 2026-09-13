"""
AI IELTS Speaking Examiner for IELTS by GAMA.
Orchestrates official 3-part test format:
- Part 1: Introduction and Interview (4–5 mins)
- Part 2: Long Turn / Cue Card (1 min prep, 2 mins talk)
- Part 3: Two-way Abstract Discussion (4–5 mins)
Evaluates FC, LR, GRA, and Pronunciation criteria with formative feedback.
"""

from typing import Dict, Any, List, Optional
from .fluency_tracker import FluencyTracker
from ..scoring.criteria_evaluator import CriteriaEvaluator
from ..grammar.grammar_engine import GrammarEngine


class SpeakingExaminer:
    """Simulates an interactive IELTS speaking examiner with authentic Cambridge question banks."""

    EXAM_SETS = [
        {
            "id": "topic_ambition",
            "title": "Career, Goals & Ambition",
            "part_1": [
                "Good morning. My name is Dr. Harrison. Can you state your full name, please?",
                "Could you tell me where you come from and what you enjoy most about your hometown?",
                "Do you currently work, or are you a student? What are your daily responsibilities?",
                "How do you usually unwind and spend your free time after a busy day?"
            ],
            "part_2_cue_card": {
                "id": "cue_ambition",
                "topic": "Describe a significant achievement or ambitious goal you reached.",
                "prompts": [
                    "What the achievement or goal was",
                    "When you first decided to pursue it",
                    "What obstacles or challenges you faced along the way",
                    "And explain why reaching this goal was personally meaningful to you."
                ]
            },
            "part_3_discussion": [
                "Do young people today face greater pressure to succeed in their careers than earlier generations?",
                "How can educational institutions better prepare students for practical life challenges?",
                "Why do some individuals lose motivation when pursuing long-term objectives?",
                "Should personal fulfillment be valued more highly than financial prosperity in modern careers?"
            ]
        },
        {
            "id": "topic_environment",
            "title": "Sustainable Living & Urban Heritage",
            "part_1": [
                "Hello. Welcome to the IELTS Speaking test. May I see your identification, please?",
                "Let's talk about where you live. Is your neighborhood noisy or quiet?",
                "Do you prefer living in a bustling metropolitan area or a peaceful countryside setting?",
                "How have cities in your country changed over the past ten years?"
            ],
            "part_2_cue_card": {
                "id": "cue_heritage",
                "topic": "Describe a historical building or architectural landmark that left a strong impression on you.",
                "prompts": [
                    "Where this building or landmark is located",
                    "What architectural features or history it possesses",
                    "When and with whom you visited it",
                    "And explain why you think preserving such heritage is important for future generations."
                ]
            },
            "part_3_discussion": [
                "Why is it essential for governments to preserve ancient architecture alongside modern high-rises?",
                "How does sustainable green architecture influence public health in densely populated cities?",
                "Should historical monuments be free for citizens to visit, or should admission fees fund restoration?",
                "In what ways can urban planners prevent historic districts from succumbing to commercialization?"
            ]
        },
        {
            "id": "topic_technology",
            "title": "Artificial Intelligence, Automation & Media",
            "part_1": [
                "Good afternoon. I am your examiner today. Could you please confirm your full name?",
                "How reliant are you on digital devices for your everyday communication?",
                "Do you prefer reading news from printed newspapers or digital applications?",
                "What kind of modern technology do you find most indispensable in your daily life?"
            ],
            "part_2_cue_card": {
                "id": "cue_technology",
                "topic": "Describe a technological innovation or digital tool that dramatically changed how you work or study.",
                "prompts": [
                    "What the innovation or software application is",
                    "How you first became aware of it",
                    "How frequently you incorporate it into your routine",
                    "And explain how it has augmented your productivity and learning efficiency."
                ]
            },
            "part_3_discussion": [
                "Will automated artificial intelligence systems eventually diminish the demand for human analytical skills?",
                "How can governments ensure ethical standards in algorithmic decision-making and data privacy?",
                "What impact has constant digital connectivity had on face-to-face interpersonal relationships?",
                "Are older demographics being unfairly marginalized by the rapid shift toward cashless, app-only services?"
            ]
        }
    ]

    LEXICAL_UPGRADE_MAP = [
        ("i think", "from my perspective / I am inclined to argue that"),
        ("in my opinion", "as far as I can ascertain / it is evident that"),
        ("a lot of", "an abundance of / a substantial proportion of"),
        ("very important", "of paramount importance / pivotal / indispensable"),
        ("good", "exemplary / commendable / profoundly beneficial"),
        ("bad", "detrimental / counterproductive / adverse"),
        ("big problem", "formidable dilemma / pressing challenge"),
        ("help", "facilitate / bolster / catalyze"),
        ("hard", "arduous / demanding / multifaceted"),
        ("happy", "immensely gratified / exhilarating"),
        ("like", "have a strong affinity for / gravitate towards"),
        ("many people", "a considerable cohort of individuals / citizens worldwide"),
        ("make better", "ameliorate / enhance / foster"),
        ("shows that", "serves as compelling evidence that / substantiates that")
    ]

    @classmethod
    def get_exam_sets(cls) -> List[Dict[str, Any]]:
        return [
            {
                "id": s["id"],
                "title": s["title"],
                "cue_topic": s["part_2_cue_card"]["topic"]
            }
            for s in cls.EXAM_SETS
        ]

    @classmethod
    def get_test_prompts(cls, card_idx: int = 0) -> Dict[str, Any]:
        set_data = cls.EXAM_SETS[card_idx % len(cls.EXAM_SETS)]
        return {
            "id": set_data["id"],
            "title": set_data["title"],
            "part_1": set_data["part_1"],
            "part_2_cue_card": set_data["part_2_cue_card"],
            "part_3_discussion": set_data["part_3_discussion"],
            "disclaimer": "AI IELTS Speaking Simulation. Practice estimate only."
        }

    @classmethod
    def generate_band_upgrades(cls, transcript: str) -> List[Dict[str, str]]:
        """Scans student transcript and suggests Band 8/9 academic lexical upgrades."""
        lower_text = transcript.lower()
        upgrades = []
        for colloquial, advanced in cls.LEXICAL_UPGRADE_MAP:
            if colloquial in lower_text:
                upgrades.append({
                    "original": colloquial,
                    "band_9_upgrade": advanced,
                    "tip": f"Replace everyday expression '{colloquial}' with higher-tier academic phrasing."
                })
                if len(upgrades) >= 4:
                    break
        if not upgrades:
            upgrades.append({
                "original": "conversational flow",
                "band_9_upgrade": "Integrate discourse markers: 'Notwithstanding that fact', 'In the broader scheme of things', 'To put this into perspective'",
                "tip": "Adding cohesive lexical markers elevates Fluency and Coherence from Band 6.5 to Band 8.0."
            })
        return upgrades

    @classmethod
    def evaluate_spoken_response(
        cls,
        transcript: str,
        duration_seconds: float = 90.0,
        pronunciation_rating: float = 6.5
    ) -> Dict[str, Any]:
        """Evaluates a learner's spoken turn across all four official criteria with formative optimization."""
        fluency_data = FluencyTracker.analyze_fluency(transcript, duration_seconds)
        fc_score = fluency_data["estimated_fc_band"]

        # Lexical Resource check
        words = transcript.lower().split()
        unique_ratio = len(set(words)) / max(1, len(words))
        lr_score = 6.0
        if unique_ratio > 0.6:
            lr_score += 0.5
        if any(w in transcript.lower() for w in ["significant", "perseverance", "milestone", "challenging", "consequently", "paramount", "perspective", "substantial"]):
            lr_score += 0.5
        lr_score = min(8.5, max(4.0, lr_score))

        # Grammatical Range and Accuracy check
        diagnosed_errors = GrammarEngine.check_sentence(transcript)
        gra_score = 6.5
        if len(diagnosed_errors) == 0 and len(words) > 50:
            gra_score += 0.5
        elif len(diagnosed_errors) >= 2:
            gra_score -= 1.0
        gra_score = min(8.5, max(4.0, gra_score))

        p_score = pronunciation_rating

        criteria_result = CriteriaEvaluator.evaluate_speaking(
            fc_score=fc_score,
            lr_score=lr_score,
            gra_score=gra_score,
            p_score=p_score,
            fluency_metrics=fluency_data
        )

        criteria_result["corrections"] = diagnosed_errors
        criteria_result["band_upgrades"] = cls.generate_band_upgrades(transcript)
        criteria_result["actionable_tips"] = [
            "Use cohesive conversational signposts ('To be entirely honest', 'Looking back at that period', 'In the broader scheme of things').",
            "Keep speech continuous by elaborating on causes and personal reflections."
        ]
        return criteria_result
