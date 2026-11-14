# -*- coding: utf-8 -*-
"""
Deep Comprehensive Curriculum Builder for C1 and C2 (Phase 13).
Preserves all 18 existing lesson IDs across C1 and C2 with rich educational depth:
- Explanations > 800 chars with structural formulas, rhetorical patterns, common errors
- 3+ authentic examples with Band 8.5/9.0 notes
- 3 guided exercises with step-by-step reasoning
- 3 assessment quiz questions with 3-4 options and explanations for all choices
"""

import json

# -------------------------------------------------------------
# C1 ADVANCED (9 Lessons)
# -------------------------------------------------------------
C1_LESSONS = [
    {
        "id": "curric_c1_gram_inversion_cleft",
        "cefr_level": "C1",
        "module_type": "grammar",
        "title": "Syntactic Inversion, Cleft Sentences & Fronting",
        "order_index": 1,
        "prerequisites": ["curric_b2_gram_conditionals"],
        "estimated_minutes": 55,
        "objectives": [
            "Construct negative and restrictive adverbial inversions ('Rarely have we...', 'Seldom does...', 'Under no circumstances should...')",
            "Deploy wh-clefts ('What concerns researchers is...') and it-clefts ('It was the policy that...') for rhetorical emphasis",
            "Apply fronted prepositional phrases and participial clauses to elevate prose register in IELTS Writing Task 2",
            "Eliminate inversion errors such as forgetting auxiliary verbs or double subject marking"
        ],
        "explanation_markdown": """### 1. Negative & Restrictive Adverbial Inversion
When a negative or restrictive adverbial is fronted (placed at the opening of a clause for rhetorical emphasis), the subject and auxiliary verb invert (identical to question order):
$$\\text{Negative Adverbial} + \\text{Auxiliary Verb} + \\text{Subject} + \\text{Main Verb}$$

#### Common Negative Triggers:
- **Rarely / Seldom:** *Rarely have environmental scientists witnessed such rapid glacial retreat.*
- **Scarcely / Hardly... when:** *Hardly had the fiscal stimulus been announced when inflation surged.*
- **Under no circumstances:** *Under no circumstances should ethical oversight be bypassed.*
- **Not only... but also:** *Not only did the intervention stabilize employment, but it also spurred innovation.*
- **Only by / Only when:** *Only by diversifying the curriculum can schools address structural inequality.*

### 2. Cleft Sentences (Information Packaging)
Cleft sentences cleave (split) a single clause to focus spotlight on a specific component:
- **It-Cleft:** *It was the lack of transparency that precipitated the corporate collapse.*
- **Wh-Cleft (Pseudo-cleft):** *What policymakers frequently overlook is the sociological impact of automation.*
- **All-Cleft:** *All the community requested was access to potable groundwater.*

### 3. Common Learner Traps:
1. **Forgetting Inversion:** ✗ *Rarely the government intervenes.* ➔ ✓ *Rarely does the government intervene.*
2. **Double Past Marking:** ✗ *Not only did they lost funding...* ➔ ✓ *Not only did they lose funding...*""",
        "examples": [
            {"text": "Seldom have technological disruptions reshaped societal labor dynamics with such unrelenting velocity.", "notes": "Fronted negative adverbial 'Seldom' with subject-auxiliary inversion ('have... disruptions reshaped')."},
            {"text": "What distinguishes elite educational institutions is not their physical infrastructure, but their pedagogical ethos.", "notes": "Wh-cleft sentence spotlighting the contrasted subject complement."},
            {"text": "Only through sustained multilateral cooperation can international carbon abatement targets be realistically achieved.", "notes": "Restrictive fronting ('Only through...') with inverted passive auxiliary ('can... targets be achieved')."}
        ],
        "guided_exercises": [
            {
                "id": "c1_g_ge_1",
                "prompt": "Rewrite using inversion starting with 'Rarely': 'Researchers have rarely observed such anomalous behavior.'",
                "answer": "Rarely have researchers observed such anomalous behavior.",
                "explanation": "Front 'Rarely', followed by auxiliary 'have', subject 'researchers', and participle 'observed'."
            },
            {
                "id": "c1_g_ge_2",
                "prompt": "Transform into an it-cleft emphasizing 'the regulatory deficit': 'The regulatory deficit caused the market failure.'",
                "answer": "It was the regulatory deficit that caused the market failure.",
                "explanation": "Formula: 'It was + focused element + that/which + remainder of sentence'."
            },
            {
                "id": "c1_g_ge_3",
                "prompt": "Complete with inversion: 'Not only _____ (the policy / reduce) emissions, but it also generated revenue.'",
                "answer": "did the policy reduce",
                "explanation": "'Not only' requires auxiliary 'did' + subject 'the policy' + base verb 'reduce'."
            }
        ],
        "assessment": [
            {
                "id": "c1_g_as_1",
                "question": "Which sentence demonstrates grammatically flawless negative inversion?",
                "options": [
                    "Seldom we have witnessed such profound economic disruption.",
                    "Seldom have we witnessed such profound economic disruption.",
                    "Seldom did we witnessed such profound economic disruption.",
                    "Seldom we witnessed such profound economic disruption."
                ],
                "correct_index": 1,
                "explanation": "'Seldom' + auxiliary 'have' + subject 'we' + past participle 'witnessed'."
            },
            {
                "id": "c1_g_as_2",
                "question": "What is the primary rhetorical purpose of a wh-cleft sentence in academic writing?",
                "options": [
                    "To confuse the reader with convoluted grammar",
                    "To focus attention deliberately onto a specific clause element by splitting the proposition",
                    "To avoid using proper nouns",
                    "To artificially inflate word counts in examinations"
                ],
                "correct_index": 1,
                "explanation": "Clefting packages information dynamically, placing emphasis on the most prominent analytical point."
            },
            {
                "id": "c1_g_as_3",
                "question": "Choose the correctly inverted sentence beginning with 'Only by':",
                "options": [
                    "Only by investing in public health governments can prevent pandemics.",
                    "Only by investing in public health can governments prevent pandemics.",
                    "Only by investing in public health do governments preventing pandemics.",
                    "Only by investing in public health governments prevent pandemics."
                ],
                "correct_index": 1,
                "explanation": "'Only by [gerund]' requires modal inversion: 'can governments prevent'."
            }
        ]
    },
    {
        "id": "curric_c1_vocab_academic_lexis",
        "cefr_level": "C1",
        "module_type": "vocabulary",
        "title": "Academic Lexis, Nominalization & Precision",
        "order_index": 2,
        "prerequisites": ["curric_b2_vocab_technology_environment"],
        "estimated_minutes": 55,
        "objectives": [
            "Transform spoken verb-heavy clauses into dense, authoritative nominalized academic syntax",
            "Command Academic Word List (AWL) sublists 7–10 lexis ('paradigm', 'empirical', 'ubiquitous', 'inexorable')",
            "Deploy precise analytical collocations ('conduct rigorous empirical inquiry', 'engender socio-economic disparity')"
        ],
        "explanation_markdown": """### 1. Nominalization (Grammatical Metaphor)
Nominalization is the conversion of verbs, adjectives, and entire clauses into noun phrases. It is the hallmark of publication-grade academic and journalistic prose:

- **Spoken / Clunky (Verb-Heavy):**
  * *Because crime rates grew rapidly after the factory closed, people became very worried about safety.*
- **Academic / Nominalized (Noun-Heavy):**
  * *The rapid escalation in urban criminality subsequent to industrial disinvestment precipitated widespread public concern regarding municipal safety.*

#### Structural Transformations:
- Verb $\\rightarrow$ Noun: *escalate $\\rightarrow$ escalation*, *deteriorate $\\rightarrow$ deterioration*, *disinvest $\\rightarrow$ disinvestment*.
- Adjective $\\rightarrow$ Noun: *resilient $\\rightarrow$ resilience*, *vulnerable $\\rightarrow$ vulnerability*, *scarce $\\rightarrow$ scarcity*.

### 2. High-Tier Academic Precision Verbs:
- **engender** (v) = to cause or give rise to (*discriminatory algorithms engender societal distrust*).
- **ameliorate** (v) = to improve a negative condition (*subsidies ameliorate rural poverty*).
- **obviate** (v) = to remove or avoid the need for (*preventive healthcare obviates emergency hospitalization*).""",
        "examples": [
            {"text": "The inexorable proliferation of automated surveillance technologies engenders profound civil liberties dilemmas.", "notes": "Nominalization: 'inexorable proliferation' and academic verb 'engenders'."},
            {"text": "Rigorous empirical scrutiny of clinical trial datasets is indispensable to obviate experimental bias.", "notes": "Precision lexis: 'empirical scrutiny' and 'obviate'."},
            {"text": "Fiscal austerity measures frequently exacerbate socio-economic stratification rather than ameliorating it.", "notes": "Juxtaposition of high-tier verbs 'exacerbate' and 'ameliorate'."}
        ],
        "guided_exercises": [
            {
                "id": "c1_v_ge_1",
                "prompt": "Nominalize: 'Because the climate is warming rapidly...' (The rapid _____ of the climate)",
                "answer": "warming",
                "explanation": "Convert verb to verbal noun / noun phrase: 'The rapid warming of the global climate'."
            },
            {
                "id": "c1_v_ge_2",
                "prompt": "Insert the verb meaning 'to eliminate the need for something': 'Early intervention can _____ invasive surgery.' (obviate / generate)",
                "answer": "obviate",
                "explanation": "'Obviate' means to render unnecessary or circumvent."
            },
            {
                "id": "c1_v_ge_3",
                "prompt": "Select the formal synonym for 'present everywhere': (ubiquitous / localized)",
                "answer": "ubiquitous",
                "explanation": "'Ubiquitous' describes phenomena that are omnipresent or widespread."
            }
        ],
        "assessment": [
            {
                "id": "c1_v_as_1",
                "question": "Which sentence demonstrates the most sophisticated nominalized academic style?",
                "options": [
                    "When the city grew very fast, there were lots of problems with traffic because too many people drove cars.",
                    "The rapid acceleration of urban demographic expansion precipitated severe vehicular congestion across central transport arteries.",
                    "Cars caused bad traffic when the town grew big quickly.",
                    "People driving caused congestion because city growth happened."
                ],
                "correct_index": 1,
                "explanation": "Replaces sprawling verb clauses with compact, authoritative nominalized academic syntax."
            },
            {
                "id": "c1_v_as_2",
                "question": "What is the meaning of the academic verb 'ameliorate'?",
                "options": [
                    "To make something worse or deteriorate",
                    "To improve or make a tolerable condition better",
                    "To measure temperature mathematically",
                    "To delete digital files permanently"
                ],
                "correct_index": 1,
                "explanation": "'Ameliorate' denotes improving or alleviating a defective state."
            },
            {
                "id": "c1_v_as_3",
                "question": "Which collocation is natural and accurate in Band 8+ academic discourse?",
                "options": [
                    "conduct rigorous empirical analysis",
                    "make heavy empirical research",
                    "do deep analytical thinking",
                    "create big empirical studies"
                ],
                "correct_index": 0,
                "explanation": "'Conduct rigorous empirical analysis' is the established academic pairing."
            }
        ]
    },
    {
        "id": "curric_c1_read_evaluating_arguments",
        "cefr_level": "C1",
        "module_type": "reading",
        "title": "Evaluating Argument Strength, Bias & Tone",
        "order_index": 3,
        "prerequisites": ["curric_b2_read_claims", "curric_c1_vocab_academic_lexis"],
        "estimated_minutes": 55,
        "objectives": [
            "Deconstruct subtle authorial skepticism, ironic undertones, and ideological bias in academic texts",
            "Differentiate between empirically substantiated claims and speculative hypotheses in scientific papers",
            "Identify methodological caveats and limitations acknowledged by researchers"
        ],
        "explanation_markdown": """### Critical Discourse Analysis in C1 Reading
At CEFR C1, texts do not merely state facts; they construct ideological arguments using subtle stance markers, ironic litotes, and calculated hedges.

#### Passage Excerpt: The Techno-Optimist Fallacy
```
Silicon Valley venture capitalists frequently proclaim that generative machine intelligence 
will inaugurate an era of boundless intellectual abundance. Such utopian prognostications, 
while undeniably intoxicating to corporate shareholders, betray a breathtaking indifference 
to the macroeconomic frictions of labor displacement. History offers scant evidence that 
displaced workers seamlessly transition into high-concept engineering roles. To blithely 
dismiss transitional human hardship as mere 'creative destruction' is less an economic 
philosophy than an act of callous moral abdication.
```

#### Analytical Breakdown:
- **Author Stance:** Highly critical of techno-utopian claims.
- **Tonal Identifiers:** Words like *'prognostications'*, *'intoxicating'*, *'breathtaking indifference'*, *'scant evidence'*, *'blithely dismiss'*, *'callous moral abdication'*.
- **Rhetorical Technique:** Acknowledges the appeal to shareholders before dismantling the underlying premise with historical counter-evidence.""",
        "examples": [
            {"text": "The author's tone toward Silicon Valley optimism is scathingly critical and ethically skeptical.", "notes": "Deducing tone from loaded evaluative vocabulary."},
            {"text": "The phrase 'callous moral abdication' reveals strong authorial condemnation.", "notes": "Identifying evaluative moral judgments."},
            {"text": "The text refutes the assumption that displaced workers transition easily to new tech roles.", "notes": "Extracting evidential refutation."}
        ],
        "guided_exercises": [
            {
                "id": "c1_r_ge_1",
                "prompt": "What does the author imply by describing predictions as 'utopian prognostications'?",
                "answer": "They are unrealistic, idealized, and disconnected from practical reality.",
                "explanation": "'Utopian' implies impractical perfectionism; 'prognostications' conveys detached forecasting."
            },
            {
                "id": "c1_r_ge_2",
                "prompt": "How does the author evaluate the historical claim that workers transition seamlessly into tech roles?",
                "answer": "History offers scant (almost zero) evidence for it.",
                "explanation": "The text states 'History offers scant evidence that displaced workers seamlessly transition'."
            },
            {
                "id": "c1_r_ge_3",
                "prompt": "Identify the tone of the final sentence: (objective / scathing / admiring)",
                "answer": "scathing",
                "explanation": "Terms like 'callous moral abdication' reflect scathing ethical critique."
            }
        ],
        "assessment": [
            {
                "id": "c1_r_as_1",
                "question": "What is the primary overarching argument asserted by the author in the excerpt?",
                "options": [
                    "Generative AI will eradicate poverty by 2030",
                    "Techno-optimist predictions ignore the severe human and economic hardships of technological labor displacement",
                    "Computer scientists should receive higher venture capital investment",
                    "Creative destruction is an admirable ethical philosophy"
                ],
                "correct_index": 1,
                "explanation": "The author argues that dismissing worker hardship as 'creative destruction' is morally indefensible and empirically unfounded."
            },
            {
                "id": "c1_r_as_2",
                "question": "Which phrase in the passage most explicitly conveys authorial disapproval of corporate attitudes?",
                "options": [
                    "'Silicon Valley venture capitalists'",
                    "'boundless intellectual abundance'",
                    "'breathtaking indifference to the macroeconomic frictions'",
                    "'generative machine intelligence'"
                ],
                "correct_index": 2,
                "explanation": "'Breathtaking indifference' directly censures corporate disregard for displaced workers."
            },
            {
                "id": "c1_r_as_3",
                "question": "In academic reading, what does the word 'scant' signify when describing empirical evidence?",
                "options": [
                    "Overwhelming and conclusive",
                    "Barely sufficient or almost non-existent",
                    "Highly controversial",
                    "Fraudulent"
                ],
                "correct_index": 1,
                "explanation": "'Scant' means deficient in quantity; meager or almost none."
            }
        ]
    },
    {
        "id": "curric_c1_listen_synthesis",
        "cefr_level": "C1",
        "module_type": "listening",
        "title": "Synthesizing Information Across Multiple Speakers",
        "order_index": 4,
        "prerequisites": ["curric_b2_listen_debates"],
        "estimated_minutes": 55,
        "objectives": [
            "Synthesize contrasting viewpoints across interdisciplinary panel presentations",
            "Identify implicit concessions and methodological limitations in spoken academic delivery",
            "Reconstruct overarching conference consensus from fragmented conversational contributions"
        ],
        "explanation_markdown": """### Transcript-Based Listening Strategy: Interdisciplinary Symposia
*(Practice session using authentic academic panel scripts.)*

#### Audio Script: Sustainable Urban Transport Panel
```
MODERATOR: Turning to panelist Dr Chen from Macroeconomics, and Professor Okafor from Environmental Health.
DR CHEN: The data on congestion charging zones is unequivocal. Imposing an eighteen-pound daily levy 
in central corridors curtailed vehicular congestion by twenty-six percent. From an economic efficiency 
perspective, market-clearing pricing models internalize negative externalities effectively.
PROF OKAFOR: While the statistical drop in particulate matter emissions is commendable, Dr Chen's economic 
model operates in a sociological vacuum. What the macroeconomic data obscures is the regressive tax burden 
imposed on shift workers—nurses, hospitality staff, emergency cleaners—who cannot commute during standard 
transit operating hours.
DR CHEN: That is an incisive critique, Okafor. If the revenue generated by the levy is strictly hypothecated 
towards round-the-clock electric bus transit, the regressive incidence is substantially mitigated.
PROF OKAFOR: If hypothecated, yes. But municipal history reveals that transit revenues are routinely diverted 
to general municipal budget shortfalls.
```

#### Analytical Synthesis Markers:
- **Economic Paradigm:** Market efficiency, negative externalities, congestion charging.
- **Sociological / Health Critique:** Regressive tax burden on vulnerable shift workers.
- **Proposed Rebuttal / Compromise:** Revenue hypothecation (ring-fencing funds for public transit).
- **Residual Skepticism:** Historical diversion of funds to municipal shortfalls.""",
        "examples": [
            {"text": "Dr Chen supports congestion charges based on traffic reduction and economic externalities.", "notes": "Synthesizing economic panelist stance."},
            {"text": "Professor Okafor critiques the charges as a regressive tax on vulnerable night workers.", "notes": "Identifying sociological counter-argument."},
            {"text": "Both panelists agree that hypothecated revenue for public transit could solve the dilemma, though skepticism remains.", "notes": "Identifying points of convergence and divergence."}
        ],
        "guided_exercises": [
            {
                "id": "c1_l_ge_1",
                "prompt": "What percentage did vehicular congestion decrease following the levy?",
                "answer": "twenty-six percent",
                "explanation": "Dr Chen notes congestion was 'curtailed by twenty-six percent'."
            },
            {
                "id": "c1_l_ge_2",
                "prompt": "What demographic group does Prof Okafor highlight as bearing an unfair burden?",
                "answer": "shift workers (nurses, hospitality staff, cleaners)",
                "explanation": "Okafor highlights 'shift workers—nurses, hospitality staff, emergency cleaners'."
            },
            {
                "id": "c1_l_ge_3",
                "prompt": "What economic term refers to legally dedicating tax revenue to a specific public purpose?",
                "answer": "hypothecation / hypothecated",
                "explanation": "'Hypothecated' means revenue is ring-fenced for a dedicated project."
            }
        ],
        "assessment": [
            {
                "id": "c1_l_as_1",
                "question": "What is the core disagreement between Dr Chen and Professor Okafor?",
                "options": [
                    "Whether cars cause air pollution",
                    "Whether market pricing models equitably account for socio-economic impacts on low-income shift workers",
                    "Whether buses should have electric motors",
                    "Whether nurses should work at night"
                ],
                "correct_index": 1,
                "explanation": "The debate centers on market pricing versus the regressive burden on night workers."
            },
            {
                "id": "c1_l_as_2",
                "question": "What does Prof Okafor cite as the major historical impediment to Dr Chen's hypothecation solution?",
                "options": [
                    "Bus drivers refusing to work",
                    "Municipalities routinely diverting transit revenues into general budget shortfalls",
                    "Voters voting to eliminate buses",
                    "The price of electric batteries increasing"
                ],
                "correct_index": 1,
                "explanation": "Okafor notes municipal history shows revenues are routinely diverted away from transit."
            },
            {
                "id": "c1_l_as_3",
                "question": "What does 'regressive tax' mean in public policy discourse?",
                "options": [
                    "A tax that charges wealthy people more",
                    "A tax that takes a proportionally larger percentage of income from low earners than from high earners",
                    "A tax that is abolished",
                    "An environmental subsidy"
                ],
                "correct_index": 1,
                "explanation": "A regressive tax places a heavier financial burden on lower-income individuals."
            }
        ]
    },
    {
        "id": "curric_c1_write_counterarguments",
        "cefr_level": "C1",
        "module_type": "writing",
        "title": "Counter-Arguments, Rebuttal & Nuanced Thesis Statements",
        "order_index": 5,
        "prerequisites": ["curric_b2_write_peel", "curric_c1_gram_inversion_cleft"],
        "estimated_minutes": 60,
        "objectives": [
            "Structure advanced dialectical paragraphs integrating concessions, counter-arguments, and decisive rebuttals",
            "Articulate non-dichotomous, nuanced thesis statements that reject simplistic black-and-white dichotomies",
            "Command Band 8.5+ argumentative framing devices ('While proponents maintain X, this argument disintegrates when...')"
        ],
        "explanation_markdown": """### 1. Moving Beyond Simplistic '50/50' Essays
In IELTS Task 2, Band 8 and 9 essays do NOT say: *'Some people think X, some people think Y, and I agree with X.'*
Instead, high-band writers construct a **qualified, dialectical thesis**:
- *'While proponents of market deregulation contend that commercial freedom maximizes economic agility, such perspectives overlook systemic externalities; therefore, targeted government intervention remains indispensable to prevent infrastructural monopolization.'*

### 2. The 4-Part Concession-Rebuttal Paragraph
1. **Concession to Opponent's Strongest Point:**
   * *'Admittedly, proponents of complete technological automation correctly observe that robotics eradicate human computational error in manufacturing...'*
2. **Identification of Flaw / Limitation:**
   * *'...However, this perspective conflates mechanical throughput with holistic organizational agility.'*
3. **Rebuttal Evidence:**
   * *'Automated systems lack the lateral problem-solving necessary to respond to unpredictable supply chain shocks, as demonstrated during recent global logistical disruptions.'*
4. **Synthesis / Decisive Verdict:**
   * *'Consequently, the optimal paradigm is not total human displacement, but symbiotic human-in-the-loop workflows.'*""",
        "examples": [
            {"text": "While proponents of universal basic income argue that direct cash transfers eradicate absolute poverty, this assertion disintegrates when factoring in localized inflationary pressure.", "notes": "Sophisticated concession-rebuttal framing."},
            {"text": "Admittedly, strict copyright enforcement protects corporate royalties; however, overzealous litigation stifles grassroots innovation.", "notes": "Balanced academic synthesis."},
            {"text": "Therefore, the question is not whether to regulate AI, but how to architect regulatory frameworks that balance public safety with entrepreneurial agility.", "notes": "Non-dichotomous conclusion framing."}
        ],
        "guided_exercises": [
            {
                "id": "c1_w_ge_1",
                "prompt": "Insert a formal concession marker: '_____, early childhood education requires significant capital outlay; nevertheless, long-term returns are immense.' (Admittedly / Yes)",
                "answer": "Admittedly",
                "explanation": "'Admittedly' formally concedes a valid counterpoint before presenting the rebuttal."
            },
            {
                "id": "c1_w_ge_2",
                "prompt": "Transform this simplistic thesis: 'I think both sides are good.'",
                "answer": "While both perspectives possess merit, a balanced integration offers the most resilient long-term outcome.",
                "explanation": "Synthesizes dual perspectives into an authoritative academic stance."
            },
            {
                "id": "c1_w_ge_3",
                "prompt": "Which phrase introduces an analytical flaw in an opponent's argument? (This assertion overlooks... / They are silly)",
                "answer": "This assertion overlooks",
                "explanation": "'This assertion overlooks / conflates...' identifies analytical shortcomings professionally."
            }
        ],
        "assessment": [
            {
                "id": "c1_w_as_1",
                "question": "Which of the following represents a Band 8.5+ nuanced thesis statement on government arts funding?",
                "options": [
                    "I will discuss both sides of funding and say my opinion in the end.",
                    "While fiscal conservatives maintain that public revenue should be restricted to essential infrastructure, artistic and cultural heritage fosters societal cohesion and lateral innovation, thereby fully justifying municipal subsidies.",
                    "Art is very beautiful and hospitals are also important so governments must pay both.",
                    "Some people like painting and some people like hospitals."
                ],
                "correct_index": 1,
                "explanation": "Concedes the opposing view, provides reasoned justification for personal stance, and uses high-tier lexis."
            },
            {
                "id": "c1_w_as_2",
                "question": "Why is the concession-rebuttal technique valued by examiners in IELTS Task 2 essays?",
                "options": [
                    "Because it demonstrates the candidate can critically engage with counter-arguments rather than ignoring opposing viewpoints",
                    "Because it makes the essay longer without needing new ideas",
                    "Because examiners love reading two separate conclusions",
                    "Because it allows the writer to avoid having a clear opinion"
                ],
                "correct_index": 0,
                "explanation": "Criterion Task Response explicitly rewards well-developed responses with thoroughly supported and qualified ideas."
            },
            {
                "id": "c1_w_as_3",
                "question": "What is the meaning of the academic phrase 'conflates X with Y'?",
                "options": [
                    "Correctly separates two distinct ideas",
                    "Erronously merges or confuses two distinct concepts into one",
                    "Deletes an idea from an essay",
                    "Translates between languages"
                ],
                "correct_index": 1,
                "explanation": "To 'conflate' means to treat two fundamentally different things as identical, creating logical fallacy."
            }
        ]
    },
    {
        "id": "curric_c1_speak_nuance_hedging",
        "cefr_level": "C1",
        "module_type": "speaking",
        "title": "Nuance, Epistemic Hedging & Speculative Discourse",
        "order_index": 6,
        "prerequisites": ["curric_b2_speak_complex_arguments"],
        "estimated_minutes": 55,
        "objectives": [
            "Modulate spoken claims using epistemic modality and academic hedging devices ('It is conceivable that...', 'Evidence tentatively suggests...')",
            "Discuss speculative and counterfactual future scenarios with spontaneous cognitive agility in IELTS Part 3",
            "Eliminate dogmatic over-generalizations ('all people', 'always', 'impossible') in formal spoken discourse"
        ],
        "explanation_markdown": """### 1. The Power of Epistemic Hedging
In advanced English, dogmatic overstatements (*'Mobile phones cause mental illness in all teenagers'*) are regarded as unscholarly. C1 speakers hedge assertions to reflect realistic probability:

#### Degrees of Epistemic Certainty:
- **Strong Conviction (High Probability):**
  * *'There is compelling empirical evidence to suggest that...'*
  * *'It is virtually indisputable that...'*
- **Moderate Probability (Prudent Hedging):**
  * *'It is highly plausible that...'*
  * *'The findings appear to indicate a discernible correlation between X and Y.'*
- **Tentative / Speculative (Possibility):**
  * *'One cannot rule out the possibility that...'*
  * *'It remains conceivable, albeit unproven, that...'*

### 2. Speculative Counterfactual Discourse
When asked about future trends (*'What will cities look like in fifty years?'*):
- Avoid: ✗ *'Everyone will live in flying cars.'*
- Deploy: ✓ *'Barring unforeseen geopolitical crises, it is conceivable that urban infrastructure will pivot towards vertical hydroponics and localized micro-grids.'*""",
        "examples": [
            {"text": "It is conceivable that aggressive automation will prompt governments to pilot universal basic income programs.", "notes": "Cautious speculative hedging ('conceivable')."},
            {"text": "There appears to be a discernible correlation between urban density and enhanced entrepreneurial dynamism.", "notes": "Prudent empirical hedging ('appears to be a discernible correlation')."},
            {"text": "Barring catastrophic economic turmoil, international tourism will likely rebound to pre-pandemic trajectories.", "notes": "Conditional qualification preceding prediction."}
        ],
        "guided_exercises": [
            {
                "id": "c1_sp_ge_1",
                "prompt": "Hedge this dogmatic statement: 'Social media destroys teenagers' attention spans.'",
                "answer": "Excessive social media consumption appears to impair adolescent attention spans.",
                "explanation": "Replaces absolute 'destroys' with calibrated hedge 'appears to impair'."
            },
            {
                "id": "c1_sp_ge_2",
                "prompt": "Insert a speculative hedge: 'It is _____ that quantum computing will revolutionize cryptography.' (conceivable / impossible)",
                "answer": "conceivable",
                "explanation": "'Conceivable' indicates plausible future probability."
            },
            {
                "id": "c1_sp_ge_3",
                "prompt": "Complete the phrase: 'One cannot rule _____ the possibility of renewed inflation.' (in / out / off)",
                "answer": "out",
                "explanation": "The idiom is 'rule out the possibility' (eliminate as potential outcome)."
            }
        ],
        "assessment": [
            {
                "id": "c1_sp_as_1",
                "question": "Which response to 'Will artificial intelligence replace human teachers?' reflects Band 8+ academic hedging?",
                "options": [
                    "Yes, all human teachers will be fired in two years.",
                    "While AI will inevitably automate routine grading and administrative workflows, it remains highly improbable that algorithms can replicate the empathetic mentorship and pastoral guidance that human educators provide.",
                    "Computers cannot teach anything because they have no soul.",
                    "Nobody knows anything about the future."
                ],
                "correct_index": 1,
                "explanation": "Distinguishes administrative automation from irreplaceable human pastoral mentorship using calibrated modal hedging."
            },
            {
                "id": "c1_sp_as_2",
                "question": "Why is epistemic hedging critical in IELTS Speaking Part 3?",
                "options": [
                    "To hide the fact that you do not know the answer",
                    "To avoid naive, dogmatic generalizations and demonstrate nuanced academic thinking",
                    "Because the examiner penalizes any use of the word 'will'",
                    "To speak as quietly as possible"
                ],
                "correct_index": 1,
                "explanation": "Hedging demonstrates intellectual maturity and linguistic precision."
            },
            {
                "id": "c1_sp_as_3",
                "question": "What is the meaning of 'barring unforeseen disruptions' in predictive discourse?",
                "options": [
                    "Unless unexpected problems occur",
                    "Because disruptions are guaranteed",
                    "After disruptions have ended",
                    "Without planning"
                ],
                "correct_index": 0,
                "explanation": "'Barring' means 'except for' or 'unless obstructed by'."
            }
        ]
    },
    {
        "id": "curric_c1_pron_intonation",
        "cefr_level": "C1",
        "module_type": "pronunciation",
        "title": "Contrastive Intonation & Tonic Prominence",
        "order_index": 7,
        "prerequisites": ["curric_b2_pron_connected_speech"],
        "estimated_minutes": 55,
        "objectives": [
            "Shift the tonic nucleus across a sentence to alter pragmatic presuppositions and communicative focus",
            "Deploy fall-rise intonation contours to signal reservation, non-finality, and polite disagreement",
            "Use intonational pitch range to express irony, enthusiasm, and academic skepticism"
        ],
        "explanation_markdown": """### Tonic Prominence (Nuclear Pitch Movement)
In English sentences, moving the primary pitch change (tonic stress) completely alters the implicit meaning:

#### Notice How Meaning Shifts:
1. **'I** didn't say she stole my book.* (Someone else said it, not me).
2. *I **didn't** say she stole my book.* (I categorically deny saying it).
3. *I didn't **say** she stole my book.* (I implied or wrote it, but didn't speak it aloud).
4. *I didn't say **she** stole my book.* (Someone else stole it, not her).
5. *I didn't say she **stole** my book.* (She borrowed it without permission, didn't steal it).
6. *I didn't say she stole **my** book.* (She stole someone else's book).

### 2. Fall-Rise Contours for Tactful Reservation
- **Falling Tone (\\):** Signals finality, certainty, factual assertion (*'The results are conclusive.'*).
- **Fall-Rise Tone (\\/):** Signals doubt, qualification, reservation, or unstated subtext:
  * *'The theoretical framework is sound... \\/ (but empirical proof is lacking).'*
  * *'I agree with your premise... \\/ (however the budget is impossible).'*""",
        "examples": [
            {"text": "The theoretical methodology is sound \\/ (fall-rise conveying implicit reservation).", "notes": "Fall-rise contour signaling unstated critique."},
            {"text": "She didn't fail the examination; she excelled \\ (falling tone indicating definitive certainty).", "notes": "Contrastive nucleus placement."},
            {"text": "It was David who initiated the proposal, not Sarah.", "notes": "Tonic prominence on 'David' to refute false attribution."}
        ],
        "guided_exercises": [
            {
                "id": "c1_p_ge_1",
                "prompt": "If you emphasize 'Sarah' in 'I invited Sarah to the symposium', what do you imply?",
                "answer": "You invited Sarah, and not someone else.",
                "explanation": "Tonic stress on 'Sarah' creates contrast against other potential attendees."
            },
            {
                "id": "c1_p_ge_2",
                "prompt": "What intonation contour signals non-finality or polite reservation? (Falling / Fall-Rise)",
                "answer": "Fall-Rise",
                "explanation": "The fall-rise intonational contour signals that there is an unstated qualification or concession."
            },
            {
                "id": "c1_p_ge_3",
                "prompt": "Where should tonic stress fall to deny taking money: 'I didn't steal the money.'?",
                "answer": "steal",
                "explanation": "Stressing 'steal' emphasizes that the action was not theft (e.g. it was borrowed)."
            }
        ],
        "assessment": [
            {
                "id": "c1_p_as_1",
                "question": "What is the pragmatic implication when a speaker delivers 'The preliminary data looks promising' with a fall-rise tone?",
                "options": [
                    "The speaker is 100% finished speaking and has no doubts",
                    "The speaker has reservations or anticipates that final data may contradict the early trend",
                    "The speaker is asking for a dictionary",
                    "The speaker does not speak English"
                ],
                "correct_index": 1,
                "explanation": "A fall-rise contour pragmatically signals doubt, non-finality, or an unvoiced reservation."
            },
            {
                "id": "c1_p_as_2",
                "question": "What is 'tonic prominence' in phonological theory?",
                "options": [
                    "Speaking louder than everyone in the room",
                    "The primary syllable in an intonation unit where the major pitch movement occurs",
                    "Singing in harmony",
                    "Pronouncing silent letters"
                ],
                "correct_index": 1,
                "explanation": "Tonic prominence marks the nuclear syllable bearing the decisive pitch direction."
            },
            {
                "id": "c1_p_as_3",
                "question": "How can contrastive stress correct a listener's misunderstanding of 'Did you buy the green car?'?",
                "options": [
                    "'No, I bought the BLUE car.'",
                    "'No, I am walking.'",
                    "'Cars are green.'",
                    "'I don't know.'"
                ],
                "correct_index": 0,
                "explanation": "Placing tonic prominence on 'BLUE' explicitly contrasts with the mistaken 'green'."
            }
        ]
    },
    {
        "id": "curric_c1_func_negotiation",
        "cefr_level": "C1",
        "module_type": "functional",
        "title": "Negotiation, Strategic Bargaining & Conflict Resolution",
        "order_index": 8,
        "prerequisites": ["curric_b2_func_meetings"],
        "estimated_minutes": 55,
        "objectives": [
            "Signal tactical concessions and conditional offers ('Provided that you agree to X, we can concede Y')",
            "Defuse entrenched adversarial deadlocks through non-combative reframing and interest-based bargaining",
            "Close high-stakes commercial agreements with watertight contractual clarity"
        ],
        "explanation_markdown": """### 1. The Language of Principled Negotiation
In executive negotiations, blunt ultimatum language (*'Take it or leave it'*) destroys business partnerships. Advanced negotiators use **Conditional Concession Framing**:
- **Formula:** *Provided that / On condition that / As long as [Your Condition], we would be prepared to [Concession].*
- **Example:** *'Provided that your logistics division guarantees 48-hour delivery benchmarks, we would be prepared to extend the exclusivity agreement for an additional eighteen months.'*

### 2. Defusing Deadlocks & Reframing
When discussions reach an impasse:
- Reframing: *'It appears we share the same overarching objective regarding cybersecurity; our disagreement concerns implementation pacing rather than technical architecture.'*
- Probing Interests: *'Could you help us understand the regulatory constraint that makes our proposed delivery date problematic from your standpoint?'*
- Safe Hypotheticals: *'Hypothetically speaking, if we were to absorb the upfront testing costs, would you be in a position to reconsider the unit pricing?'*""",
        "examples": [
            {"text": "Provided that your consortium absorbs the transit insurance liability, we would be amenable to expediting the production timetable.", "notes": "Formal conditional concession formula."},
            {"text": "Hypothetically speaking, were we to restructure the payment milestones into quarterly tranches, would that alleviate your cash-flow concerns?", "notes": "Inverted hypothetical condition to unlock deadlock."},
            {"text": "Let us summarize our mutually agreed positions before documenting the final memorandum of understanding.", "notes": "Professional contractual alignment."}
        ],
        "guided_exercises": [
            {
                "id": "c1_f_ge_1",
                "prompt": "Insert a conditional connector: '_____ that you commit to the volume targets, we can offer a 10% discount.' (Provided / Although)",
                "answer": "Provided",
                "explanation": "'Provided that' introduces a mandatory prerequisite condition in formal negotiation."
            },
            {
                "id": "c1_f_ge_2",
                "prompt": "Reframe a conflict non-combatively: 'You are stalling our launch.'",
                "answer": "It seems we have differing timelines regarding launch readiness.",
                "explanation": "Reframes an accusation into an objective difference in scheduling priorities."
            },
            {
                "id": "c1_f_ge_3",
                "prompt": "What does 'amenable to' mean in commercial negotiation? (willing to agree to / hostile towards)",
                "answer": "willing to agree to",
                "explanation": "'Amenable to' signifies readiness to accept or cooperate with a proposal."
            }
        ],
        "assessment": [
            {
                "id": "c1_f_as_1",
                "question": "Which statement demonstrates the most effective conditional bargaining technique?",
                "options": [
                    "You must lower the price or we will terminate the meeting immediately.",
                    "On condition that you increase the minimum order volume to five thousand units, we would be amenable to reducing the unit cost by eight percent.",
                    "We want discounts because we are a big company.",
                    "Why are your prices so high?"
                ],
                "correct_index": 1,
                "explanation": "Pairs a firm business condition with a concrete concession in formal diplomatic register."
            },
            {
                "id": "c1_f_as_2",
                "question": "What is the primary advantage of posing hypothetical questions ('What if we were to...') during an impasse?",
                "options": [
                    "It binds both parties to a legal contract instantly",
                    "It allows exploration of potential solutions without legally committing either party",
                    "It distracts the other party from reading the contract",
                    "It guarantees an automatic victory"
                ],
                "correct_index": 1,
                "explanation": "Hypothetical inquiries permit safe exploration of trade-offs without committing either side prematurely."
            },
            {
                "id": "c1_f_as_3",
                "question": "What does 'hypothecated revenue' mean in bilateral fiscal negotiations?",
                "options": [
                    "Money that has been stolen",
                    "Revenue legally ring-fenced and restricted exclusively to a specific designated project",
                    "Income from gambling",
                    "Uncollectible debt"
                ],
                "correct_index": 1,
                "explanation": "Hypothecated funds are legally dedicated to a specific expenditure purpose."
            }
        ]
    },
    {
        "id": "curric_c1_review_milestone",
        "cefr_level": "C1",
        "module_type": "review",
        "title": "C1 Milestone Review & Comprehensive Evaluation",
        "order_index": 9,
        "prerequisites": ["curric_c1_gram_inversion_cleft", "curric_c1_write_counterarguments"],
        "estimated_minutes": 60,
        "objectives": [
            "Demonstrate mastery of syntactic inversion, wh-clefting, academic nominalization, and epistemic hedging",
            "Validate readiness for C2 Proficiency capstone work and IELTS Band 7.5–8.5 performance",
            "Synthesize complex dialectical counter-argumentation and principled diplomatic negotiation"
        ],
        "explanation_markdown": """### C1 Milestone Synthesis
Attaining CEFR C1 signifies operational language mastery capable of conducting demanding academic research, publication writing, and executive negotiation:
1. **Syntactic Sophistication:** Spontaneous execution of negative inversion (*Rarely have...*), cleft sentences (*It was X that...*), and participial fronting.
2. **Lexical Precision:** Replacing verb-heavy sprawl with nominalized academic discourse (*precipitation of urban unrest*).
3. **Dialectical Argumentation:** Developing concession-rebuttal paragraphs that deconstruct opposing arguments methodically.
4. **Epistemic Calibration:** Modulating claims with academic hedging (*plausible, tentative, conceivable*).

Pass this milestone examination to unlock CEFR C2 Proficiency.""",
        "examples": [
            {"text": "Rarely has technological disruption precipitated such widespread structural reorganization across international labor markets.", "notes": "Negative inversion with advanced academic nominalization."},
            {"text": "While techno-optimists champion unchecked automation, this perspective collapses when evaluating sociological displacement.", "notes": "Concession-rebuttal dialectic."},
            {"text": "Provided that intellectual property rights are mutually respected, our consortium is amenable to technology transfer.", "notes": "Strategic negotiation conditional concession."}
        ],
        "guided_exercises": [
            {
                "id": "c1_rev_ge_1",
                "prompt": "Rewrite with inversion: 'We have seldom observed such blatant methodological bias.'",
                "answer": "Seldom have we observed such blatant methodological bias.",
                "explanation": "Front 'Seldom' + auxiliary 'have' + subject 'we' + participle 'observed'."
            },
            {
                "id": "c1_rev_ge_2",
                "prompt": "Hedge this assertion: 'This policy will fail.'",
                "answer": "It appears highly probable that this policy will encounter substantial implementation friction.",
                "explanation": "Replaces crude dogma with scholarly academic hedging."
            },
            {
                "id": "c1_rev_ge_3",
                "prompt": "Nominalize: 'Because the river was polluted, fish died.'",
                "answer": "Riverine pollution precipitated widespread aquatic mortality.",
                "explanation": "Elevates informal causality into publication-grade nominalized prose."
            }
        ],
        "assessment": [
            {
                "id": "c1_rev_as_1",
                "question": "Which sentence demonstrates 100% flawless C1 syntactic and stylistic mastery?",
                "options": [
                    "Rarely governments intervene when technology creates bad things for workers.",
                    "Seldom have public authorities intervened with such decisive alacrity to mitigate algorithmic discrimination.",
                    "Not only the government intervened, but they made a new law.",
                    "Under no circumstances governments should forget workers."
                ],
                "correct_index": 1,
                "explanation": "'Seldom have public authorities intervened...' executes inverted auxiliary, high-tier lexis ('alacrity', 'mitigate'), and flawless concord."
            },
            {
                "id": "c1_rev_as_2",
                "question": "What distinguishes a Band 8.5 IELTS essay from a Band 6.5 essay in Task Response?",
                "options": [
                    "The Band 8.5 essay is typed faster",
                    "The Band 8.5 essay presents a fully developed, nuanced response with critically evaluated counter-arguments and precise academic register",
                    "The Band 8.5 essay uses only one-syllable words",
                    "There is no difference"
                ],
                "correct_index": 1,
                "explanation": "Band 8.5+ requires sophisticated, nuanced engagement with the complexity of the prompt."
            },
            {
                "id": "c1_rev_as_3",
                "question": "In negotiation, which structure represents the most professional conditional concession?",
                "options": [
                    "Give me what I want or I quit.",
                    "Provided that your team assumes liability for transit insurance, we would be prepared to expedite delivery.",
                    "We will think about it if you are nice.",
                    "Pay more money now."
                ],
                "correct_index": 1,
                "explanation": "'Provided that... we would be prepared to...' is the gold-standard formal negotiation protocol."
            }
        ]
    }
]

# -------------------------------------------------------------
# C2 PROFICIENCY (9 Lessons)
# -------------------------------------------------------------
C2_LESSONS = [
    {
        "id": "curric_c2_gram_subjunctive_ellipses",
        "cefr_level": "C2",
        "module_type": "grammar",
        "title": "The Mandative Subjunctive, Stylistic Ellipsis & Gapping",
        "order_index": 1,
        "prerequisites": ["curric_c1_gram_inversion_cleft"],
        "estimated_minutes": 55,
        "objectives": [
            "Master the formal mandative subjunctive mood in legislative, legal, and academic clauses ('insist that he submit', 'vital that she be informed')",
            "Deploy syntactic ellipsis and gapping to eliminate redundant verbiage in publication-grade prose",
            "Command rare stylistic preposing and absolute participial constructions ('The motion having carried, the assembly adjourned')"
        ],
        "explanation_markdown": """### 1. The Mandative Subjunctive Mood
In high formal register (legal, parliamentary, academic), the mandative subjunctive uses the **base infinitive form of the verb for all persons** (including third-person singular):
- **Triggers:** Verbs of demand, recommendation, urgency (*insist, recommend, demand, mandate, stipulate, propose*) and adjectives (*essential, vital, imperative, crucial*):
  * *The tribunal mandated that the corporation **cease** (NOT ceases) industrial extraction immediately.*
  * *It is imperative that every candidate **be** (NOT is) verified prior to ballot counting.*
  * *The committee recommends that the director **resign** (NOT resigns).*

### 2. Stylistic Ellipsis & Gapping
C2 prose achieves conciseness by omitting words that are recoverable from context:
- **Gapping (Omitting repeated verbs):**
  * *Oxford produced six prime ministers; Cambridge, four.* (The verb 'produced' is gapped).
- **Adverbial Ellipsis:**
  * *When [he was] asked about the deficit, the minister hesitated.*

### 3. Absolute Participial Clauses
A noun + participle construction having no grammatical attachment to the main clause:
- *The committee **having adjourned**, delegates departed for the evening reception.*""",
        "examples": [
            {"text": "The international treaty stipulates that each signatory state submit comprehensive carbon auditing reports annually.", "notes": "Mandative subjunctive: 'stipulate that state submit' (base infinitive)."},
            {"text": "The senior diplomat advocated caution; the junior attaché, immediate confrontation.", "notes": "Stylistic gapping omitting the repeated verb 'advocated'."},
            {"text": "All formalities having been executed, the commercial merger officially closed.", "notes": "Absolute participial clause establishing temporal independence."}
        ],
        "guided_exercises": [
            {
                "id": "c2_g_ge_1",
                "prompt": "Apply the mandative subjunctive: 'The judge demanded that the defendant _____ (stand) in the dock.'",
                "answer": "stand",
                "explanation": "Mandative subjunctive requires base form 'stand' (NOT 'stands')."
            },
            {
                "id": "c2_g_ge_2",
                "prompt": "Apply the subjunctive verb 'to be': 'It is essential that she _____ (be) notified of the verdict.'",
                "answer": "be",
                "explanation": "The subjunctive form of 'to be' is simply 'be' for all persons."
            },
            {
                "id": "c2_g_ge_3",
                "prompt": "Complete with gapping: 'The treasury released fiscal reserves; the central bank, monetary liquidity.' What verb is omitted?",
                "answer": "released",
                "explanation": "The verb 'released' is elliptically gapped after the semicolon."
            }
        ],
        "assessment": [
            {
                "id": "c2_g_as_1",
                "question": "Which sentence demonstrates the correct use of the formal mandative subjunctive?",
                "options": [
                    "The hospital ethics committee insisted that the surgeon performs the audit.",
                    "The hospital ethics committee insisted that the surgeon perform the audit.",
                    "The hospital ethics committee insisted that the surgeon will perform the audit.",
                    "The hospital ethics committee insisted that the surgeon performed the audit."
                ],
                "correct_index": 1,
                "explanation": "Mandative subjunctive uses the base verb: 'insisted that the surgeon perform'."
            },
            {
                "id": "c2_g_as_2",
                "question": "What stylistic device is demonstrated in: 'Athens bequeathed philosophy to posterity; Rome, law.'?",
                "options": [
                    "Tautology",
                    "Gapping (verbal ellipsis)",
                    "Hyperbole",
                    "Malapropism"
                ],
                "correct_index": 1,
                "explanation": "The second clause omits the verb 'bequeathed' via stylistic gapping."
            },
            {
                "id": "c2_g_as_3",
                "question": "Identify the absolute clause in: 'The weather having deteriorated rapidly, mountaineers abandoned the summit push.'",
                "options": [
                    "The weather having deteriorated rapidly",
                    "mountaineers abandoned the summit push",
                    "having deteriorated rapidly mountaineers",
                    "the summit push"
                ],
                "correct_index": 0,
                "explanation": "'The weather having deteriorated rapidly' is an independent absolute participial construction."
            }
        ]
    },
    {
        "id": "curric_c2_vocab_idiomatic_mastery",
        "cefr_level": "C2",
        "module_type": "vocabulary",
        "title": "Idiomatic Mastery, Metaphor & Rare Lexis",
        "order_index": 2,
        "prerequisites": ["curric_c1_vocab_academic_lexis"],
        "estimated_minutes": 55,
        "objectives": [
            "Deploy literary and erudite idioms with flawless sociolinguistic register ('Gordian knot', 'Pyrrhic victory', 'Achilles heel')",
            "Distinguish between subtle connotations of high-tier literary synonyms ('ephemeral' vs 'transitory' vs 'fugacious')",
            "Deconstruct conceptual metaphors in high-stakes editorial and philosophical essays"
        ],
        "explanation_markdown": """### 1. Erudite Classical & Literary Idioms
At C2, idiomatic mastery does not mean using overused street slang (*'raining cats and dogs'*). It means deploying erudite idioms that encapsulate complex historical and philosophical concepts:
- **A Pyrrhic Victory:** A victory achieved at such devastating cost that it is tantamount to defeat.
- **Cutting the Gordian Knot:** Resolving a seemingly intractable problem through bold, unconventional action.
- **The Sword of Damocles:** An imminent and pervasive peril hanging over an apparently prosperous situation.
- **Crossing the Rubicon:** Taking an irrevocable step committing oneself to a hazardous course of action.

### 2. Nuanced Connotative Distinction
Examine three words meaning 'lasting a short time':
- **Ephemeral:** Emphasizes transient beauty and delicate fragility (*ephemeral spring blossoms, ephemeral celebrity*).
- **Transitory:** Emphasizes impermanence and progression through stages (*transitory economic fluctuations*).
- **Fleeting:** Emphasizes swift, vanishing speed (*a fleeting glimpse of truth*).

### 3. Conceptual Metaphor
Abstract reasoning is expressed via embodied metaphors:
- Argument is War (*defend a thesis, shoot down an objection, entrench a position*).
- Ideas are Commodities (*buy into an ideology, sell an agenda, bankrupt philosophy*).""",
        "examples": [
            {"text": "The company secured a Pyrrhic victory in the patent lawsuit, bankrupting its reserves on legal retainers.", "notes": "Erudite idiom: Pyrrhic victory."},
            {"text": "The regulatory agency cut the Gordian knot of cryptocurrency oversight by classifying all tokens as securities.", "notes": "Classical idiom: cutting the Gordian knot."},
            {"text": "Youth and beauty are proverbially ephemeral; wisdom, enduring.", "notes": "Literary precision with 'ephemeral'."}
        ],
        "guided_exercises": [
            {
                "id": "c2_v_ge_1",
                "prompt": "Which idiom describes a success achieved at such catastrophic expense that it amounts to defeat? (Pyrrhic victory / Golden handshake)",
                "answer": "Pyrrhic victory",
                "explanation": "A Pyrrhic victory originates from King Pyrrhus, whose victories against Rome cost his entire army."
            },
            {
                "id": "c2_v_ge_2",
                "prompt": "Insert the adjective meaning 'lasting for only a very brief, beautiful moment': 'The _____ glory of the cherry blossoms.' (ephemeral / durable)",
                "answer": "ephemeral",
                "explanation": "'Ephemeral' denotes short-lived, transient beauty."
            },
            {
                "id": "c2_v_ge_3",
                "prompt": "Complete the historical idiom: 'Once we sign this contract, we have crossed the _____.' (Rubicon / Thames)",
                "answer": "Rubicon",
                "explanation": "Crossing the Rubicon (from Julius Caesar) means committing to an irrevocable decision."
            }
        ],
        "assessment": [
            {
                "id": "c2_v_as_1",
                "question": "What is the meaning of 'a Damoclean threat' in political commentary?",
                "options": [
                    "A danger that has already passed",
                    "A constant, imminent danger hanging over a situation",
                    "A fabricated lie",
                    "An environmental treaty"
                ],
                "correct_index": 1,
                "explanation": "The Sword of Damocles symbolizes an ever-present peril suspended above someone in power."
            },
            {
                "id": "c2_v_as_2",
                "question": "Which sentence demonstrates the most authentic, non-cliché C2 metaphorical style?",
                "options": [
                    "It was a piece of cake to pass the examination.",
                    "The minister's aggressive rhetoric was intended to burnish his populist credentials before the general election.",
                    "At the end of the day, it's raining cats and dogs.",
                    "He is the apple of my eye in the office."
                ],
                "correct_index": 1,
                "explanation": "'Burnish populist credentials' is sophisticated, natural contemporary political prose."
            },
            {
                "id": "c2_v_as_3",
                "question": "What is the subtle difference between 'transitory' and 'ephemeral'?",
                "options": [
                    "'Transitory' relates to stages of passing change; 'ephemeral' evokes fleeting, delicate short-livedness.",
                    "There is no difference.",
                    "'Ephemeral' is only used for food.",
                    "'Transitory' is informal slang."
                ],
                "correct_index": 0,
                "explanation": "Transitory emphasizes passing states of time; ephemeral captures delicate, short-lived fragility."
            }
        ]
    },
    {
        "id": "curric_c2_read_subtext",
        "cefr_level": "C2",
        "module_type": "reading",
        "title": "Dissecting Irony, Subtext & Dense Philosophy",
        "order_index": 3,
        "prerequisites": ["curric_c1_read_evaluating_arguments", "curric_c2_vocab_idiomatic_mastery"],
        "estimated_minutes": 55,
        "objectives": [
            "Decode multi-layered satire, ironic understatement (litotes), and ideological presupposition in dense prose",
            "Synthesize complex dialectical epistemologies across conflicting philosophical and economic paradigms",
            "Identify implicit authorial cynicism masked by courteous superficial academic praise"
        ],
        "explanation_markdown": """### Hermeneutic Decoding of C2 Subtext
At CEFR C2, authors frequently say the opposite of what they mean to execute biting satire or philosophical irony:

#### Literary Excerpt: The Meritocratic Illusion
```
How reassuring it must be for our titan industrialists to contemplate their celestial fortunes 
and reflect that every guinea was acquired through immaculate individual genius. What a fortunate 
coincidence that merit, in its boundless cosmic wisdom, chose to incarnate exclusively within 
the sons of hereditary dukes and venture hedge-fund magnates. One can only marvel at the 
metaphysical harmony that aligns superior intellect so unfailingly with prior capital endowment. 
To suggest that inherited wealth, private schooling, and familial cronyism might have exerted 
the slightest nudge upon their ascent would be, of course, the most vulgar variety of envy.
```

#### Analytical Deconstruction:
- **Literal Surface:** The author appears to praise industrialists for genius and cosmic merit.
- **Hermeneutic Subtext (The Real Meaning):** Biting, contemptuous sarcasm. The author is ruthlessly mocking the myth of meritocracy by exposing that wealth is simply inherited privilege and cronyism.
- **Rhetorical Litotes:** *'the slightest nudge'* (ironic understatement for massive unfair advantage).
- **Mock Pretentiousness:** *'celestial fortunes'*, *'immaculate individual genius'*, *'boundless cosmic wisdom'*.""",
        "examples": [
            {"text": "The author ruthlessly satirizes the myth of self-made billionaires as an illusion of inherited privilege.", "notes": "Decoding satirical subtext contrary to literal surface words."},
            {"text": "The phrase 'most vulgar variety of envy' ironically parodies how the wealthy deflect legitimate systemic critique.", "notes": "Analyzing ideological defense mechanisms."},
            {"text": "Irony operates through mock flattery: 'celestial fortunes' and 'immaculate genius'.", "notes": "Identifying linguistic markers of satire."}
        ],
        "guided_exercises": [
            {
                "id": "c2_r_ge_1",
                "prompt": "Does the author genuinely believe industrialists acquired wealth through 'immaculate individual genius'? (Yes / No)",
                "answer": "No",
                "explanation": "The entire passage is ironic sarcasm; the author believes wealth stems from inheritance and cronyism."
            },
            {
                "id": "c2_r_ge_2",
                "prompt": "What does the author identify as the real causes of their success?",
                "answer": "inherited wealth, private schooling, and familial cronyism",
                "explanation": "Explicitly exposed in the penultimate sentence."
            },
            {
                "id": "c2_r_ge_3",
                "prompt": "What rhetorical device is 'celestial fortunes'? (Hyperbole / Irony / Sarcastic flattery)",
                "answer": "Sarcastic flattery",
                "explanation": "Elevating earthly money to 'celestial' heights mocks the arrogance of the wealthy."
            }
        ],
        "assessment": [
            {
                "id": "c2_r_as_1",
                "question": "What is the primary rhetorical technique employed throughout the excerpt?",
                "options": [
                    "Straightforward scientific reporting",
                    "Irony and satirical mock-praise",
                    "A statistical literature review",
                    "An objective legal contract"
                ],
                "correct_index": 1,
                "explanation": "The author employs sophisticated ironic praise to expose the absurdity of meritocratic myths."
            },
            {
                "id": "c2_r_as_2",
                "question": "What does the author satirize when writing: 'What a fortunate coincidence that merit... chose to incarnate exclusively within the sons of hereditary dukes'?",
                "options": [
                    "The genuine biological superiority of dukes",
                    "The false claim that the existing distribution of wealth is based on natural merit rather than inherited privilege",
                    "The architectural beauty of castles",
                    "The weather in London"
                ],
                "correct_index": 1,
                "explanation": "Highlights the statistical absurdity of claiming that talent conveniently matches inherited nobility."
            },
            {
                "id": "c2_r_as_3",
                "question": "In literary criticism, what is 'litotes'?",
                "options": [
                    "A deliberate ironic understatement using double negatives or understated phrasing",
                    "A loud theatrical shout",
                    "A poem written in Latin",
                    "A spelling mistake"
                ],
                "correct_index": 0,
                "explanation": "Litotes is an understatement in which an affirmative is expressed by negating its contrary (e.g. 'not bad' for great)."
            }
        ]
    },
    {
        "id": "curric_c2_listen_rapid_speech",
        "cefr_level": "C2",
        "module_type": "listening",
        "title": "Rapid Colloquial Speech, Jargon & Obscure Accents",
        "order_index": 4,
        "prerequisites": ["curric_c1_listen_synthesis"],
        "estimated_minutes": 55,
        "objectives": [
            "Decipher stream-of-consciousness natural speech delivered at high speed with regional phonological elisions",
            "Filter dense disciplinary jargon in spontaneous multi-party symposium cross-examinations",
            "Identify double negatives, ironies, and subtle conversational implicatures in fast dialogue"
        ],
        "explanation_markdown": """### Transcript-Based Listening Strategy: High-Speed Dialectal Exchanges
*(Practice session using authentic fast-paced debate scripts.)*

#### Audio Script: Parliamentary Committee Cross-Examination
```
CHAIR: Order! Mr Sterling, let's cut through the procedural obfuscation. You've sat before this committee 
for three hours waxing lyrical about fiduciary diligence, yet the forensic balance sheet tells an entirely 
different story. A four-million-pound tranche of capital vanished into an offshore shell entity within 
twelve hours of the bailout confirmation. 
MR STERLING: Look, with all due respect, Mr Chair, the committee's conflating structural liquidity with 
proprietary capital deployment. That capital wasn't 'siphoned'; it was hedged against impending currency volatility 
in our European derivatives portfolio.
CHAIR: Hedged, you say? Funny how that hedge conveniently vested into your private executive pension trust 
the very next morning. Do you take this committee for complete fools, or does your corporate chutzpah know no bounds?
```

#### Decoding High-Speed Dialectal Markers:
- **Idiomatic Thrusts:** *'cut through the procedural obfuscation'*, *'waxing lyrical'*, *'corporate chutzpah'*.
- **Euphemistic Camouflage:** *'proprietary capital deployment'* vs the Chair's plain reality: *'vanished into an offshore shell entity'*.
- **Rhetorical Interrogation:** *'Funny how that hedge conveniently vested...'* (Biting sarcastic dismissal of financial excuses).""",
        "examples": [
            {"text": "The Chair accuses Sterling of concealing embezzlement behind complex financial jargon.", "notes": "Deconstructing institutional obfuscation."},
            {"text": "Sterling euphemistically reframes capital flight as 'hedging against currency volatility'.", "notes": "Detecting rhetorical spin in spoken cross-examination."},
            {"text": "The Chair employs heavy sarcasm: 'Do you take this committee for complete fools...'", "notes": "Interpreting rhetorical indignation."}
        ],
        "guided_exercises": [
            {
                "id": "c2_l_ge_1",
                "prompt": "How much capital disappeared into the offshore entity?",
                "answer": "four million pounds",
                "explanation": "The Chair cites 'A four-million-pound tranche of capital'."
            },
            {
                "id": "c2_l_ge_2",
                "prompt": "What euphemistic financial term did Sterling use to explain the transfer?",
                "answer": "hedging / hedged against currency volatility",
                "explanation": "Sterling claimed it was 'hedged against impending currency volatility'."
            },
            {
                "id": "c2_l_ge_3",
                "prompt": "Where did the funds ultimately vest the following morning?",
                "answer": "his private executive pension trust",
                "explanation": "The Chair points out it vested into 'your private executive pension trust'."
            }
        ],
        "assessment": [
            {
                "id": "c2_l_as_1",
                "question": "What is the Chair's central accusation against Mr Sterling?",
                "options": [
                    "He spoke too quietly",
                    "He embezzled four million pounds of bailout money into his private pension while hiding behind financial jargon",
                    "He refused to invest in European currencies",
                    "He forgot to bring his balance sheet"
                ],
                "correct_index": 1,
                "explanation": "The Chair exposes that the so-called 'hedge' conveniently enriched Sterling's private pension trust."
            },
            {
                "id": "c2_l_as_2",
                "question": "What does the Yiddish-origin word 'chutzpah' mean in modern political English?",
                "options": [
                    "Supreme modesty and humility",
                    "Shameless audacity, impudence, or nerve",
                    "A legal document",
                    "Financial bankruptcy"
                ],
                "correct_index": 1,
                "explanation": "'Chutzpah' denotes audacious, shameless effrontery or nerve."
            },
            {
                "id": "c2_l_as_3",
                "question": "What does 'procedural obfuscation' mean in committee hearings?",
                "options": [
                    "Deliberately complicating legal rules to confuse and conceal the truth",
                    "Arriving early to a meeting",
                    "Providing clear financial evidence",
                    "Speaking French in Parliament"
                ],
                "correct_index": 0,
                "explanation": "Obfuscation is the deliberate act of making something obscure, unclear, or unintelligible."
            }
        ]
    },
    {
        "id": "curric_c2_write_mastery",
        "cefr_level": "C2",
        "module_type": "writing",
        "title": "Master Stylistics, Rhetorical Devices & Publication Prose",
        "order_index": 5,
        "prerequisites": ["curric_c1_write_counterarguments", "curric_c2_gram_subjunctive_ellipses"],
        "estimated_minutes": 60,
        "objectives": [
            "Deploy classical rhetorical figures (chiasmus, anaphora, tricolon, periodic sentence structures) with stylistic poise",
            "Command register modulation across scholarly monograph, legal draftsmanship, and high-literary journalism",
            "Produce Band 9 publication-grade prose demonstrating effortless syntactic rhythm and cadence"
        ],
        "explanation_markdown": """### The Architectural Ornaments of C2 Prose
To attain Band 9 in IELTS Task 2 or produce publication-grade writing, a writer commands stylistic figures that create memorable cadences:

#### 1. The Periodic Sentence (Delayed Syntax):
A periodic sentence withholds its main independent clause until the very end, creating dramatic cognitive suspension:
- *Standard (Loose):* Democratic institutions falter when citizens succumb to political apathy and polarization.
- **Periodic (C2 Mastery):** *When citizens succumb to ideological tribalism, when civic institutions are starved of fiscal nourishment, and when truth itself is subordinated to demagoguery—**it is then that democracy falters**.*

#### 2. Classical Figures of Speech:
- **Chiasmus (Syntactic Inversion):** Crossing sentence elements symmetrically:
  * *'We must not shape our tools merely to survive; we must ensure our tools do not reshape our humanity.'*
- **Anaphora (Rhythmic Repetition):** Repetition of opening phrases for rhetorical momentum:
  * *'It demands fiscal courage; it demands institutional transparency; it demands ethical resolve.'*
- **Tricolon (The Rule of Three):** Packaging arguments into triplets of escalating magnitude:
  * *'Liberty is not preserved by decrees, nor sustained by armies, but safeguarded in the conscious vigilance of free citizens.'*""",
        "examples": [
            {"text": "When truth is eclipsed by convenience, and justice subordinated to expediency, the moral architecture of the state collapses.", "notes": "Periodic sentence withholding the main clause until the end."},
            {"text": "We should not adapt humanity to technological imperatives; rather, we must bend technological tools to human flourishing.", "notes": "Chiasmic contrast."},
            {"text": "The policy was ill-conceived in its inception, chaotic in its execution, and disastrous in its culmination.", "notes": "Ascending tricolon (triplet of clauses)."}
        ],
        "guided_exercises": [
            {
                "id": "c2_w_ge_1",
                "prompt": "Identify the rhetorical device in: 'It was chaotic in its inception, flawed in its execution, and catastrophic in its conclusion.'",
                "answer": "Tricolon / Rule of Three",
                "explanation": "A series of three parallel words or phrases of increasing gravity is a tricolon."
            },
            {
                "id": "c2_w_ge_2",
                "prompt": "Construct a chiasmus: 'Never let a fool kiss you or a _____ fool you.'",
                "answer": "kiss",
                "explanation": "'kiss you / kiss fool you' forms a chiasmic A-B-B-A structure."
            },
            {
                "id": "c2_w_ge_3",
                "prompt": "What is a periodic sentence? (A sentence with its main point delayed until the end / A sentence with many commas)",
                "answer": "A sentence with its main point delayed until the end",
                "explanation": "Periodic sentences build suspension by placing the independent main clause at the end."
            }
        ],
        "assessment": [
            {
                "id": "c2_w_as_1",
                "question": "Which of the following represents a Band 9 publication-grade periodic sentence?",
                "options": [
                    "Democracy will fail if people don't vote because voting is good.",
                    "If the government ignores voters, and if voters stop caring, then the democracy dies.",
                    "Only when civic institutions are revitalized, when public discourse is liberated from partisan venality, and when economic equity is restored to working communities—only then will our democratic republic regain its vitality.",
                    "Voting is important and people should do it every year."
                ],
                "correct_index": 2,
                "explanation": "Delivers an ascending series of parallel dependent clauses before releasing the main proposition with commanding cadence."
            },
            {
                "id": "c2_w_as_2",
                "question": "What is the defining structural property of 'chiasmus' in classical rhetoric?",
                "options": [
                    "A symmetrical inversion of grammatical structures across parallel clauses (A-B $\\rightarrow$ B-A)",
                    "A spelling error in ancient Greek",
                    "A poem that doesn't rhyme",
                    "A paragraph with no verbs"
                ],
                "correct_index": 0,
                "explanation": "Chiasmus reverses concepts or syntactic structures symmetrically for powerful rhetorical impact."
            },
            {
                "id": "c2_w_as_3",
                "question": "How does rhythmic cadence influence an examiner's evaluation of Grammatical Range and Accuracy?",
                "options": [
                    "It has no impact whatsoever",
                    "It exhibits effortless stylistic flexibility, natural cohesion, and mastery of sentence variety characteristic of Band 9",
                    "It makes the essay look like a song",
                    "It guarantees that word count doesn't matter"
                ],
                "correct_index": 1,
                "explanation": "Band 9 descriptors explicitly demand full flexibility and precise use of a wide range of complex structures."
            }
        ]
    },
    {
        "id": "curric_c2_speak_spontaneous_discourse",
        "cefr_level": "C2",
        "module_type": "speaking",
        "title": "Spontaneous Discourse & Native-Like Idiom",
        "order_index": 6,
        "prerequisites": ["curric_c1_speak_nuance_hedging"],
        "estimated_minutes": 55,
        "objectives": [
            "Maintain effortless spoken discourse at native pace without perceptible lexical searching or cognitive pause",
            "Embed colloquial wit, erudite analogies, and situational humor with impeccable socio-pragmatic pitch",
            "Synthesize abstract socio-cultural dilemmas in IELTS Speaking Part 3 with oratorical ease"
        ],
        "explanation_markdown": """### The Benchmark of Spontaneous C2 Fluency
CEFR C2 and IELTS Band 9 Speaking are characterized by **effortless flow**. Pauses are strictly natural (breathing or dramatic emphasis), NEVER for searching for grammar or vocabulary:

#### Core Competencies:
1. **Analogy as an Argumentative Tool:**
   * Instead of listing dry statistics, C2 speakers deploy resonant analogies: *'Treating climate change solely through consumer carbon offsets is rather like arranging deckchairs on the Titanic—it gives an impression of purposeful industry while doing nothing to avert the iceberg.'*
2. **Socio-Pragmatic Pitch:**
   * Effortless switching between formal academic rhetoric and playful colloquial wit (*'That proposal is dead in the water'*, *'par for the course'*, *'a storm in a teacup'*).
3. **Conversational Agility:**
   * Answering abstract interrogations by reframing the question itself: *'That's a fascinating premise, though I'd question whether framing it as a binary choice between economic growth and environmental stewardship doesn't present a false dichotomy.'*""",
        "examples": [
            {"text": "Treating systemic inequality solely with corporate philanthropy is like applying a band-aid to a structural fracture.", "notes": "Powerful, vivid C2 argumentative analogy."},
            {"text": "Framing the debate as a zero-sum game between economic growth and ecological conservation presents an unhelpful false dichotomy.", "notes": "Intellectual reframing of examiner prompt."},
            {"text": "That legislative proposal was dead on arrival; it completely ignored regional constitutional sensitivities.", "notes": "Natural idiomatic register."}
        ],
        "guided_exercises": [
            {
                "id": "c2_sp_ge_1",
                "prompt": "Complete the analogy: 'Treating inflation solely by printing more currency is like trying to extinguish a fire with _____.' (water / gasoline)",
                "answer": "gasoline",
                "explanation": "Adding fuel to fire is the classical analogy for self-defeating interventions."
            },
            {
                "id": "c2_sp_ge_2",
                "prompt": "Which idiom describes an exaggerated fuss over an insignificant matter? (a storm in a teacup / a cold day in July)",
                "answer": "a storm in a teacup",
                "explanation": "'A storm in a teacup' denotes a disproportionate overreaction to a minor incident."
            },
            {
                "id": "c2_sp_ge_3",
                "prompt": "Reframe: 'Is money or happiness more important?'",
                "answer": "That presents a false dichotomy; financial security is a prerequisite for holistic happiness, not its adversary.",
                "explanation": "Reframes simplistic either/or options into an integrated reality."
            }
        ],
        "assessment": [
            {
                "id": "c2_sp_as_1",
                "question": "Which spoken turn in IELTS Speaking Part 3 exemplifies Band 9 spontaneous discourse?",
                "options": [
                    "Money is good. But happiness is also very good. So I like both.",
                    "That question poses an intriguing dilemma, though I would argue it constructs a false dichotomy. Financial solvency provides the baseline stability upon which human well-being rests; however, treating wealth accumulation as an end in itself yields diminishing emotional returns.",
                    "I want to make a lot of money because then I can be happy with cars.",
                    "Happiness cannot be bought in shops."
                ],
                "correct_index": 1,
                "explanation": "Seamlessly reframes false dichotomy, balances material solvency with diminishing returns, and speaks with effortless academic poise."
            },
            {
                "id": "c2_sp_as_2",
                "question": "What distinguishes natural C2 pause behavior from lower-band hesitation?",
                "options": [
                    "C2 speakers pause solely for dramatic effect or thought structuring, not to search for English vocabulary or syntax",
                    "C2 speakers never pause under any circumstances",
                    "C2 speakers speak at 500 words per minute",
                    "C2 speakers cough before answering"
                ],
                "correct_index": 0,
                "explanation": "Band 9 fluency descriptors state: 'Any hesitation is content-related rather than to find words or grammar'."
            },
            {
                "id": "c2_sp_as_3",
                "question": "What is the rhetorical benefit of using vivid analogies in speaking interviews?",
                "options": [
                    "It simplifies complex abstract concepts and demonstrates supreme lexical and conceptual command",
                    "It confuses the examiner",
                    "It proves the candidate knows stories about animals",
                    "It eliminates the need for grammar"
                ],
                "correct_index": 0,
                "explanation": "Metaphor and analogy transform dry intellectual points into memorable, lucid communicative turns."
            }
        ]
    },
    {
        "id": "curric_c2_pron_modulation",
        "cefr_level": "C2",
        "module_type": "pronunciation",
        "title": "Voice Modulation, Dramatic Pausing & Rhetorical Oratory",
        "order_index": 7,
        "prerequisites": ["curric_c1_pron_intonation"],
        "estimated_minutes": 55,
        "objectives": [
            "Modulate pitch, vocal tempo, and dynamic volume to command auditorium attention during public addresses",
            "Deploy strategic dramatic pauses (pregnant pauses) immediately prior to delivering pivotal thesis assertions",
            "Vary acoustic timbre to project warmth, moral authority, satirical skepticism, or intellectual detachment"
        ],
        "explanation_markdown": """### Suprasegmental Oratory & Voice Modulation
At the pinnacle of spoken English, pronunciation transcends phonetic accuracy to encompass **acoustic orchestration**:

#### 1. Dynamic Tempo Variation:
- **Accelerando (Speeding Up):** Used during descriptive build-ups, lists, or excitement to build narrative momentum.
- **Ritardando (Slowing Down):** Decelerating tempo dramatically on the core thesis statement forces the listener's cognitive focus onto every individual word:
  * *'And that... is why... the policy... failed.'*

#### 2. The Pregnant Pause:
Silence is a powerful acoustic instrument. A two-second pause placed:
- **Before an assertion:** Generates heightened anticipation.
- **After an assertion:** Grants the audience cognitive space to absorb the profound implication of the proposition.

#### 3. Pitch Register Modulation:
- High Pitch Register: Excitement, curiosity, rhetorical questioning.
- Low Pitch Register: Solemnity, authority, decisive finality.""",
        "examples": [
            {"text": "The speaker paused for two full seconds before uttering the final, devastating statistic.", "notes": "Strategic deployment of pregnant silence for dramatic gravity."},
            {"text": "Accelerating through the historical context, she abruptly slowed her cadence to emphasize the moral conclusion.", "notes": "Dynamic tempo variation (accelerando into ritardando)."},
            {"text": "Lowering his vocal pitch, he delivered the verdict with indisputable moral resonance.", "notes": "Pitch modulation to convey authority."}
        ],
        "guided_exercises": [
            {
                "id": "c2_p_ge_1",
                "prompt": "What effect does decelerating your speech tempo have on the listener? (Increases focus and gravity / Causes confusion)",
                "answer": "Increases focus and gravity",
                "explanation": "Slowing tempo signals to the listener that the upcoming words carry supreme importance."
            },
            {
                "id": "c2_p_ge_2",
                "prompt": "What is a 'pregnant pause' in public speaking? (A significant silence filled with meaning / Forgetting what to say)",
                "answer": "A significant silence filled with meaning",
                "explanation": "A pregnant pause is an intentional silence pregnant with anticipation and dramatic weight."
            },
            {
                "id": "c2_p_ge_3",
                "prompt": "Should your pitch stay at a flat, unvarying monotone level during an IELTS Part 3 discussion? (Yes / No)",
                "answer": "No",
                "explanation": "Monotone delivery is heavily penalized under the IELTS Pronunciation criteria."
            }
        ],
        "assessment": [
            {
                "id": "c2_p_as_1",
                "question": "How does deliberate silence (pausing) function as a rhetorical device in advanced spoken English?",
                "options": [
                    "It shows the candidate has fallen asleep",
                    "It frames pivotal claims, creates dramatic tension, and allows listeners to absorb complex conceptual propositions",
                    "It is penalized as an error in IELTS",
                    "It wastes examination time"
                ],
                "correct_index": 1,
                "explanation": "Purposeful pauses create dramatic emphasis and signal supreme oratorical self-assurance."
            },
            {
                "id": "c2_p_as_2",
                "question": "What does a flat, unvarying acoustic monotone signify under IELTS Pronunciation rubrics?",
                "options": [
                    "A Band 9 British accent",
                    "A severe defect in intonation and rhythm limiting the pronunciation score to Band 5 or 6",
                    "Extreme academic intelligence",
                    "Proper etiquette"
                ],
                "correct_index": 1,
                "explanation": "Rubrics require natural variation in pitch, rhythm, and intonation for higher bands."
            },
            {
                "id": "c2_p_as_3",
                "question": "How should an orator vocalize an ascending tricolon (a triplet of phrases)?",
                "options": [
                    "By getting quieter with every item",
                    "By elevating pitch, energy, or volume progressively with each of the three items",
                    "By whispering all three",
                    "By skipping the third phrase"
                ],
                "correct_index": 1,
                "explanation": "An ascending tricolon builds momentum by escalating acoustic prominence across the three parts."
            }
        ]
    },
    {
        "id": "curric_c2_func_keynote",
        "cefr_level": "C2",
        "module_type": "functional",
        "title": "High-Stakes Keynote Delivery & Hostile Q&A Handling",
        "order_index": 8,
        "prerequisites": ["curric_c1_func_negotiation"],
        "estimated_minutes": 55,
        "objectives": [
            "Deliver commanding keynote orations combining personal ethos, logos, and emotional pathos",
            "Field aggressive, hostile media interrogations and cross-examinations unflappably",
            "Deploy the 'Bridge' technique to deflect loaded questions back to core strategic messaging"
        ],
        "explanation_markdown": """### 1. High-Stakes Public Keynote Architecture
Delivering a global keynote requires synthesizing the classical Aristotelian triad:
- **Ethos (Credibility & Character):** *'Over twenty-five years in clinical oncology, I have witnessed both the agony of diagnostic delay and the miracle of early detection.'*
- **Logos (Intellectual Rigor & Data):** *'The longitudinal cohort data spanning seventy thousand patients confirms a forty-percent reduction in metastatic recurrence.'*
- **Pathos (Moral Urgency & Emotional Resonance):** *'Behind every single statistic sits a parent, a child, an irreplaceable life whose future hangs upon the wisdom of our decision today.'*

### 2. The 'Bridging' Technique for Hostile Q&A
When an adversarial journalist or critic asks a trap question (*'Isn't your technology just an overpriced boondoggle that failed its trials?'*):
1. **Acknowledge & Neutralize:** *'That question touches upon the rigorous regulatory scrutiny our phase-three trials underwent...'*
2. **The Verbal Bridge:** *'...and what those regulatory findings actually demonstrated was...' / '...what is essential to bear in mind is...'*
3. **Core Message:** *'...that efficacy was achieved in ninety-four percent of compliant cohorts.'*""",
        "examples": [
            {"text": "Behind every clinical metric stands a human life whose preservation demands our unwavering collective courage.", "notes": "Aristotelian pathos in keynote delivery."},
            {"text": "I welcome that question because it highlights the fundamental distinction between short-term capital volatility and long-term infrastructure value.", "notes": "Bridging technique in hostile Q&A."},
            {"text": "Let me address the premise of your interrogation directly, while correcting the statistical inaccuracy upon which it rests.", "notes": "Firm, poised executive pushback against loaded question."}
        ],
        "guided_exercises": [
            {
                "id": "c2_f_ge_1",
                "prompt": "Identify the rhetorical bridge: 'That is an important concern, and what our data fundamentally proves is...'",
                "answer": "and what our data fundamentally proves is",
                "explanation": "This phrase serves as the transitional bridge moving from the question to the core message."
            },
            {
                "id": "c2_f_ge_2",
                "prompt": "Which Aristotelian appeal relies on clinical statistics and longitudinal data? (Ethos / Logos / Pathos)",
                "answer": "Logos",
                "explanation": "Logos is the appeal to logic, evidence, and empirical reasoning."
            },
            {
                "id": "c2_f_ge_3",
                "prompt": "How should a CEO respond to a hostile shout from the audience? (Shout back / Respond with unshakeable calm and address the substantive point)",
                "answer": "Respond with unshakeable calm and address the substantive point",
                "explanation": "Unshakeable composure affirms executive authority and neutralizes hostility."
            }
        ],
        "assessment": [
            {
                "id": "c2_f_as_1",
                "question": "What is the primary objective of the 'Bridging' technique during hostile media interrogations?",
                "options": [
                    "To lie to the public",
                    "To acknowledge the topic professionally while seamlessly redirecting the narrative back to substantiated key messages",
                    "To run off the stage",
                    "To insult the journalist"
                ],
                "correct_index": 1,
                "explanation": "Bridging prevents defensive traps and pivots the focus back to positive strategic realities."
            },
            {
                "id": "c2_f_as_2",
                "question": "Which combination of elements defines an exceptional, historic keynote address?",
                "options": [
                    "Reading a PowerPoint presentation word-for-word in monotone",
                    "Harmonizing personal credibility (Ethos), rigorous evidence (Logos), and moral resonance (Pathos)",
                    "Speaking for four hours without breaks",
                    "Showing complex mathematical formulas only"
                ],
                "correct_index": 1,
                "explanation": "Classical rhetoric unites Ethos, Logos, and Pathos to achieve persuasive impact."
            },
            {
                "id": "c2_f_as_3",
                "question": "How should an executive dismantle a loaded premise in an interrogation (e.g., 'When will you stop polluting rivers?')?",
                "options": [
                    "By accepting the false premise",
                    "By calmly identifying and rejecting the false premise before articulating documented environmental compliance",
                    "By refusing to answer entirely",
                    "By crying"
                ],
                "correct_index": 1,
                "explanation": "A loaded question's false premise must be dismantled calmly and explicitly."
            }
        ]
    },
    {
        "id": "curric_c2_review_milestone",
        "cefr_level": "C2",
        "module_type": "review",
        "title": "C2 Master Capstone Examination & Proficiency Certification",
        "order_index": 9,
        "prerequisites": ["curric_c2_gram_subjunctive_ellipses", "curric_c2_write_mastery"],
        "estimated_minutes": 65,
        "objectives": [
            "Demonstrate complete bilingual/native-level English proficiency across all syntactic, lexical, phonological, and pragmatic domains",
            "Attain certification for IELTS Band 8.5–9.0 performance across Academic and General Training specifications",
            "Synthesize mandative subjunctives, classical rhetorical devices, subtext dissection, and keynote oratory"
        ],
        "explanation_markdown": """### C2 Master Capstone Evaluation
Attaining CEFR C2 Proficiency is the ultimate milestone in English language education. It certifies that the learner possesses:
1. **Flawless Syntactic Command:** Effortless deployment of mandative subjunctives (*demand that he submit*), absolute clauses, and stylistic ellipsis.
2. **Lexical Erudition:** Natural command of conceptual metaphors, classical idioms (*Pyrrhic victory, Gordian knot*), and subtle connotative nuance.
3. **Hermeneutic Acuity:** Deciphering dense satire, ironic litotes, and complex philosophical treatises.
4. **Master Oratory & Rhetoric:** Commanding rhythmic periodic sentences, chiasmic balance, and unshakeable public presence.

Complete this master capstone assessment to earn your official Band 9.0 Master Certification.""",
        "examples": [
            {"text": "The international convention mandates that every sovereign entity submit comprehensive emissions registries annually.", "notes": "Mandative subjunctive with flawless formal concord."},
            {"text": "What was heralded as an economic triumph proved, in retrospective analysis, a devastating Pyrrhic victory.", "notes": "Clefting and classical idiom."},
            {"text": "Only when ethical wisdom guides technological capability—only then can human society claim genuine advancement.", "notes": "Periodic sentence with restrictive inversion."}
        ],
        "guided_exercises": [
            {
                "id": "c2_rev_ge_1",
                "prompt": "Apply the mandative subjunctive: 'The charter stipulates that each member state _____ (contribute) ten percent.'",
                "answer": "contribute",
                "explanation": "Mandative subjunctive uses base verb 'contribute'."
            },
            {
                "id": "c2_rev_ge_2",
                "prompt": "What classical idiom signifies an irrevocable, decisive step committing oneself to hazard? (Crossing the _____)",
                "answer": "Rubicon",
                "explanation": "Crossing the Rubicon."
            },
            {
                "id": "c2_rev_ge_3",
                "prompt": "Identify the literary figure: 'Ask not what your country can do for you; ask what you can do for your country.'",
                "answer": "Chiasmus",
                "explanation": "A-B (country for you) / B-A (you for country) forms a classical chiasmus."
            }
        ],
        "assessment": [
            {
                "id": "c2_rev_as_1",
                "question": "Which sentence demonstrates 100% flawless C2 mandative subjunctive and stylistic mastery?",
                "options": [
                    "The senate mandated that the governor resigns his office immediately.",
                    "The senate mandated that the governor resign his office immediately, all legal avenues having been exhausted.",
                    "The senate mandated that the governor will resign, and he did it.",
                    "The senate mandated the governor to resigning his office."
                ],
                "correct_index": 1,
                "explanation": "'mandated that the governor resign' (mandative subjunctive base verb) + 'all legal avenues having been exhausted' (absolute clause)."
            },
            {
                "id": "c2_rev_as_2",
                "question": "In literary and philosophical prose, what is the effect of combining litotes with satirical mock-flattery?",
                "options": [
                    "It creates a scathing, multi-layered critique that exposes hypocrisy without resorting to crude polemics",
                    "It makes the text impossible to understand",
                    "It means the author is complimenting their opponents",
                    "It is forbidden in academic journals"
                ],
                "correct_index": 0,
                "explanation": "Litotes and mock-flattery produce subtle, devastating satirical irony characteristic of master C2 prose."
            },
            {
                "id": "c2_rev_as_3",
                "question": "What is the defining mark of an IELTS Band 9 candidate in Speaking and Writing?",
                "options": [
                    "Using only long words found in the dictionary",
                    "Effortless, natural precision, sophisticated stylistic flexibility, nuanced dialectical reasoning, and complete absence of mechanical strain",
                    "Speaking with an exaggerated aristocratic accent",
                    "Writing 5,000 words in 40 minutes"
                ],
                "correct_index": 1,
                "explanation": "Band 9 descriptors explicitly demand full flexibility, effortless naturalness, and comprehensive stylistic command."
            }
        ]
    }
]

with open("content/curriculum/c1.json", "w", encoding="utf-8") as f:
    json.dump(C1_LESSONS, f, indent=2, ensure_ascii=False)
print("Saved C1:", len(C1_LESSONS), "lessons.")

with open("content/curriculum/c2.json", "w", encoding="utf-8") as f:
    json.dump(C2_LESSONS, f, indent=2, ensure_ascii=False)
print("Saved C2:", len(C2_LESSONS), "lessons.")
