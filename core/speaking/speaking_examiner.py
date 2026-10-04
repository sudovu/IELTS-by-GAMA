"""
AI IELTS Speaking Examiner for IELTS by GAMA.
Orchestrates official 3-part test format:
- Part 1: Introduction and Interview (4–5 mins)
- Part 2: Long Turn / Cue Card (1 min prep, 2 mins talk)
- Part 3: Two-way Abstract Discussion (4–5 mins)
Includes IELTS Advantage 3-Step Speaking Strategy (Direct Answer -> Reason -> Example),
authentic Cambridge question banks, Band 9 model answers, and criterion scoring.
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
                ],
                "band_9_model": (
                    "I'd like to talk about successfully launching an open-source educational platform for underprivileged students. "
                    "I initially conceived this idea during my second year at university when I observed a profound digital divide. "
                    "The primary obstacle was undoubtedly securing reliable server infrastructure with virtually zero financial capital, "
                    "which compelled me to optimize database performance to run on minimal hardware. "
                    "Reaching this milestone was deeply fulfilling because it directly empowered hundreds of young learners to access quality study materials."
                )
            },
            "part_3_discussion": [
                "Do young people today face greater pressure to succeed in their careers than earlier generations?",
                "How can educational institutions better prepare students for practical life challenges?",
                "Why do some individuals lose motivation when pursuing long-term objectives?",
                "Should personal fulfillment be valued more highly than financial prosperity in modern careers?"
            ],
            "advantage_strategy_tip": "IELTS Advantage 3-Step Formula: 1. Answer directly ('Yes, indisputably...'), 2. State the reason ('Because globalization and social media heighten competition...'), 3. Provide a concrete example ('For instance, entry-level jobs now demand multiple internships...')."
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
                ],
                "band_9_model": (
                    "A historical landmark that profoundly resonated with me is the ancient library in my capital's historic quarter, "
                    "constructed in the mid-19th century. Architecturally, it features vaulted limestone ceilings, intricate hand-carved arches, "
                    "and passive ventilation shafts designed well before modern air conditioning. I visited it with my grandfather during my final year "
                    "of high school. Preserving monuments of this caliber is indispensable because they serve as tangible conduits to our ancestral roots "
                    "and prevent historical narratives from being subsumed by modern urban homogeneity."
                )
            },
            "part_3_discussion": [
                "Why is it essential for governments to preserve ancient architecture alongside modern high-rises?",
                "How does sustainable green architecture influence public health in densely populated cities?",
                "Should historical monuments be free for citizens to visit, or should admission fees fund restoration?",
                "In what ways can urban planners prevent historic districts from succumbing to commercialization?"
            ],
            "advantage_strategy_tip": "Use vivid adjectives and precise collocations ('vaulted limestone ceilings', 'passive ventilation', 'tangible conduits') rather than generic words like 'nice' or 'old'."
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
                ],
                "band_9_model": (
                    "I want to speak about an offline-first linguistic analysis engine that I discovered while preparing for postgraduate research. "
                    "A fellow software developer recommended it when I struggled with intermittent connectivity in rural areas. "
                    "I now employ it daily to verify grammatical nuance and structural coherence in academic manuscripts. "
                    "It has transformed my productivity because instead of relying on sluggish cloud APIs, the engine executes neural parsing "
                    "directly on my local device in milliseconds, allowing me to maintain unbroken cognitive focus."
                )
            },
            "part_3_discussion": [
                "Will automated artificial intelligence systems eventually diminish the demand for human analytical skills?",
                "How can governments ensure ethical standards in algorithmic decision-making and data privacy?",
                "What impact has constant digital connectivity had on face-to-face interpersonal relationships?",
                "Are older demographics being unfairly marginalized by the rapid shift toward cashless, app-only services?"
            ],
            "advantage_strategy_tip": "In Part 3, avoid single-perspective answers. Use concession structures: 'While some critics fear job displacement, on the other hand, history demonstrates that technological innovation generates higher-tier specialized professions.'"
        },
        {
            "id": "topic_tourism",
            "title": "International Tourism, Cultural Preservation & Overtourism",
            "part_1": [
                "Good morning. Let's discuss travel and holidays. How often do you travel during vacation periods?",
                "Do you prefer visiting famous tourist destinations or exploring secluded off-the-beaten-track locations?",
                "What factors do you consider when choosing a holiday destination?",
                "Do you think tourism brings more economic advantages or environmental challenges to your region?"
            ],
            "part_2_cue_card": {
                "id": "cue_tourism",
                "topic": "Describe an unforgettable journey or trip you took to an unfamiliar destination.",
                "prompts": [
                    "Where you went and how you traveled there",
                    "Who accompanied you on this journey",
                    "What memorable activities you engaged in",
                    "And explain what valuable insights or lessons you gleaned from the experience."
                ],
                "band_9_model": (
                    "I would like to describe a scenic overland expedition I took across the northern highlands two years ago with two childhood companions. "
                    "We traversed mountainous topography via local sleeper trains and rented electric bicycles. "
                    "What struck me most forcefully was the remarkable ecological stewardship exhibited by indigenous mountain communities, "
                    "who managed community-owned eco-lodges with zero plastic waste. "
                    "This expedition taught me that authentic tourism is not merely about sightseeing, but about fostering mutual cultural respect and sustainable local commerce."
                )
            },
            "part_3_discussion": [
                "Should governments place statutory caps on daily visitor numbers to safeguard delicate historical monuments from overtourism?",
                "How does mass commercial tourism alter the authentic traditions and linguistic identity of host communities?",
                "Do you believe virtual reality simulations could ever substitute physical international travel?",
                "In what ways can travelers minimize their environmental footprint when visiting fragile natural reserves?"
            ],
            "advantage_strategy_tip": "When answering Part 3 questions on tourism, balance the economic benefits (job creation, infrastructure funding) with environmental and sociocultural hazards (gentrification, carbon emissions)."
        },
        {
            "id": "topic_education",
            "title": "Modern Education, University Curricula & Practical Skills",
            "part_1": [
                "Good afternoon. Let's talk about education. What was your favorite subject in secondary school?",
                "Did you have an inspirational teacher who significantly influenced your educational journey?",
                "Do you find learning in an interactive classroom or online self-study more effective?",
                "Are practical vocational skills sufficiently taught in modern secondary schools?"
            ],
            "part_2_cue_card": {
                "id": "cue_education",
                "topic": "Describe a difficult skill or subject you successfully mastered through deliberate practice.",
                "prompts": [
                    "What the skill or subject was",
                    "Why you initially found it formidable or challenging",
                    "What study methods or resources you leveraged to master it",
                    "And explain how mastering this skill enhanced your personal or academic confidence."
                ],
                "band_9_model": (
                    "A subject that initially presented a steep learning curve for me was statistical econometrics. "
                    "I found the mathematical formulas rather abstract until I began applying them to empirical datasets analyzing climate economics. "
                    "I adopted a disciplined study protocol: dedicating 45 minutes every morning to solving regression problems and diagramming hypotheses. "
                    "Overcoming that mental barrier instilled in me the conviction that intellectual mastery is not innate talent, "
                    "but the cumulative dividend of consistent, deliberate application."
                )
            },
            "part_3_discussion": [
                "Should tertiary higher education be funded entirely by taxpayers, or should students contribute tuition fees?",
                "To what extent will artificial intelligence tutors replace traditional classroom educators?",
                "Why are soft skills like emotional intelligence and teamwork becoming more coveted by modern employers than rote academic knowledge?",
                "How can school curricula bridge the growing divide between theoretical academia and industry workplace demands?"
            ],
            "advantage_strategy_tip": "Employ the 'Coffee Shop Method' when generating ideas: don't search for 'genius' thoughts; formulate realistic, straightforward arguments supported by a clean explanation and example."
        },
        {
            "id": "topic_health",
            "title": "Public Health, Fast-Paced Lifestyles & Mental Well-being",
            "part_1": [
                "Hello. Let's discuss daily habits and health. What healthy habits do you try to maintain every day?",
                "How do you manage stress and psychological pressure during intense working or examination periods?",
                "Do you prefer engaging in outdoor team sports or individual physical workouts?",
                "Has public awareness regarding balanced nutrition improved in your home country recently?"
            ],
            "part_2_cue_card": {
                "id": "cue_health",
                "topic": "Describe a positive lifestyle modification you implemented to boost your physical or mental health.",
                "prompts": [
                    "What the modification or new habit was",
                    "What triggered or motivated you to make this change",
                    "How challenging it was to sustain in the initial stages",
                    "And explain the lasting benefits you noticed in your well-being."
                ],
                "band_9_model": (
                    "I would like to highlight my decision to institute a strict digital curfew one hour before bed, combined with a daily 30-minute morning jog. "
                    "The catalyst was chronic daytime fatigue caused by late-night screen illumination disrupting my circadian rhythm. "
                    "Initially, detaching from social notifications proved arduous, but within three weeks, my sleep architecture improved dramatically. "
                    "The sustained outcome has been higher cognitive clarity throughout my workdays and a marked reduction in baseline anxiety."
                )
            },
            "part_3_discussion": [
                "Should municipal authorities penalize junk food manufacturers by levying sugar and saturated fat taxes?",
                "Why are modern sedentary white-collar professions experiencing an epidemic of postural and cardiovascular ailments?",
                "Is individual personal discipline or state regulation more effective in curbing national obesity rates?",
                "How can corporations structure working hours to prevent employee burnout and mental exhaustion?"
            ],
            "advantage_strategy_tip": "IELTS Advantage 3-Step Formula: 1. Direct answer -> 2. The 'Why' (scientific/social mechanism) -> 3. Practical illustration. This ensures Band 7+ Fluency & Coherence without awkward pauses."
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
            "advantage_strategy_tip": set_data.get("advantage_strategy_tip", ""),
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
            "IELTS Advantage 3-Step Formula: 1. Answer Directly -> 2. Give the Reason -> 3. Add an authentic real-world Example.",
            "Avoid short, monosyllabic answers in Part 1; elaborate with 2-3 coherent sentences.",
            "In Part 3, explore multiple viewpoints with concession phrases ('While some argue X, on balance I believe Y')."
        ]
        return criteria_result
