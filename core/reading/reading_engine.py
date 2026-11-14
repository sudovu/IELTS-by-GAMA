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
        },
        # -------------------------------------------------------------
        # IELTS GENERAL TRAINING READING PASSAGES
        # -------------------------------------------------------------
        "gt_s1": {
            "id": "gt_s1",
            "track": "General Training",
            "section": 1,
            "title": "Community College Adult Education & Facility Guidelines",
            "text": (
                "Welcome to the Southwark Community College Continuing Education Programme. We provide a diverse range of "
                "evening and weekend courses designed for career advancement and personal enrichment.\n\n"
                "Registration and Tuition Fees:\n"
                "Enrollment opens four weeks prior to the start of each academic term. To guarantee placement, fees must be "
                "settled in full at least seven working days before the inaugural class. A non-refundable administration levy "
                "of £25 applies to all new applicants. Concessionary discounts of 20% are available to senior citizens aged 65 "
                "and over, full-time undergraduate students, and registered jobseekers upon presentation of verifiable documentation.\n\n"
                "Class Cancellations and Refunds:\n"
                "Courses with fewer than eight confirmed participants will regrettably be suspended. In such instances, enrolled "
                "candidates will receive an immediate full refund or may transfer credit to an alternate course without penalty. "
                "Individual withdrawals requested more than ten days before course commencement will receive an 80% tuition refund. "
                "No refunds will be granted for cancellations submitted within seven days of the course starting date.\n\n"
                "Campus Facilities & Parking Permits:\n"
                "Evening learners enjoy complimentary access to the college library and computer laboratories until 9:30 PM on "
                "weekdays. On-campus vehicular parking is strictly regulated. Learners may obtain a subsidized evening parking "
                "permit from the Security Pavilion for £15 per term. Parking without a valid displayed permit will result in an "
                "immediate fixed penalty charge of £40."
            ),
            "questions": [
                {
                    "num": 1,
                    "type": "TFNG",
                    "prompt": "Tuition fees may be paid on the day the course begins.",
                    "correct": "False",
                    "evidence": "fees must be settled in full at least seven working days before the inaugural class",
                    "explanation": "The text states fees must be paid at least seven working days prior to the first class."
                },
                {
                    "num": 2,
                    "type": "TFNG",
                    "prompt": "Jobseekers are entitled to a 20 percent concession on tuition fees.",
                    "correct": "True",
                    "evidence": "Concessionary discounts of 20% are available to... registered jobseekers upon presentation of verifiable documentation.",
                    "explanation": "Jobseekers receive a 20% discount if they provide documentation."
                },
                {
                    "num": 3,
                    "type": "TFNG",
                    "prompt": "The college library remains open on Saturday evenings.",
                    "correct": "Not Given",
                    "evidence": "Evening learners enjoy complimentary access to the college library... until 9:30 PM on weekdays.",
                    "explanation": "Weekday opening hours are given, but Saturday evening library hours are not specified."
                },
                {
                    "num": 4,
                    "type": "Completion",
                    "max_words": 1,
                    "prompt": "Courses will be cancelled if they fail to attract at least _____ students.",
                    "acceptable": ["eight", "8"],
                    "evidence": "Courses with fewer than eight confirmed participants will regrettably be suspended.",
                    "explanation": "The minimum enrollment threshold is eight participants."
                },
                {
                    "num": 5,
                    "type": "Completion",
                    "max_words": 2,
                    "prompt": "Evening parking permits must be acquired from the _____.",
                    "acceptable": ["Security Pavilion", "security pavilion"],
                    "evidence": "Learners may obtain a subsidized evening parking permit from the Security Pavilion",
                    "explanation": "The Security Pavilion issues parking permits."
                }
            ],
            "synonym_table": [
                {"question_keyword": "concession on tuition", "passage_synonym": "Concessionary discounts of 20%"},
                {"question_keyword": "cancelled", "passage_synonym": "regrettably be suspended"},
                {"question_keyword": "acquired from", "passage_synonym": "obtain... from"}
            ]
        },
        "gt_s2": {
            "id": "gt_s2",
            "track": "General Training",
            "section": 2,
            "title": "Corporate Ergonomics & Hybrid Telecommuting Policy",
            "text": (
                "Apex Global Enterprises is dedicated to promoting occupational health and workplace well-being across our "
                "hybrid workforce. This protocol outlines workstation ergonomic standards and remote telecommuting compliance.\n\n"
                "Workstation Setup Standards:\n"
                "Employees are required to maintain an ergonomically sound physical setup whether working in the corporate "
                "headquarters or within a designated domestic workspace. Display monitors should be positioned directly at eye level "
                "at approximately an arm's length (50 to 70 centimeters) from the user, ensuring the upper third of the screen "
                "aligns with natural horizontal gaze. Chairs must offer adjustable lumbar support, with seat height configured so "
                "that thighs remain parallel to the floor and feet rest firmly upon a solid surface or footrest.\n\n"
                "Micro-Breaks and Movement:\n"
                "Sustained static postures represent a leading contributor to musculoskeletal discomfort. Staff members must adhere "
                "to the '20-20-20 rule': every 20 minutes, gaze at an object situated at least 20 feet away for a duration of 20 seconds "
                "to alleviate ocular strain. In addition, employees are strongly urged to stand and stretch for at least two minutes "
                "every hour during prolonged computer usage.\n\n"
                "IT Security & Equipment Allocation:\n"
                "Apex provides each eligible telecommuting employee with a standardized laptop, an external monitor, an ergonomic "
                "keyboard, and a peripheral mouse. Domestic computer equipment is strictly prohibited from connecting to the internal "
                "corporate virtual private network (VPN). Any accidental data breach or unauthorized device connection must be "
                "notified to the IT Security Helpdesk within two hours of discovery."
            ),
            "questions": [
                {
                    "num": 1,
                    "type": "MCQ",
                    "prompt": "According to the protocol, how far should the computer display be placed from the employee?",
                    "correct": "B",
                    "evidence": "approximately an arm's length (50 to 70 centimeters) from the user",
                    "explanation": "The text explicitly specifies an arm's length, or 50 to 70 cm.",
                    "distractor_analysis": {
                        "A": "Incorrect; 20 cm is far too close.",
                        "C": "Incorrect; 100 cm exceeds the 50-70 cm limit."
                    }
                },
                {
                    "num": 2,
                    "type": "TFNG",
                    "prompt": "Staff members are permitted to connect personal home desktop computers to the corporate VPN.",
                    "correct": "False",
                    "evidence": "Domestic computer equipment is strictly prohibited from connecting to the internal corporate virtual private network (VPN).",
                    "explanation": "The passage states domestic computers are strictly prohibited from connecting to the corporate VPN."
                },
                {
                    "num": 3,
                    "type": "Completion",
                    "max_words": 2,
                    "prompt": "The 20-20-20 rule is intended to alleviate _____ among computer users.",
                    "acceptable": ["ocular strain", "eye strain"],
                    "evidence": "gaze at an object situated at least 20 feet away for a duration of 20 seconds to alleviate ocular strain.",
                    "explanation": "The text states the rule is to alleviate ocular strain."
                },
                {
                    "num": 4,
                    "type": "Completion",
                    "max_words": 2,
                    "prompt": "Security incidents must be reported to the IT Security Helpdesk within _____.",
                    "acceptable": ["two hours", "2 hours"],
                    "evidence": "notified to the IT Security Helpdesk within two hours of discovery.",
                    "explanation": "The notification deadline is two hours."
                }
            ],
            "synonym_table": [
                {"question_keyword": "personal home computers", "passage_synonym": "Domestic computer equipment"},
                {"question_keyword": "reported", "passage_synonym": "notified"},
                {"question_keyword": "prevent", "passage_synonym": "alleviate / minimize"}
            ]
        },
        "gt_s3": {
            "id": "gt_s3",
            "track": "General Training",
            "section": 3,
            "title": "The Evolution & Civil Engineering of the Suspension Bridge",
            "text": (
                "The suspension bridge is arguably humanity's most elegant architectural triumph over geographical obstacles, "
                "spanning vast waterways with soaring aesthetic lightness. While rudimentary rope and vine suspension bridges "
                "have spanned Himalayan ravines for over two millennia, the genesis of modern structural suspension engineering "
                "occurred in the early nineteenth century with the advent of wrought iron chain cables, pioneered by American "
                "engineer James Finley and refined by British industrial titan Thomas Telford at the Menai Strait.\n\n"
                "The mechanical principle underpinning a suspension bridge is deceptively simple: tensile forces. Heavy vertical "
                "deck loads—comprising vehicular traffic, rail carriages, and dead weight—are transferred through vertical hanger ropes "
                "upwards to massive main suspension cables. These main cables drape parabolically over colossal support towers before "
                "being firmly secured into subterranean concrete anchorages at either terminal bank. In essence, the roadway is "
                "literally hung from the sky, with the towers experiencing pure vertical compression while the cables endure colossal tension.\n\n"
                "However, suspension bridges are acutely vulnerable to dynamic aerodynamic resonance. This catastrophic flaw was "
                "dramatically illustrated in November 1940 by the collapse of the Tacoma Narrows Bridge in Washington State. Designed "
                "with an aesthetically slender, solid-plate girder deck, the bridge acted like an airplane wing in moderate 42-mph winds. "
                "Vortices shed along the girders matched the natural frequency of the bridge, exciting torsional flutter that tore "
                "the roadway apart within hours of onset.\n\n"
                "Following the Tacoma disaster, aerodynamic engineering fundamentally transformed bridge design. Contemporary civil "
                "engineers utilize open aerodynamic steel trusses or streamlined hollow aerofoil box girders, thoroughly verified "
                "through boundary-layer wind tunnel simulation. Structures such as the Akashi Kaikyo Bridge in Japan and the Canakkale "
                "Bridge in Turkey now span distances exceeding two kilometers with total aeroelastic stability."
            ),
            "questions": [
                {
                    "num": 1,
                    "type": "TFNG",
                    "prompt": "Primitive suspension bridges were built in Asia long before the nineteenth century.",
                    "correct": "True",
                    "evidence": "While rudimentary rope and vine suspension bridges have spanned Himalayan ravines for over two millennia",
                    "explanation": "The text confirms rope bridges spanned Himalayan ravines for over 2,000 years."
                },
                {
                    "num": 2,
                    "type": "TFNG",
                    "prompt": "Main suspension cables experience compressive forces rather than tensile forces.",
                    "correct": "False",
                    "evidence": "towers experiencing pure vertical compression while the cables endure colossal tension.",
                    "explanation": "Cables endure tension, while towers experience compression."
                },
                {
                    "num": 3,
                    "type": "MCQ",
                    "prompt": "What caused the structural failure of the Tacoma Narrows Bridge?",
                    "correct": "C",
                    "evidence": "Vortices shed along the girders matched the natural frequency of the bridge, exciting torsional flutter",
                    "explanation": "Aerodynamic resonance and torsional flutter induced by wind vortices destroyed the bridge.",
                    "distractor_analysis": {
                        "A": "Overloaded traffic weight was not the cause.",
                        "B": "Subterranean anchorage fracture was not mentioned."
                    }
                },
                {
                    "num": 4,
                    "type": "Completion",
                    "max_words": 2,
                    "prompt": "Modern bridge deck stability is verified using boundary-layer _____ simulation.",
                    "acceptable": ["wind tunnel"],
                    "evidence": "thoroughly verified through boundary-layer wind tunnel simulation.",
                    "explanation": "Wind tunnel simulation verifies aeroelastic stability."
                }
            ],
            "synonym_table": [
                {"question_keyword": "primitive", "passage_synonym": "rudimentary"},
                {"question_keyword": "compressive forces", "passage_synonym": "pure vertical compression"},
                {"question_keyword": "failure", "passage_synonym": "collapse / tore the roadway apart"}
            ]
        }
    }

    @classmethod
    def list_passages(cls, track: Optional[str] = None) -> List[Dict[str, Any]]:
        passages = list(cls.ORIGINAL_PASSAGES.values())
        if track:
            passages = [p for p in passages if p["track"].lower() == track.lower()]
        return [
            {
                "id": p["id"],
                "track": p["track"],
                "section": p.get("section", 1),
                "title": p["title"],
                "question_count": len(p["questions"])
            }
            for p in passages
        ]

    @classmethod
    def get_passage(cls, passage_id: str = "acad_p1", show_answers: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieves passage text and questions.
        If show_answers is False (exam mode), answer keys, evidence, and explanations are sanitized.
        """
        p = cls.ORIGINAL_PASSAGES.get(passage_id)
        if not p:
            return None

        clean = {
            "id": p["id"],
            "track": p["track"],
            "section": p.get("section", 1),
            "title": p["title"],
            "text": p["text"],
            "questions": []
        }

        for q in p["questions"]:
            q_copy = {
                "num": q["num"],
                "type": q["type"],
                "prompt": q["prompt"],
                "max_words": q.get("max_words")
            }
            if show_answers:
                q_copy["correct"] = q.get("correct")
                q_copy["acceptable"] = q.get("acceptable")
                q_copy["evidence"] = q.get("evidence")
                q_copy["explanation"] = q.get("explanation")
                q_copy["distractor_analysis"] = q.get("distractor_analysis")
            clean["questions"].append(q_copy)

        if show_answers and "synonym_table" in p:
            clean["synonym_table"] = p["synonym_table"]

        return clean

    @classmethod
    def generate_full_mock(cls, track: str = "Academic") -> Dict[str, Any]:
        """
        Generates a comprehensive multi-passage mock examination for Academic or General Training.
        Sanitizes answer keys for active exam mode.
        """
        is_academic = track.lower().startswith("acad")
        passages = []
        target_keys = ["acad_p1", "acad_p2", "acad_p3"] if is_academic else ["gt_s1", "gt_s2", "gt_s3"]

        total_questions = 0
        for k in target_keys:
            p = cls.get_passage(k, show_answers=False)
            if p:
                passages.append(p)
                total_questions += len(p["questions"])

        return {
            "mock_id": f"mock_reading_{track.lower()[:4]}",
            "track": "Academic" if is_academic else "General Training",
            "time_limit_minutes": 60,
            "passages": passages,
            "total_questions": total_questions,
            "instructions": "Read the passages carefully and answer all questions within the 60-minute time allocation."
        }

    @classmethod
    def evaluate_test(cls, passage_id: str, user_answers: Dict[Any, str]) -> Dict[str, Any]:
        """
        Grades reading test submissions using ReadingQuestionTypes dispatcher.
        Explains WHY correct is correct and WHY errors are incorrect.
        """
        passage = cls.ORIGINAL_PASSAGES.get(passage_id)
        if not passage:
            raise ValueError(f"Passage {passage_id} not found")

        total = len(passage["questions"])
        correct_count = 0
        detailed_eval = []

        for q in passage["questions"]:
            qnum = q["num"]
            # Look up answer by integer or string key
            ans = user_answers.get(qnum) or user_answers.get(str(qnum)) or ""
            res = ReadingQuestionTypes.grade_question(q, str(ans))
            res["question_num"] = qnum
            res["prompt"] = q["prompt"]
            if res["is_correct"]:
                correct_count += 1
            detailed_eval.append(res)

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
