"""
Exam Content Repository for IELTS by GAMA.
Provides comprehensive, copyright-compliant practice examination sets:
1. Academic Full Mock (Listening 40 Qs, Reading 40 Qs, Writing Task 1 + Task 2, Speaking Parts 1-3)
2. General Training Full Mock (Listening 40 Qs, Reading 40 Qs, Writing Task 1 + Task 2, Speaking Parts 1-3)
3. Individual Skill Examinations (Reading 40 Qs, Listening 40 Qs, Writing paired tasks, Speaking complete sets)

Includes strict answer-key concealment methods for active examination security.
"""

import copy
from typing import Dict, Any, List, Optional
from ..reading.reading_engine import ReadingEngine
from ..listening.listening_engine import ListeningEngine
from ..writing.writing_evaluator import WritingEvaluator
from ..speaking.speaking_examiner import SpeakingExaminer


class ExamContentRepository:
    """Manages full 4-skill and skill-specific practice examination packages."""

    # -------------------------------------------------------------------------
    # 1. ACADEMIC READING FULL MOCK (40 QUESTIONS ACROSS 3 PASSAGES)
    # -------------------------------------------------------------------------
    ACADEMIC_READING_MOCK_1 = {
        "id": "exam_read_acad_1",
        "title": "IELTS Academic Reading Practice Examination 1",
        "track": "Academic",
        "time_limit_minutes": 60,
        "total_questions": 40,
        "instructions": (
            "You have 60 minutes to complete all 3 passages and 40 questions. "
            "Manage your time carefully (approx. 20 minutes per passage). "
            "Write your answers in the answer boxes provided."
        ),
        "passages": [
            {
                "passage_number": 1,
                "id": "acad_p1",
                "title": "The Architecture of Deep-Sea Hydrothermal Ecosystems",
                "text": (
                    "Paragraph A: Deep-sea hydrothermal vents, discovered in 1977 along the Galapagos Rift, represent one of the "
                    "most remarkable biological frontiers on Earth. Located thousands of meters beneath the oceanic surface where "
                    "sunlight cannot penetrate, these geological formations dispel the historical assumption that all complex "
                    "ecosystems rely fundamentally on solar photosynthesis. Instead, these abyssal biomes are sustained through "
                    "chemosynthesis, a process mediated by specialized extremophilic bacteria.\n\n"
                    "Paragraph B: As tectonic plates diverge, seawater infiltrates subterranean fissures, reaching temperatures exceeding "
                    "400 degrees Celsius near magma chambers. Saturated with dissolved minerals—predominantly hydrogen sulfide, iron, "
                    "and copper—the superheated water precipitates violently upon encountering the frigid, near-freezing ambient ocean. "
                    "This reaction constructs towering mineralized chimneys colloquially known as 'black smokers'.\n\n"
                    "Paragraph C: The organisms flourishing around these vents exhibit astounding biological adaptations. Giant tube worms "
                    "(Riftia pachyptila), which can reach lengths of over two meters, completely lack a digestive tract, mouth, or gut. "
                    "Instead, they harbor billions of symbiotic sulfur-oxidizing bacteria within an organ called the trophosome. "
                    "The tube worms extract hydrogen sulfide and oxygen from the hydrothermal fluid using vascularized red plumes, "
                    "transferring these compounds to the endosymbionts, which synthesize organic nourishment for the host.\n\n"
                    "Paragraph D: Nevertheless, these thriving oasis communities are exceptionally ephemeral. Because tectonic shifts "
                    "and volcanic eruptions routinely seal hydrothermal conduits or open new subterranean fractures, vents can abruptly "
                    "shut down within a matter of decades. Consequently, hydrothermal vent fauna have developed rapid larval dispersion "
                    "mechanisms capable of traversing vast expanses of inhospitable abyssal desert to locate newly forming vents."
                ),
                "questions": [
                    {
                        "num": 1,
                        "type": "TFNG",
                        "prompt": "Deep-sea hydrothermal ecosystems require solar radiation to produce fundamental nutrients.",
                        "correct": "False",
                        "evidence": "dispel the historical assumption that all complex ecosystems rely fundamentally on solar photosynthesis. Instead, these abyssal biomes are sustained through chemosynthesis",
                        "explanation": "Paragraph A states hydrothermal vents rely on chemosynthesis rather than solar photosynthesis, directly contradicting the prompt."
                    },
                    {
                        "num": 2,
                        "type": "TFNG",
                        "prompt": "Precipitation of dissolved minerals occurs when superheated hydrothermal fluids mix with frigid oceanic water.",
                        "correct": "True",
                        "evidence": "the superheated water precipitates violently upon encountering the frigid, near-freezing ambient ocean",
                        "explanation": "Paragraph B explicitly confirms mineral precipitation happens upon encountering frigid seawater."
                    },
                    {
                        "num": 3,
                        "type": "TFNG",
                        "prompt": "Giant tube worms ingest organic prey through a microscopic mouth opening.",
                        "correct": "False",
                        "evidence": "completely lack a digestive tract, mouth, or gut",
                        "explanation": "Paragraph C clearly states that Riftia pachyptila completely lack a mouth and gut."
                    },
                    {
                        "num": 4,
                        "type": "TFNG",
                        "prompt": "Hydrothermal vents remain active and stable for several consecutive centuries.",
                        "correct": "False",
                        "evidence": "exceptionally ephemeral... vents can abruptly shut down within a matter of decades",
                        "explanation": "Paragraph D states vents are ephemeral and shut down within decades, not centuries."
                    },
                    {
                        "num": 5,
                        "type": "TFNG",
                        "prompt": "The discovery of hydrothermal vents occurred before the mid-twentieth century.",
                        "correct": "False",
                        "evidence": "discovered in 1977 along the Galapagos Rift",
                        "explanation": "1977 is in the late twentieth century, not before the mid-twentieth century."
                    },
                    {
                        "num": 6,
                        "type": "TFNG",
                        "prompt": "Human deep-sea submersibles are frequently damaged by magma near black smokers.",
                        "correct": "Not Given",
                        "evidence": "No mention of human deep-sea submersibles being damaged.",
                        "explanation": "The text discusses temperatures and geological forces but says nothing about human submersibles being damaged."
                    },
                    {
                        "num": 7,
                        "type": "TFNG",
                        "prompt": "Larvae of hydrothermal vent fauna can navigate between distant vent chimneys.",
                        "correct": "True",
                        "evidence": "developed rapid larval dispersion mechanisms capable of traversing vast expanses of inhospitable abyssal desert",
                        "explanation": "Paragraph D confirms vent fauna larvae can traverse vast expanses between vents."
                    },
                    {
                        "num": 8,
                        "type": "Completion",
                        "prompt": "Superheated hydrothermal fluid reaches temperatures in excess of _____ degrees Celsius.",
                        "correct": "400",
                        "acceptable": ["400", "400 degrees", "400°C"],
                        "max_words": 2,
                        "evidence": "temperatures exceeding 400 degrees Celsius",
                        "explanation": "Paragraph B identifies the temperature as exceeding 400 degrees Celsius."
                    },
                    {
                        "num": 9,
                        "type": "Completion",
                        "prompt": "Towering chimneys composed of precipitated minerals are colloquially designated as _____.",
                        "correct": "black smokers",
                        "acceptable": ["black smokers", "black smoker chimneys"],
                        "max_words": 2,
                        "evidence": "towering mineralized chimneys colloquially known as 'black smokers'",
                        "explanation": "Paragraph B states they are known colloquially as 'black smokers'."
                    },
                    {
                        "num": 10,
                        "type": "Completion",
                        "prompt": "Giant tube worms extract vital compounds using their vascularized red _____.",
                        "correct": "plumes",
                        "acceptable": ["plumes", "red plumes"],
                        "max_words": 2,
                        "evidence": "using vascularized red plumes",
                        "explanation": "Paragraph C notes that vascularized red plumes extract hydrogen sulfide and oxygen."
                    },
                    {
                        "num": 11,
                        "type": "Completion",
                        "prompt": "Sulfur-oxidizing symbiotic bacteria inhabit an internal organ called the _____.",
                        "correct": "trophosome",
                        "acceptable": ["trophosome"],
                        "max_words": 1,
                        "evidence": "within an organ called the trophosome",
                        "explanation": "Paragraph C specifies the organ name is the trophosome."
                    },
                    {
                        "num": 12,
                        "type": "Completion",
                        "prompt": "Chemical synthesis of nutrients in deep-sea vents is driven by extremophilic _____.",
                        "correct": "bacteria",
                        "acceptable": ["bacteria", "extremophilic bacteria"],
                        "max_words": 2,
                        "evidence": "mediated by specialized extremophilic bacteria",
                        "explanation": "Paragraph A states chemosynthesis is mediated by specialized bacteria."
                    },
                    {
                        "num": 13,
                        "type": "MCQ",
                        "prompt": "What is the primary evolutionary challenge facing vent fauna when active vents seal?",
                        "options": [
                            "Developing tolerance to higher sunlight exposure",
                            "Rapid larval dispersion across inhospitable abyssal waters",
                            "Transitioning from chemosynthesis back to normal digestion",
                            "Surviving prolonged immersion in boiling fresh water"
                        ],
                        "correct": "Rapid larval dispersion across inhospitable abyssal waters",
                        "correct_index": 1,
                        "evidence": "fauna have developed rapid larval dispersion mechanisms capable of traversing vast expanses of inhospitable abyssal desert",
                        "explanation": "Paragraph D highlights rapid larval dispersion as the adaptation against abrupt vent shutdowns."
                    }
                ]
            },
            {
                "passage_number": 2,
                "id": "acad_p2",
                "title": "The Cognitive Architecture of Bilingualism & Executive Function",
                "text": (
                    "Paragraph A: For much of the twentieth century, clinical educators cautioned parents against raising children in "
                    "bilingual households, asserting that juggling two grammatical systems would cause cognitive confusion and impede "
                    "linguistic development. However, modern neuroimaging and psycholinguistic experiments have thoroughly debunked "
                    "this deficit hypothesis. Far from hindering intellect, acquiring multiple languages reshapes neural pathways "
                    "and fortifies the brain's executive control center.\n\n"
                    "Paragraph B: Executive function refers to a constellation of higher-order cognitive operations overseen predominantly "
                    "by the prefrontal cortex. These include cognitive flexibility, inhibitory control, working memory, and selective "
                    "attention. When a bilingual individual communicates, both language systems remain perpetually active in the brain. "
                    "Even when conducting a conversation entirely in Spanish, the English lexical network is primed and competes for "
                    "activation. To prevent interference, the brain must continuously exert inhibitory control to suppress the "
                    "irrelevant language while maintaining attentional focus on the target vernacular.\n\n"
                    "Paragraph C: This relentless neural workout produces measurable neuroplastic advantages across the lifespan. "
                    "In laboratory experiments such as the Simon task and the Stroop color-word test, bilingual participants consistently "
                    "outperform monolingual peers in resolving conflicting stimuli and executing rapid task-switching protocols. "
                    "Crucially, this advantage is not restricted to linguistic tasks; it manifests robustly across spatial reasoning "
                    "and abstract problem-solving.\n\n"
                    "Paragraph D: Perhaps the most profound implication of bilingualism is its neuroprotective capacity against age-related "
                    "cognitive decline. Longitudinal epidemiological studies led by cognitive neuroscientists demonstrate that lifelong "
                    "bilinguals manifest symptoms of neurodegenerative disorders, such as Alzheimer's disease, an average of four to "
                    "five years later than monolingual cohorts with equivalent neuropathological brain damage. This phenomenon is known "
                    "as 'cognitive reserve'—the brain's enhanced resilience and capability to improvise alternative neural routes around damaged areas."
                ),
                "questions": [
                    {
                        "num": 14,
                        "type": "Matching Information",
                        "prompt": "Which paragraph mentions the historical warning against early multilingual upbringing?",
                        "correct": "Paragraph A",
                        "acceptable": ["A", "Paragraph A"],
                        "evidence": "Paragraph A: For much of the twentieth century, clinical educators cautioned parents against raising children in bilingual households",
                        "explanation": "Paragraph A discusses historical clinical educator warnings."
                    },
                    {
                        "num": 15,
                        "type": "Matching Information",
                        "prompt": "Which paragraph explains the neurological mechanism of co-active lexical networks during speech?",
                        "correct": "Paragraph B",
                        "acceptable": ["B", "Paragraph B"],
                        "evidence": "Paragraph B: When a bilingual individual communicates, both language systems remain perpetually active in the brain.",
                        "explanation": "Paragraph B details co-activation and inhibitory suppression."
                    },
                    {
                        "num": 16,
                        "type": "Matching Information",
                        "prompt": "Which paragraph describes standard laboratory cognitive tests comparing performance speed?",
                        "correct": "Paragraph C",
                        "acceptable": ["C", "Paragraph C"],
                        "evidence": "Paragraph C: In laboratory experiments such as the Simon task and the Stroop color-word test",
                        "explanation": "Paragraph C cites specific experiments like the Simon task and Stroop test."
                    },
                    {
                        "num": 17,
                        "type": "Matching Information",
                        "prompt": "Which paragraph documents statistical delay in symptoms of neurodegenerative disease?",
                        "correct": "Paragraph D",
                        "acceptable": ["D", "Paragraph D"],
                        "evidence": "Paragraph D: manifest symptoms of neurodegenerative disorders... an average of four to five years later",
                        "explanation": "Paragraph D discusses delaying Alzheimer's symptoms by 4-5 years."
                    },
                    {
                        "num": 18,
                        "type": "YNNG",
                        "prompt": "Early 20th-century educators encouraged multilingual upbringing to accelerate intellectual development.",
                        "correct": "No",
                        "evidence": "cautioned parents against raising children in bilingual households, asserting that juggling two grammatical systems would cause cognitive confusion",
                        "explanation": "They cautioned against it, directly contradicting the claim."
                    },
                    {
                        "num": 19,
                        "type": "YNNG",
                        "prompt": "The inactive language is completely de-energized during monolingual speech in a bilingual speaker.",
                        "correct": "No",
                        "evidence": "both language systems remain perpetually active in the brain",
                        "explanation": "Paragraph B states the inactive language remains co-active and primed."
                    },
                    {
                        "num": 20,
                        "type": "YNNG",
                        "prompt": "Bilingual advantages are confined exclusively to verbal and linguistic processing exercises.",
                        "correct": "No",
                        "evidence": "Crucially, this advantage is not restricted to linguistic tasks; it manifests robustly across spatial reasoning and abstract problem-solving",
                        "explanation": "The text states the advantage is NOT restricted to linguistic tasks."
                    },
                    {
                        "num": 21,
                        "type": "YNNG",
                        "prompt": "Bilingualism completely cures patients of underlying Alzheimer's neuropathology.",
                        "correct": "No",
                        "evidence": "manifest symptoms... four to five years later than monolingual cohorts with equivalent neuropathological brain damage",
                        "explanation": "It delays symptom onset via cognitive reserve, but does not cure or eliminate physical neuropathological damage."
                    },
                    {
                        "num": 22,
                        "type": "Completion",
                        "prompt": "Executive function is primarily regulated by the brain's _____ cortex.",
                        "correct": "prefrontal",
                        "acceptable": ["prefrontal", "prefrontal cortex"],
                        "max_words": 2,
                        "evidence": "overseen predominantly by the prefrontal cortex",
                        "explanation": "Paragraph B specifies the prefrontal cortex."
                    },
                    {
                        "num": 23,
                        "type": "Completion",
                        "prompt": "To prevent interference from competing vernaculars, the brain continuously applies _____ control.",
                        "correct": "inhibitory",
                        "acceptable": ["inhibitory", "inhibitory control"],
                        "max_words": 2,
                        "evidence": "must continuously exert inhibitory control to suppress the irrelevant language",
                        "explanation": "Paragraph B names inhibitory control as the mechanism."
                    },
                    {
                        "num": 24,
                        "type": "Completion",
                        "prompt": "Experimental protocols such as the Stroop test and the _____ task confirm rapid stimulus resolution.",
                        "correct": "Simon",
                        "acceptable": ["Simon", "Simon task"],
                        "max_words": 2,
                        "evidence": "such as the Simon task and the Stroop color-word test",
                        "explanation": "Paragraph C explicitly names the Simon task."
                    },
                    {
                        "num": 25,
                        "type": "Completion",
                        "prompt": "Lifelong bilinguals exhibit symptom onset of Alzheimer's approximately _____ years later than monolinguals.",
                        "correct": "four to five",
                        "acceptable": ["four to five", "4 to 5", "4-5"],
                        "max_words": 3,
                        "evidence": "an average of four to five years later",
                        "explanation": "Paragraph D states the average delay is four to five years."
                    },
                    {
                        "num": 26,
                        "type": "MCQ",
                        "prompt": "The term 'cognitive reserve' in Paragraph D most accurately describes:",
                        "options": [
                            "The capacity of the brain to memorize unlimited foreign vocabulary",
                            "The brain's resilience in improvising alternative neural pathways around damage",
                            "A permanent immunity to all forms of neurodegenerative pathology",
                            "The biological requirement to speak three or more unrelated languages"
                        ],
                        "correct": "The brain's resilience in improvising alternative neural pathways around damage",
                        "correct_index": 1,
                        "evidence": "the brain's enhanced resilience and capability to improvise alternative neural routes around damaged areas",
                        "explanation": "Paragraph D defines cognitive reserve as resilience and improvising alternative neural routes."
                    }
                ]
            },
            {
                "passage_number": 3,
                "id": "acad_p3",
                "title": "Urban Heat Islands and Microclimate Architecture",
                "text": (
                    "Paragraph A: The Urban Heat Island (UHI) effect represents one of the starkest anthropogenic modifications of local "
                    "climatology. Modern urban centers exhibit ambient air temperatures between 2 and 6 degrees Celsius higher than "
                    "their surrounding rural peripheries. This thermal disparity stems from the replacement of natural permeable "
                    "vegetation with dense, impervious engineered surfaces—such as asphalt roadways and concrete skyscrapers—which "
                    "exhibit elevated thermal mass and low solar albedo.\n\n"
                    "Paragraph B: During daylight hours, conventional construction materials absorb shortwave solar irradiance and store it "
                    "as sensible heat. Because dense masonry and bituminous pavements lack moisture for evaporative cooling, this trapped "
                    "thermal energy is re-radiated into the canopy layer as longwave infrared radiation throughout the nocturnal cycle, "
                    "preventing nighttime ambient cooling. Furthermore, the geometric morphology of deep urban canyons restricts air "
                    "ventilation and traps re-emitted heat within street corridors.\n\n"
                    "Paragraph C: Anthropogenic heat generation compound the crisis. Heavy vehicular traffic, industrial manufacturing, "
                    "and widespread mechanical air conditioning exhaust immense amounts of waste heat directly into the urban atmosphere. "
                    "This creates a pernicious feedback loop: higher outdoor temperatures trigger increased consumer demand for indoor "
                    "air conditioning, which subsequently expels greater thermal exhaust into the streets, escalating the ambient heat load.\n\n"
                    "Paragraph D: Urban civil engineers and climatologists are implementing bio-responsive mitigation architectures to "
                    "decelerate UHI intensity. Green roofs—soil substrates planted with drought-resistant sedum—substantially reduce rooftop "
                    "surface temperatures through evapotranspiration. Concurrently, retrofitting horizontal surfaces with high-albedo cool "
                    "coatings and integrating permeable hydro-retentive pavers facilitates evaporative moisture retention. Coupled with strategic "
                    "urban forest corridors that optimize prevailing wind channels, these targeted interventions can lower peak metropolitan "
                    "temperatures by up to 3 degrees Celsius, diminishing grid electricity strain and urban heat mortality."
                ),
                "questions": [
                    {
                        "num": 27,
                        "type": "YNNG",
                        "prompt": "Urban Heat Islands exhibit higher ambient temperatures than surrounding rural peripheries.",
                        "correct": "Yes",
                        "evidence": "temperatures between 2 and 6 degrees Celsius higher than their surrounding rural peripheries",
                        "explanation": "Paragraph A directly states urban temperatures are 2 to 6 degrees higher than rural areas."
                    },
                    {
                        "num": 28,
                        "type": "YNNG",
                        "prompt": "Dense concrete and asphalt have higher solar albedo than natural grass and tree canopies.",
                        "correct": "No",
                        "evidence": "exhibit elevated thermal mass and low solar albedo",
                        "explanation": "The text states asphalt and concrete exhibit LOW solar albedo, not higher."
                    },
                    {
                        "num": 29,
                        "type": "YNNG",
                        "prompt": "Narrow urban canyons enhance natural cross-ventilation and rapidly dispel trapped heat.",
                        "correct": "No",
                        "evidence": "deep urban canyons restricts air ventilation and traps re-emitted heat within street corridors",
                        "explanation": "Paragraph B confirms urban canyons restrict ventilation and trap heat rather than dispelling it."
                    },
                    {
                        "num": 30,
                        "type": "YNNG",
                        "prompt": "Mechanical air conditioning exhaust contributes to escalating outdoor street temperatures.",
                        "correct": "Yes",
                        "evidence": "air conditioning exhaust immense amounts of waste heat directly into the urban atmosphere",
                        "explanation": "Paragraph C notes AC systems expel thermal exhaust into the streets, escalating heat."
                    },
                    {
                        "num": 31,
                        "type": "YNNG",
                        "prompt": "Urban heat mitigation techniques have eliminated all human heat mortality in major tropical capitals.",
                        "correct": "Not Given",
                        "evidence": "No claim of total elimination of heat mortality in tropical capitals.",
                        "explanation": "The text states techniques diminish heat mortality, but does not claim complete elimination."
                    },
                    {
                        "num": 32,
                        "type": "Matching Headings",
                        "prompt": "Choose the most appropriate heading for Paragraph A:",
                        "options": [
                            "The Root Physical Causes and Temperature Disparity of UHIs",
                            "The Mechanical Physics of Subterranean Geothermal Energy",
                            "Global Legislation on High-Rise Architectural Zoning",
                            "The Extinction of Urban Wildlife in Concrete Structures"
                        ],
                        "correct": "The Root Physical Causes and Temperature Disparity of UHIs",
                        "correct_index": 0,
                        "evidence": "Paragraph A defines the UHI temperature difference (2-6°C) and replacement of vegetation with impervious surfaces.",
                        "explanation": "Paragraph A introduces the thermal disparity and its primary physical causes."
                    },
                    {
                        "num": 33,
                        "type": "Matching Headings",
                        "prompt": "Choose the most appropriate heading for Paragraph C:",
                        "options": [
                            "Anthropogenic Waste Heat and the Cooling Feedback Loop",
                            "Rural Agricultural Subsidies and Solar Irrigation",
                            "The Historical Invention of Modern Refrigeration",
                            "Satellite Mapping of Oceanic Currents"
                        ],
                        "correct": "Anthropogenic Waste Heat and the Cooling Feedback Loop",
                        "correct_index": 0,
                        "evidence": "Paragraph C analyzes vehicular/AC emissions and the feedback loop of cooling demand.",
                        "explanation": "Paragraph C focuses on human waste heat generation and the vicious AC cycle."
                    },
                    {
                        "num": 34,
                        "type": "Matching Headings",
                        "prompt": "Choose the most appropriate heading for Paragraph D:",
                        "options": [
                            "Architectural Solutions and Microclimate Mitigation Strategies",
                            "The Economic Decline of Commercial Roofing Manufacturers",
                            "Banning Air Conditioning in Residential Developments",
                            "Subterranean Water Reservoirs in Desert Regions"
                        ],
                        "correct": "Architectural Solutions and Microclimate Mitigation Strategies",
                        "correct_index": 0,
                        "evidence": "Paragraph D discusses green roofs, cool coatings, permeable pavers, and wind corridors.",
                        "explanation": "Paragraph D details civil engineering and architectural interventions to mitigate UHI."
                    },
                    {
                        "num": 35,
                        "type": "Completion",
                        "prompt": "Urban centers typically measure between _____ degrees Celsius warmer than neighboring rural fringes.",
                        "correct": "2 and 6",
                        "acceptable": ["2 and 6", "2 to 6", "2-6"],
                        "max_words": 3,
                        "evidence": "temperatures between 2 and 6 degrees Celsius higher",
                        "explanation": "Paragraph A specifies the temperature disparity is 2 to 6 degrees Celsius."
                    },
                    {
                        "num": 36,
                        "type": "Completion",
                        "prompt": "Trapped thermal energy is released at night in the form of longwave _____ radiation.",
                        "correct": "infrared",
                        "acceptable": ["infrared", "infrared radiation"],
                        "max_words": 2,
                        "evidence": "re-radiated into the canopy layer as longwave infrared radiation",
                        "explanation": "Paragraph B states it is re-radiated as longwave infrared radiation."
                    },
                    {
                        "num": 37,
                        "type": "Completion",
                        "prompt": "Green roofs utilize soil substrates planted with drought-resistant _____.",
                        "correct": "sedum",
                        "acceptable": ["sedum", "sedum plants"],
                        "max_words": 2,
                        "evidence": "planted with drought-resistant sedum",
                        "explanation": "Paragraph D notes green roofs are planted with drought-resistant sedum."
                    },
                    {
                        "num": 38,
                        "type": "Completion",
                        "prompt": "Strategic urban forest corridors are designed to optimize channels for prevailing _____.",
                        "correct": "wind",
                        "acceptable": ["wind", "winds", "wind channels"],
                        "max_words": 2,
                        "evidence": "optimize prevailing wind channels",
                        "explanation": "Paragraph D explains forest corridors optimize prevailing wind channels."
                    },
                    {
                        "num": 39,
                        "type": "Completion",
                        "prompt": "Bio-responsive architectural interventions can decrease peak metropolitan temperatures by up to _____ degrees Celsius.",
                        "correct": "3",
                        "acceptable": ["3", "3 degrees", "three"],
                        "max_words": 2,
                        "evidence": "lower peak metropolitan temperatures by up to 3 degrees Celsius",
                        "explanation": "Paragraph D states interventions can lower peak temperatures by up to 3 degrees Celsius."
                    },
                    {
                        "num": 40,
                        "type": "MCQ",
                        "prompt": "What is the primary mechanism by which green roofs reduce surface heat?",
                        "options": [
                            "Reflecting shortwave radiation with metallic sheets",
                            "Evapotranspiration through moisture-retaining plants and soil",
                            "Absorbing nocturnal wind through high-voltage fans",
                            "Channeling rainwater directly into sewer mains"
                        ],
                        "correct": "Evapotranspiration through moisture-retaining plants and soil",
                        "correct_index": 1,
                        "evidence": "substantially reduce rooftop surface temperatures through evapotranspiration",
                        "explanation": "Paragraph D specifies evapotranspiration as the mechanism of green roofs."
                    }
                ]
            }
        ]
    }

    # -------------------------------------------------------------------------
    # 2. GENERAL TRAINING READING FULL MOCK (40 QUESTIONS ACROSS 3 SECTIONS)
    # -------------------------------------------------------------------------
    GENERAL_READING_MOCK_1 = {
        "id": "exam_read_gt_1",
        "title": "IELTS General Training Reading Practice Examination 1",
        "track": "General Training",
        "time_limit_minutes": 60,
        "total_questions": 40,
        "instructions": (
            "You have 60 minutes to complete all 3 sections and 40 questions. "
            "Write your answers in the answer boxes provided."
        ),
        "sections": [
            {
                "section_number": 1,
                "id": "gt_s1",
                "title": "Community Adult Education & Facility Guidelines",
                "text": (
                    "Notice A: Riverside Community College Evening Workshops\n"
                    "Enrollment for spring trimester courses commences on February 1st. We offer practical courses in digital photography, "
                    "introductory accounting, culinary arts, and conversational Spanish. Standard tuition is £140 per 8-week module. "
                    "Early-bird applicants registering prior to January 15th receive a 15% discount. Concession rates (50% reduction) "
                    "are available for verified full-time students, jobseekers, and senior citizens over 65 upon presentation of valid documentation.\n\n"
                    "Notice B: Multi-Purpose Computer Laboratory Regulations\n"
                    "The multimedia computer suites in Building C are accessible Monday through Friday, 08:00 to 21:30, and Saturday, 09:00 to 17:00. "
                    "Users must log in utilizing their college identification credentials. Strictly no open food containers or unsheltered liquids "
                    "are permitted near workstations; sealed spill-proof travel flasks are allowed on floor storage hooks only. Printing quotas "
                    "are capped at 100 monochrome pages per semester. Color printing costs £0.15 per sheet and requires advance credit top-ups "
                    "via the campus portal. All storage media must be virus-scanned at the front reception terminal prior to insertion."
                ),
                "questions": [
                    {
                        "num": 1,
                        "type": "TFNG",
                        "prompt": "Spring evening workshops can be booked starting from the first day of February.",
                        "correct": "True",
                        "evidence": "Enrollment for spring trimester courses commences on February 1st",
                        "explanation": "Notice A confirms enrollment commences on February 1st."
                    },
                    {
                        "num": 2,
                        "type": "TFNG",
                        "prompt": "Applicants registering in late January qualify for the early-bird 15% discount.",
                        "correct": "False",
                        "evidence": "prior to January 15th receive a 15% discount",
                        "explanation": "The early-bird deadline is January 15th; late January does not qualify."
                    },
                    {
                        "num": 3,
                        "type": "TFNG",
                        "prompt": "Senior citizens must provide documentation to secure the 50% concession tuition fee.",
                        "correct": "True",
                        "evidence": "upon presentation of valid documentation",
                        "explanation": "Concession rates require presentation of valid documentation."
                    },
                    {
                        "num": 4,
                        "type": "TFNG",
                        "prompt": "The Building C computer suite remains open on Sunday afternoons.",
                        "correct": "False",
                        "evidence": "accessible Monday through Friday, 08:00 to 21:30, and Saturday, 09:00 to 17:00 [No Sunday hours]",
                        "explanation": "The facility is open Monday to Saturday only; Sunday is closed."
                    },
                    {
                        "num": 5,
                        "type": "TFNG",
                        "prompt": "Uncovered cups of hot coffee are permitted on workstation computer desks.",
                        "correct": "False",
                        "evidence": "Strictly no open food containers or unsheltered liquids are permitted near workstations",
                        "explanation": "Open containers are strictly prohibited near workstations."
                    },
                    {
                        "num": 6,
                        "type": "TFNG",
                        "prompt": "Students receive unlimited free color printing throughout the academic semester.",
                        "correct": "False",
                        "evidence": "Color printing costs £0.15 per sheet and requires advance credit top-ups",
                        "explanation": "Color printing is not free; it costs £0.15 per sheet."
                    },
                    {
                        "num": 7,
                        "type": "TFNG",
                        "prompt": "The campus portal accepts payment via international mobile wallets.",
                        "correct": "Not Given",
                        "evidence": "No mention of specific mobile wallet payment methods.",
                        "explanation": "The text mentions top-ups via campus portal but does not state payment methods."
                    },
                    {
                        "num": 8,
                        "type": "Completion",
                        "prompt": "Standard tuition for an 8-week community college workshop is £_____.",
                        "correct": "140",
                        "acceptable": ["140", "£140"],
                        "max_words": 1,
                        "evidence": "Standard tuition is £140 per 8-week module",
                        "explanation": "Notice A states standard tuition is £140."
                    },
                    {
                        "num": 9,
                        "type": "Completion",
                        "prompt": "Students registering before January 15th obtain a _____% discount.",
                        "correct": "15",
                        "acceptable": ["15", "15%"],
                        "max_words": 1,
                        "evidence": "receive a 15% discount",
                        "explanation": "Notice A states the early-bird reduction is 15%."
                    },
                    {
                        "num": 10,
                        "type": "Completion",
                        "prompt": "Concession rates provide a _____% reduction on course fees.",
                        "correct": "50",
                        "acceptable": ["50", "50%"],
                        "max_words": 1,
                        "evidence": "Concession rates (50% reduction)",
                        "explanation": "Notice A defines concession rate as 50% reduction."
                    },
                    {
                        "num": 11,
                        "type": "Completion",
                        "prompt": "Computer facilities close at _____ on Saturday afternoons.",
                        "correct": "17:00",
                        "acceptable": ["17:00", "5:00 PM", "5 PM"],
                        "max_words": 2,
                        "evidence": "Saturday, 09:00 to 17:00",
                        "explanation": "Notice B specifies Saturday closing time is 17:00."
                    },
                    {
                        "num": 12,
                        "type": "Completion",
                        "prompt": "Free monochrome printing per semester is capped at _____ pages.",
                        "correct": "100",
                        "acceptable": ["100", "100 pages"],
                        "max_words": 2,
                        "evidence": "capped at 100 monochrome pages per semester",
                        "explanation": "Notice B states monochrome quota is 100 pages."
                    },
                    {
                        "num": 13,
                        "type": "Completion",
                        "prompt": "Color printing costs £_____ per individual sheet.",
                        "correct": "0.15",
                        "acceptable": ["0.15", "£0.15", "15p"],
                        "max_words": 1,
                        "evidence": "Color printing costs £0.15 per sheet",
                        "explanation": "Notice B specifies color printing is £0.15 per sheet."
                    },
                    {
                        "num": 14,
                        "type": "Completion",
                        "prompt": "All portable storage media must undergo a virus scan at the front _____.",
                        "correct": "reception terminal",
                        "acceptable": ["reception terminal", "reception"],
                        "max_words": 2,
                        "evidence": "virus-scanned at the front reception terminal",
                        "explanation": "Notice B specifies scanning takes place at the front reception terminal."
                    }
                ]
            },
            {
                "section_number": 2,
                "id": "gt_s2",
                "title": "Corporate Ergonomics & Hybrid Telecommuting Policy",
                "text": (
                    "Section 1: Workstation Setup and Health Guidance\n"
                    "Apex Global Logistics is committed to preventing musculoskeletal strain among corporate and remote personnel. "
                    "When seated at your assigned workstation, adjust the pneumatic chair cylinder so that your forearms rest parallel to "
                    "the desk plane with elbows positioned at approximately 90 degrees. Computer monitors must be positioned directly in "
                    "front of your visual midline at arm's length (50–70 centimeters), with the topmost line of text aligned precisely with "
                    "or slightly below horizontal eye level. Employees spending more than four consecutive hours on display screen equipment "
                    "are mandated to take a five-minute micropauses every hour to practice ocular focal adjustments.\n\n"
                    "Section 2: Hybrid Remote Work Authorization\n"
                    "Full-time personnel completing their six-month probationary review are eligible to request hybrid telecommuting arrangements "
                    "up to a maximum of two days per calendar week. Telecommuting agreements require formal endorsement from your direct department "
                    "supervisor and the Human Resources Directorate. Approved remote workers must ensure access to a secure, private room with "
                    "broadband download speeds exceeding 25 megabits per second. All enterprise computing must be conducted via the company-issued "
                    "Virtual Private Network (VPN) with two-factor token authentication activated at all times."
                ),
                "questions": [
                    {
                        "num": 15,
                        "type": "Completion",
                        "prompt": "Office workers should adjust chair height so that forearms are parallel to the desk with elbows at _____ degrees.",
                        "correct": "90",
                        "acceptable": ["90", "90 degrees"],
                        "max_words": 2,
                        "evidence": "elbows positioned at approximately 90 degrees",
                        "explanation": "Section 1 specifies elbows should be at approximately 90 degrees."
                    },
                    {
                        "num": 16,
                        "type": "Completion",
                        "prompt": "Monitors should be situated at an approximate distance of _____ centimeters from the eyes.",
                        "correct": "50-70",
                        "acceptable": ["50-70", "50 to 70", "50–70"],
                        "max_words": 3,
                        "evidence": "at arm's length (50–70 centimeters)",
                        "explanation": "Section 1 specifies 50-70 centimeters distance."
                    },
                    {
                        "num": 17,
                        "type": "Completion",
                        "prompt": "Staff working over four hours on screens must observe a _____-minute pause every hour.",
                        "correct": "five",
                        "acceptable": ["5", "five", "five-minute"],
                        "max_words": 2,
                        "evidence": "take a five-minute micropauses every hour",
                        "explanation": "Section 1 mandates five-minute pauses."
                    },
                    {
                        "num": 18,
                        "type": "Completion",
                        "prompt": "Employees become eligible to request hybrid work upon finishing their _____-month probationary review.",
                        "correct": "six",
                        "acceptable": ["6", "six", "six-month"],
                        "max_words": 2,
                        "evidence": "completing their six-month probationary review",
                        "explanation": "Section 2 specifies a six-month review."
                    },
                    {
                        "num": 19,
                        "type": "Completion",
                        "prompt": "Approved hybrid arrangements allow staff to telecommute up to _____ days weekly.",
                        "correct": "two",
                        "acceptable": ["2", "two"],
                        "max_words": 1,
                        "evidence": "maximum of two days per calendar week",
                        "explanation": "Section 2 limits telecommuting to two days per week."
                    },
                    {
                        "num": 20,
                        "type": "Completion",
                        "prompt": "Remote home broadband connections must possess download speeds exceeding _____ megabits per second.",
                        "correct": "25",
                        "acceptable": ["25", "25 Mbps"],
                        "max_words": 2,
                        "evidence": "broadband download speeds exceeding 25 megabits per second",
                        "explanation": "Section 2 requires download speeds over 25 Mbps."
                    },
                    {
                        "num": 21,
                        "type": "Completion",
                        "prompt": "Remote corporate computing must be routed exclusively through a Virtual Private _____.",
                        "correct": "Network",
                        "acceptable": ["Network", "VPN"],
                        "max_words": 1,
                        "evidence": "via the company-issued Virtual Private Network (VPN)",
                        "explanation": "Section 2 specifies Virtual Private Network."
                    },
                    {
                        "num": 22,
                        "type": "MCQ",
                        "prompt": "Where should the top line of text on a computer monitor be situated?",
                        "options": [
                            "Directly at or slightly below horizontal eye level",
                            "At least 30 centimeters above head height",
                            "Tilted downwards onto the physical desktop surface",
                            "Positioned adjacent to the office window"
                        ],
                        "correct": "Directly at or slightly below horizontal eye level",
                        "correct_index": 0,
                        "evidence": "with the topmost line of text aligned precisely with or slightly below horizontal eye level",
                        "explanation": "Section 1 specifies precisely at or slightly below eye level."
                    },
                    {
                        "num": 23,
                        "type": "TFNG",
                        "prompt": "Temporary probationary workers in their first month can immediately work from home.",
                        "correct": "False",
                        "evidence": "completing their six-month probationary review are eligible",
                        "explanation": "They must complete 6 months first."
                    },
                    {
                        "num": 24,
                        "type": "TFNG",
                        "prompt": "The company subsidizes employee ergonomic desk chairs for personal home offices.",
                        "correct": "Not Given",
                        "evidence": "No mention of financial chair subsidies for home offices.",
                        "explanation": "The text specifies workstation setup guidelines but does not mention chair subsidies."
                    },
                    {
                        "num": 25,
                        "type": "TFNG",
                        "prompt": "Remote workers must obtain sign-off from both their supervisor and Human Resources.",
                        "correct": "True",
                        "evidence": "require formal endorsement from your direct department supervisor and the Human Resources Directorate",
                        "explanation": "Both direct supervisor and HR Directorate endorsements are required."
                    },
                    {
                        "num": 26,
                        "type": "TFNG",
                        "prompt": "Employees may operate on unsecured public hotel Wi-Fi without VPN tokens.",
                        "correct": "False",
                        "evidence": "conducted via the company-issued Virtual Private Network (VPN) with two-factor token authentication activated at all times",
                        "explanation": "VPN with 2FA token is mandatory at all times."
                    },
                    {
                        "num": 27,
                        "type": "MCQ",
                        "prompt": "What is the primary objective of taking ocular micropauses during screen work?",
                        "options": [
                            "Practicing eye focal adjustments and preventing eye strain",
                            "Allowing the computer processor to cool down",
                            "Answering non-urgent personal telephone calls",
                            "Conducting physical inventory counts in the warehouse"
                        ],
                        "correct": "Practicing eye focal adjustments and preventing eye strain",
                        "correct_index": 0,
                        "evidence": "take a five-minute micropauses every hour to practice ocular focal adjustments",
                        "explanation": "Section 1 mandates pauses to practice ocular focal adjustments."
                    }
                ]
            },
            {
                "section_number": 3,
                "id": "gt_s3",
                "title": "The Evolution & Civil Engineering of the Suspension Bridge",
                "text": (
                    "Paragraph A: For millennia, humanity has engineered bridges to overcome geographical chasms, yet few structural "
                    "forms match the grace and mechanical efficiency of the modern suspension bridge. Developed systematically during "
                    "the Industrial Revolution, the suspension bridge revolutionized transportation by spanning maritime straits and deep "
                    "ravines that resisted conventional stone arch or timber trestle construction.\n\n"
                    "Paragraph B: The fundamental physical principle governing suspension bridges is tensile distribution. Massive vertical "
                    "towers anchored into deep bedrock support twin primary cables woven from thousands of cold-drawn galvanized steel wires. "
                    "Vertical hanger cables (suspenders) descend at regular intervals from these master cables to cradle the road deck below. "
                    "While the deck and passing vehicular traffic exert downward gravitational loads, this weight is transferred upwards "
                    "through the hangers into the main cables as pure tension. The cables in turn channel this immense force across the tower "
                    "saddles and down into monumental concrete anchorages embedded into the earth at each terminal.\n\n"
                    "Paragraph C: However, early nineteenth-century suspension bridges were intensely vulnerable to aerodynamic excitation. "
                    "Because structural engineers prioritized static dead loads over dynamic wind forces, several notable spans suffered "
                    "catastrophic failure during gales. The most famous disaster occurred in November 1940, when the Tacoma Narrows Bridge "
                    "in Washington State collapsed under moderate 42-mile-per-hour winds. Aerodynamic flutter induced violent torsional "
                    "oscillations that twisted the light steel plate girder deck until structural failure ensued.\n\n"
                    "Paragraph D: The Tacoma collapse prompted a total paradigm shift in civil engineering. Modern suspension bridges are "
                    "aerodynamically sculpted in wind tunnels prior to construction. Solid plate girders have been replaced by open aerodynamic "
                    "trusses or aerofoil-shaped hollow steel box girders that permit gusting winds to pass smoothly around the structure without "
                    "generating destructive vortex shedding. Coupled with tuned mass dampers and continuous laser telemetry monitoring, "
                    "contemporary suspension spans routinely exceed two kilometers in central clear span while withstanding typhoon-force winds."
                ),
                "questions": [
                    {
                        "num": 28,
                        "type": "Completion",
                        "prompt": "Suspension bridges transfer structural loads primarily through the physical principle of tensile _____.",
                        "correct": "distribution",
                        "acceptable": ["distribution", "tensile distribution"],
                        "max_words": 2,
                        "evidence": "governing suspension bridges is tensile distribution",
                        "explanation": "Paragraph B states the fundamental principle is tensile distribution."
                    },
                    {
                        "num": 29,
                        "type": "Completion",
                        "prompt": "Master cables are woven from thousands of cold-drawn galvanized _____ wires.",
                        "correct": "steel",
                        "acceptable": ["steel", "galvanized steel"],
                        "max_words": 2,
                        "evidence": "thousands of cold-drawn galvanized steel wires",
                        "explanation": "Paragraph B specifies cold-drawn galvanized steel wires."
                    },
                    {
                        "num": 30,
                        "type": "Completion",
                        "prompt": "Vertical cables that descend to hold the road deck are known as _____.",
                        "correct": "suspenders",
                        "acceptable": ["suspenders", "hangers", "hanger cables"],
                        "max_words": 2,
                        "evidence": "Vertical hanger cables (suspenders) descend at regular intervals",
                        "explanation": "Paragraph B names them vertical hanger cables or suspenders."
                    },
                    {
                        "num": 31,
                        "type": "Completion",
                        "prompt": "Immense tensile forces are channeled across tower saddles into concrete _____ embedded in bedrock.",
                        "correct": "anchorages",
                        "acceptable": ["anchorages", "concrete anchorages"],
                        "max_words": 2,
                        "evidence": "down into monumental concrete anchorages embedded into the earth",
                        "explanation": "Paragraph B identifies monumental concrete anchorages."
                    },
                    {
                        "num": 32,
                        "type": "Completion",
                        "prompt": "The catastrophic collapse of the Tacoma Narrows Bridge occurred in the month of November in _____.",
                        "correct": "1940",
                        "acceptable": ["1940"],
                        "max_words": 1,
                        "evidence": "occurred in November 1940, when the Tacoma Narrows Bridge",
                        "explanation": "Paragraph C states November 1940."
                    },
                    {
                        "num": 33,
                        "type": "Completion",
                        "prompt": "Modern bridge prototypes are tested in _____ tunnels to prevent aerodynamic instability.",
                        "correct": "wind",
                        "acceptable": ["wind", "wind tunnels"],
                        "max_words": 2,
                        "evidence": "aerodynamically sculpted in wind tunnels prior to construction",
                        "explanation": "Paragraph D states they are sculpted in wind tunnels."
                    },
                    {
                        "num": 34,
                        "type": "Completion",
                        "prompt": "Contemporary suspension bridge clear spans frequently exceed _____ kilometers in length.",
                        "correct": "two",
                        "acceptable": ["two", "2", "2 km"],
                        "max_words": 2,
                        "evidence": "routinely exceed two kilometers in central clear span",
                        "explanation": "Paragraph D confirms spans exceed two kilometers."
                    },
                    {
                        "num": 35,
                        "type": "MCQ",
                        "prompt": "What aerodynamic phenomenon caused the catastrophic failure of the Tacoma Narrows Bridge?",
                        "options": [
                            "Extreme seismic tremors fracturing the bedrock towers",
                            "Torsional oscillations induced by aerodynamic flutter",
                            "Overloading by bumper-to-bumper commercial freight trucks",
                            "Corrosion of underwater cable anchorages"
                        ],
                        "correct": "Torsional oscillations induced by aerodynamic flutter",
                        "correct_index": 1,
                        "evidence": "Aerodynamic flutter induced violent torsional oscillations that twisted the light steel plate girder deck",
                        "explanation": "Paragraph C attributes failure to torsional oscillations from aerodynamic flutter."
                    },
                    {
                        "num": 36,
                        "type": "MCQ",
                        "prompt": "How do modern aerodynamic hollow box girders improve structural safety in high winds?",
                        "options": [
                            "They allow gusting winds to pass smoothly without creating destructive vortex shedding",
                            "They are filled with heavy liquid concrete to prevent movement",
                            "They are dismantled and lowered into water during storms",
                            "They convert kinetic wind energy into municipal electricity"
                        ],
                        "correct": "They allow gusting winds to pass smoothly without creating destructive vortex shedding",
                        "correct_index": 0,
                        "evidence": "permit gusting winds to pass smoothly around the structure without generating destructive vortex shedding",
                        "explanation": "Paragraph D explains they allow wind to pass without destructive vortex shedding."
                    },
                    {
                        "num": 37,
                        "type": "YNNG",
                        "prompt": "Suspension bridges were completely unknown prior to the twentieth century.",
                        "correct": "No",
                        "evidence": "Developed systematically during the Industrial Revolution... early nineteenth-century suspension bridges",
                        "explanation": "They were developed during the Industrial Revolution in the 19th century."
                    },
                    {
                        "num": 38,
                        "type": "YNNG",
                        "prompt": "Main suspension cables experience compressive force rather than tensile force.",
                        "correct": "No",
                        "evidence": "weight is transferred upwards through the hangers into the main cables as pure tension",
                        "explanation": "The text states cables experience pure tension, not compression."
                    },
                    {
                        "num": 39,
                        "type": "YNNG",
                        "prompt": "Early 19th-century engineers fully accounted for dynamic aerodynamic wind resonance.",
                        "correct": "No",
                        "evidence": "structural engineers prioritized static dead loads over dynamic wind forces",
                        "explanation": "Engineers prioritized static dead loads and neglected dynamic wind forces."
                    },
                    {
                        "num": 40,
                        "type": "YNNG",
                        "prompt": "Modern civil engineers employ laser telemetry monitoring on contemporary suspension spans.",
                        "correct": "Yes",
                        "evidence": "Coupled with tuned mass dampers and continuous laser telemetry monitoring",
                        "explanation": "Paragraph D confirms the use of continuous laser telemetry monitoring."
                    }
                ]
            }
        ]
    }

    # -------------------------------------------------------------------------
    # 3. COMPLETE WRITING PACKAGES
    # -------------------------------------------------------------------------
    ACADEMIC_WRITING_SET_1 = {
        "id": "exam_write_acad_1",
        "title": "IELTS Academic Writing Practice Examination 1",
        "track": "Academic",
        "time_limit_minutes": 60,
        "instructions": (
            "You have 60 minutes to complete both Task 1 and Task 2. "
            "You should spend about 20 minutes on Task 1 (minimum 150 words) "
            "and about 40 minutes on Task 2 (minimum 250 words). "
            "Task 2 contributes twice as much as Task 1 to your writing score."
        ),
        "task_1": {
            "prompt_id": "acad_t1_emissions",
            "task_number": 1,
            "title": "Industrial Greenhouse Gas Emissions (1990–2025)",
            "min_words": 150,
            "recommended_minutes": 20,
            "prompt": (
                "The line graph illustrates greenhouse gas emissions (in millions of metric tons) produced by "
                "four separate industrial sectors—Energy Production, Transportation, Agriculture, and Manufacturing—in "
                "a European country between 1990 and 2025.\n\n"
                "Summarize the information by selecting and reporting the main features, and make comparisons where relevant.\n"
                "Write at least 150 words."
            )
        },
        "task_2": {
            "prompt_id": "acad_t2_ubi",
            "task_number": 2,
            "title": "Universal Basic Income & Workplace Automation",
            "min_words": 250,
            "recommended_minutes": 40,
            "prompt": (
                "As artificial intelligence and automated robotics increasingly replace manual and white-collar workers, "
                "some economists argue that governments should introduce an unconditional Universal Basic Income (UBI) "
                "for all citizens regardless of employment status. Others contend that this would bankrupt national treasuries "
                "and diminish individual incentive to work.\n\n"
                "To what extent do you agree or disagree with the implementation of a Universal Basic Income? "
                "Give reasons for your answer and include relevant examples from your knowledge or experience.\n"
                "Write at least 250 words."
            )
        }
    }

    GENERAL_WRITING_SET_1 = {
        "id": "exam_write_gt_1",
        "title": "IELTS General Training Writing Practice Examination 1",
        "track": "General Training",
        "time_limit_minutes": 60,
        "instructions": (
            "You have 60 minutes to complete both Task 1 and Task 2. "
            "You should spend about 20 minutes on Task 1 (minimum 150 words) "
            "and about 40 minutes on Task 2 (minimum 250 words)."
        ),
        "task_1": {
            "prompt_id": "gt_t1_airline_complaint",
            "task_number": 1,
            "title": "Damaged Luggage & Delayed International Transit",
            "min_words": 150,
            "recommended_minutes": 20,
            "prompt": (
                "You recently traveled on an international flight with Global Airways. Upon arriving at your destination, "
                "your checked suitcase was delayed by two days, and when finally returned, several valuable personal items "
                "inside were damaged.\n\n"
                "Write a formal letter to the airline's customer service manager. In your letter:\n"
                "• Give full details of your flight itinerary and booking reference\n"
                "• Explain the inconvenience and expenses caused by the luggage delay\n"
                "• Describe the damage to your possessions and demand appropriate compensation\n\n"
                "Write at least 150 words. You do NOT need to write any addresses."
            )
        },
        "task_2": {
            "prompt_id": "gt_t2_remote_work",
            "task_number": 2,
            "title": "Telecommuting, Work-Life Balance & Office Culture",
            "min_words": 250,
            "recommended_minutes": 40,
            "prompt": (
                "An increasing number of employees now work from home using digital technology rather than traveling to a physical office. "
                "While some people believe this improves work-life balance and productivity, others argue it leads to social isolation "
                "and weakens organizational team culture.\n\n"
                "Do you agree or disagree that working from home is more advantageous than working in a traditional workplace? "
                "Give reasons for your answer and include relevant examples from your personal knowledge or experience.\n"
                "Write at least 250 words."
            )
        }
    }

    # -------------------------------------------------------------------------
    # 4. SPEAKING EXAM PACKAGES (PARTS 1, 2 & 3)
    # -------------------------------------------------------------------------
    SPEAKING_SET_1 = {
        "id": "exam_speak_1",
        "title": "IELTS Speaking Practice Examination 1 (Career Ambition & Workplace Dynamics)",
        "time_limit_minutes": 14,
        "instructions": (
            "This speaking practice simulation consists of three sequential stages: "
            "Part 1 (Introduction & Interview - 4-5 mins), "
            "Part 2 (Individual Long Turn with 1 minute preparation countdown - 3-4 mins), "
            "and Part 3 (Two-way Discussion - 4-5 mins)."
        ),
        "part_1": {
            "topic": "Daily Schedule & Professional Aspirations",
            "recommended_minutes": 4,
            "questions": [
                {"id": "sp1_q1", "text": "What time of day do you find yourself most productive, and why?"},
                {"id": "sp1_q2", "text": "Do you prefer sticking to a fixed daily routine or having spontaneous plans?"},
                {"id": "sp1_q3", "text": "What profession or career field did you dream of pursuing when you were a child?"},
                {"id": "sp1_q4", "text": "How do you think your daily work or study routine will change in the next five years?"}
            ]
        },
        "part_2": {
            "topic": "An Ambitious Goal",
            "preparation_seconds": 60,
            "speaking_seconds": 120,
            "cue_card": {
                "task": "Describe an ambitious goal or project you successfully achieved.",
                "points": [
                    "What the goal or project was",
                    "When and why you decided to pursue it",
                    "What obstacles or challenges you faced along the way",
                    "And explain why this achievement was particularly meaningful to you"
                ],
                "follow_up_question": "Did achieving this goal encourage you to set even more ambitious targets?"
            }
        },
        "part_3": {
            "topic": "Career Ambition, Automation & Society",
            "recommended_minutes": 5,
            "questions": [
                {"id": "sp3_q1", "text": "Why do some individuals prioritize career ambition over personal relationships and leisure?"},
                {"id": "sp3_q2", "text": "How does parental expectation influence the career ambitions of young people in your country?"},
                {"id": "sp3_q3", "text": "In what ways might artificial intelligence and automation alter the types of ambitions people pursue in the future?"},
                {"id": "sp3_q4", "text": "Is material wealth the most reliable benchmark of professional achievement in modern society?"}
            ]
        }
    }

    # -------------------------------------------------------------------------
    # UTILITY METHODS & SECURITY CONCEALMENT
    # -------------------------------------------------------------------------
    @classmethod
    def get_exam_package(cls, exam_id: str, conceal_answers: bool = True) -> Optional[Dict[str, Any]]:
        """
        Retrieves a full examination package by ID.
        If conceal_answers is True, removes all correct answers, evidence, and explanations
        so sensitive keys are never exposed in pre-submission client payloads.
        """
        raw_pkg = None

        if exam_id in ("exam_read_acad_1", "reading_acad"):
            raw_pkg = copy.deepcopy(cls.ACADEMIC_READING_MOCK_1)
        elif exam_id in ("exam_read_gt_1", "reading_gt"):
            raw_pkg = copy.deepcopy(cls.GENERAL_READING_MOCK_1)
        elif exam_id in ("exam_listen_1", "listening_full"):
            raw_pkg = {
                "id": "exam_listen_1",
                "title": "IELTS Listening Practice Examination 1",
                "mock_id": "mock_listening_full",
                "time_limit_minutes": 32,
                "total_questions": 40,
                "sections": [copy.deepcopy(ListeningEngine.SECTIONS[f"sec_{i}"]) for i in range(1, 5)],
                "activity_type": "transcript_strategy_practice_and_synthesis",
                "audio_asset_status": "speech_synthesis_ready (pre-recorded studio audio files not bundled)",
                "exam_concealment_mode": conceal_answers,
                "instructions": (
                    "You have approximately 30 minutes to listen to 4 recorded sections and 2 minutes to review your answers. "
                    "Write your answers in the answer boxes provided."
                )
            }
        elif exam_id in ("exam_write_acad_1", "writing_acad"):
            raw_pkg = copy.deepcopy(cls.ACADEMIC_WRITING_SET_1)
        elif exam_id in ("exam_write_gt_1", "writing_gt"):
            raw_pkg = copy.deepcopy(cls.GENERAL_WRITING_SET_1)
        elif exam_id in ("exam_speak_1", "speaking_full"):
            raw_pkg = copy.deepcopy(cls.SPEAKING_SET_1)
        elif exam_id == "mock_full_acad":
            raw_pkg = {
                "id": "mock_full_acad",
                "title": "IELTS Academic Full Practice Examination",
                "track": "Academic",
                "total_time_minutes": 164, # 30 listening + 60 reading + 60 writing + 14 speaking
                "skills": {
                    "listening": cls.get_exam_package("exam_listen_1", conceal_answers=conceal_answers),
                    "reading": cls.get_exam_package("exam_read_acad_1", conceal_answers=conceal_answers),
                    "writing": cls.get_exam_package("exam_write_acad_1", conceal_answers=conceal_answers),
                    "speaking": cls.get_exam_package("exam_speak_1", conceal_answers=conceal_answers)
                }
            }
            return raw_pkg
        elif exam_id == "mock_full_gt":
            raw_pkg = {
                "id": "mock_full_gt",
                "title": "IELTS General Training Full Practice Examination",
                "track": "General Training",
                "total_time_minutes": 164,
                "skills": {
                    "listening": cls.get_exam_package("exam_listen_1", conceal_answers=conceal_answers),
                    "reading": cls.get_exam_package("exam_read_gt_1", conceal_answers=conceal_answers),
                    "writing": cls.get_exam_package("exam_write_gt_1", conceal_answers=conceal_answers),
                    "speaking": cls.get_exam_package("exam_speak_1", conceal_answers=conceal_answers)
                }
            }
            return raw_pkg

        if not raw_pkg:
            return None

        if conceal_answers:
            raw_pkg = cls.sanitize_for_client(raw_pkg)

        return raw_pkg

    @classmethod
    def sanitize_for_client(cls, package: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitizes examination structures to strip all answer keys and evidence."""
        sanitized = copy.deepcopy(package)

        def sanitize_question(q: Dict[str, Any]):
            # Strip answer keys
            q.pop("correct", None)
            q.pop("correct_index", None)
            q.pop("acceptable", None)
            q.pop("evidence", None)
            q.pop("explanation", None)
            q.pop("distractor_analysis", None)
            q.pop("distractor_note", None)

        if "passages" in sanitized:
            for p in sanitized["passages"]:
                p.pop("synonym_table", None)
                for q in p.get("questions", []):
                    sanitize_question(q)

        if "sections" in sanitized:
            for s in sanitized["sections"]:
                s.pop("synonym_table", None)
                # Keep audio_script so browser Web Speech synthesis can vocalize the dialogue,
                # but question answer keys and notes are strictly sanitized below.
                for q in s.get("questions", []):
                    sanitize_question(q)

        return sanitized

    @classmethod
    def list_available_exams(cls) -> List[Dict[str, Any]]:
        """Returns catalog of all available full and skill-specific practice examinations."""
        return [
            {
                "id": "mock_full_acad",
                "title": "IELTS Academic Full Practice Examination",
                "track": "Academic",
                "format": "Full 4-Skill Mock (Listening, Reading, Writing, Speaking)",
                "duration_minutes": 164,
                "total_questions": 82, # 40 listening + 40 reading + 2 writing tasks
                "availability": "Complete Original Examination"
            },
            {
                "id": "mock_full_gt",
                "title": "IELTS General Training Full Practice Examination",
                "track": "General Training",
                "format": "Full 4-Skill Mock (Listening, Reading, Writing, Speaking)",
                "duration_minutes": 164,
                "total_questions": 82,
                "availability": "Complete Original Examination"
            },
            {
                "id": "exam_read_acad_1",
                "title": "Academic Reading Examination 1",
                "track": "Academic",
                "format": "Reading (3 Passages, 40 Questions)",
                "duration_minutes": 60,
                "total_questions": 40,
                "availability": "Complete Original Examination"
            },
            {
                "id": "exam_read_gt_1",
                "title": "General Training Reading Examination 1",
                "track": "General Training",
                "format": "Reading (3 Sections, 40 Questions)",
                "duration_minutes": 60,
                "total_questions": 40,
                "availability": "Complete Original Examination"
            },
            {
                "id": "exam_listen_1",
                "title": "Listening Practice Examination 1",
                "track": "Academic & General Training",
                "format": "Listening (4 Sections, 40 Questions)",
                "duration_minutes": 32,
                "total_questions": 40,
                "availability": "Complete Original Examination (Web Speech Synthesis)"
            },
            {
                "id": "exam_write_acad_1",
                "title": "Academic Writing Practice Examination 1",
                "track": "Academic",
                "format": "Writing (Task 1 Report + Task 2 Essay)",
                "duration_minutes": 60,
                "total_questions": 2,
                "availability": "Complete Original Examination"
            },
            {
                "id": "exam_write_gt_1",
                "title": "General Training Writing Practice Examination 1",
                "track": "General Training",
                "format": "Writing (Task 1 Letter + Task 2 Essay)",
                "duration_minutes": 60,
                "total_questions": 2,
                "availability": "Complete Original Examination"
            },
            {
                "id": "exam_speak_1",
                "title": "Speaking Practice Examination 1",
                "track": "Academic & General Training",
                "format": "Speaking (Parts 1, 2, 3 with 1-min prep timer)",
                "duration_minutes": 14,
                "total_questions": 9,
                "availability": "Complete Original Examination (Speech-to-Text Transcripts)"
            }
        ]
