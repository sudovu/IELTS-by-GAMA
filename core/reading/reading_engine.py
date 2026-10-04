"""
Reading Engine for IELTS by GAMA.
Delivers 100% original, copyright-compliant IELTS-style reading passages and exercises.
Analyzes skimming, scanning, distractor traps, and keyword matching.
Includes IELTS Advantage Keyword & Synonym Mapping Tables for Band 8+ reading strategy.
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
            ],
            "synonym_table": [
                {"question_keyword": "solar radiation", "passage_synonym": "sunlight / solar photosynthesis"},
                {"question_keyword": "fundamental nutrients", "passage_synonym": "organic nourishment"},
                {"question_keyword": "absorb nourishment", "passage_synonym": "synthesize organic nourishment for the host"},
                {"question_keyword": "continuously active", "passage_synonym": "ephemeral / shut down within a matter of decades"}
            ]
        },
        "acad_p2": {
            "id": "acad_p2",
            "track": "Academic",
            "title": "The Cognitive Architecture of Bilingualism & Executive Function",
            "text": (
                "For much of the twentieth century, clinical educators cautioned parents against raising children in "
                "bilingual households, asserting that juggling two grammatical systems would cause cognitive confusion "
                "and impede linguistic development. However, modern neuroimaging and psycholinguistic experiments have thoroughly "
                "debunked this deficit hypothesis. Far from hindering intellect, acquiring multiple languages reshapes neural "
                "pathways and fortifies the brain's executive control center.\n\n"
                "Executive function refers to a constellation of higher-order cognitive operations overseen predominantly "
                "by the prefrontal cortex. These include cognitive flexibility, inhibitory control, working memory, and selective "
                "attention. When a bilingual individual communicates, both language systems remain perpetually active in the brain. "
                "Even when conducting a conversation entirely in Spanish, the English lexical network is primed and competes for "
                "activation. To prevent interference, the brain must continuously exert inhibitory control to suppress the "
                "irrelevant language while maintaining attentional focus on the target vernacular.\n\n"
                "This relentless neural workout produces measurable neuroplastic advantages across the lifespan. In laboratory "
                "experiments such as the Simon task and the Stroop color-word test, bilingual participants consistently outperform "
                "monolingual peers in resolving conflicting stimuli and executing rapid task-switching protocols. Crucially, this "
                "advantage is not restricted to linguistic tasks; it manifests robustly across spatial reasoning and abstract problem-solving.\n\n"
                "Perhaps the most profound implication of bilingualism is its neuroprotective capacity against age-related cognitive "
                "decline. Longitudinal epidemiological studies led by cognitive neuroscientists demonstrate that lifelong bilinguals "
                "manifest symptoms of neurodegenerative disorders, such as Alzheimer's disease, an average of four to five years "
                "later than monolingual cohorts with equivalent neuropathological brain damage. This phenomenon is known as "
                "'cognitive reserve'—the brain's enhanced resilience and capability to improvise alternative neural routes around damaged areas."
            ),
            "questions": [
                {
                    "num": 1,
                    "type": "TFNG",
                    "prompt": "Early twentieth-century educators encouraged families to raise multilingual children.",
                    "correct": "False",
                    "evidence": "clinical educators cautioned parents against raising children in bilingual households, asserting that juggling two grammatical systems would cause cognitive confusion",
                    "explanation": "The text confirms early educators warned AGAINST bilingualism, not encouraged it."
                },
                {
                    "num": 2,
                    "type": "TFNG",
                    "prompt": "When a bilingual speaks one language, their other language system is entirely shut down.",
                    "correct": "False",
                    "evidence": "both language systems remain perpetually active in the brain... the English lexical network is primed and competes for activation.",
                    "explanation": "Both languages remain perpetually active and compete for activation."
                },
                {
                    "num": 3,
                    "type": "TFNG",
                    "prompt": "The cognitive benefits of bilingualism are strictly confined to verbal and language-based tests.",
                    "correct": "False",
                    "evidence": "this advantage is not restricted to linguistic tasks; it manifests robustly across spatial reasoning and abstract problem-solving.",
                    "explanation": "The text directly states the benefits extend to spatial reasoning and abstract tasks."
                },
                {
                    "num": 4,
                    "type": "Completion",
                    "max_words": 2,
                    "prompt": "The brain's ability to resist neurodegenerative symptoms by finding alternate neural circuits is termed _____.",
                    "acceptable": ["cognitive reserve"],
                    "evidence": "This phenomenon is known as 'cognitive reserve'—the brain's enhanced resilience and capability to improvise alternative neural routes",
                    "explanation": "The passage terms this resilience 'cognitive reserve'."
                }
            ],
            "synonym_table": [
                {"question_keyword": "encouraged families", "passage_synonym": "cautioned parents against"},
                {"question_keyword": "entirely shut down", "passage_synonym": "perpetually active / competes for activation"},
                {"question_keyword": "strictly confined to verbal", "passage_synonym": "not restricted to linguistic tasks"},
                {"question_keyword": "alternate neural circuits", "passage_synonym": "improvise alternative neural routes"}
            ]
        },
        "acad_p3": {
            "id": "acad_p3",
            "track": "Academic",
            "title": "Urban Heat Islands and Microclimate Architecture",
            "text": (
                "Urban Heat Islands (UHIs) represent a pronounced meteorological phenomenon whereby metropolitan centers "
                "experience surface and ambient air temperatures substantially higher than their surrounding rural peripheries. "
                "This thermal discrepancy, which can reach up to 10 degrees Celsius in densely populated capitals during nighttime hours, "
                "is primarily driven by the extensive replacement of vegetative terrain with impermeable artificial surfaces such "
                "as asphalt, concrete, and masonry. These materials possess high thermal mass and low albedo, enabling them to absorb "
                "copious solar irradiance during daytime hours and reradiate it as sensible heat after dusk.\n\n"
                "Furthermore, urban canyons formed by towering high-rise developments impede natural wind ventilation, trapping "
                "anthropogenic heat generated by industrial machinery, vehicular exhausts, and air-conditioning refrigeration units. "
                "The consequences of unmitigated UHIs are severe, exacerbating heat-related cardiovascular mortality, amplifying "
                "smog photochemistry, and triggering immense spikes in electrical energy consumption for cooling systems.\n\n"
                "To counter these escalating urban microclimates, contemporary municipal architects and urban planners are implementing "
                "multi-layered passive cooling strategies. Central to these interventions is the widespread integration of living architecture, "
                "such as vegetative green roofs and extensive vertical facade gardens. Vegetative surfaces cool the ambient microclimate "
                "through evapotranspiration—a biophysical process where plants transpire moisture while solar energy evaporates water "
                "from soil matrices, thereby dissipating latent heat without raising temperature.\n\n"
                "Concurrently, civil engineers are retrofitting road networks with permeable, high-albedo cool pavements. By reflecting "
                "upwards of 40% of incident solar radiation compared to the standard 10% reflected by aged asphalt, cool pavements prevent "
                "initial thermal absorption. When combined with strategic urban forestry corridors that channel prevailing oceanic breezes, "
                "these sustainable architectural interventions can suppress peak localized temperatures by several critical degrees."
            ),
            "questions": [
                {
                    "num": 1,
                    "type": "TFNG",
                    "prompt": "Rural peripheral regions typically experience higher temperatures than city centers.",
                    "correct": "False",
                    "evidence": "metropolitan centers experience surface and ambient air temperatures substantially higher than their surrounding rural peripheries",
                    "explanation": "City centers are hotter than rural peripheries, so the statement is False."
                },
                {
                    "num": 2,
                    "type": "TFNG",
                    "prompt": "Urban canyon high-rises can hinder atmospheric airflow and trap heat.",
                    "correct": "True",
                    "evidence": "urban canyons formed by towering high-rise developments impede natural wind ventilation, trapping anthropogenic heat",
                    "explanation": "The text confirms high-rise canyons impede ventilation and trap heat."
                },
                {
                    "num": 3,
                    "type": "TFNG",
                    "prompt": "Standard aged asphalt reflects over 40% of incoming solar radiation.",
                    "correct": "False",
                    "evidence": "compared to the standard 10% reflected by aged asphalt",
                    "explanation": "Aged asphalt reflects only about 10%, whereas cool pavements reflect 40%."
                },
                {
                    "num": 4,
                    "type": "Completion",
                    "max_words": 1,
                    "prompt": "Plants lower ambient air temperatures without heating through the process of _____.",
                    "acceptable": ["evapotranspiration"],
                    "evidence": "Vegetative surfaces cool the ambient microclimate through evapotranspiration",
                    "explanation": "The biophysical cooling process specified is evapotranspiration."
                }
            ],
            "synonym_table": [
                {"question_keyword": "higher temperatures than city centers", "passage_synonym": "metropolitan centers substantially higher than rural peripheries"},
                {"question_keyword": "hinder atmospheric airflow", "passage_synonym": "impede natural wind ventilation"},
                {"question_keyword": "incoming solar radiation", "passage_synonym": "incident solar radiation / solar irradiance"},
                {"question_keyword": "cooling process", "passage_synonym": "evapotranspiration / dissipating latent heat"}
            ]
        }
    }

    @classmethod
    def list_passages(cls) -> List[Dict[str, Any]]:
        return [
            {
                "id": p["id"],
                "track": p["track"],
                "title": p["title"],
                "question_count": len(p["questions"])
            }
            for p in cls.ORIGINAL_PASSAGES.values()
        ]

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
            "synonym_table": passage.get("synonym_table", []),
            "reading_strategy_tips": [
                "IELTS Advantage Keyword Strategy: Locate keywords in questions, then scan for paraphrases/synonyms in the text.",
                "True/False/Not Given Decision Matrix: True = same meaning; False = opposite/contradicts; Not Given = no proof either way.",
                "Watch out for qualifying adverbs ('predominantly', 'solely', 'temporarily') which determine the boundary of truth."
            ],
            "disclaimer": BandCalculator.DISCLAIMER,
            "copyright_notice": "Original IELTS-style practice passage architected for GAMA."
        }
