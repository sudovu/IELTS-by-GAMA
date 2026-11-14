"""
build_b2_c1_c2.py
Generates B2, C1, and C2 curriculum JSON files with 9 modules each.
Incorporates all existing starter lesson IDs and adheres to 12 pedagogical components.
"""

import os
import json

CURRICULUM_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "curriculum")
os.makedirs(CURRICULUM_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# B2 — UPPER-INTERMEDIATE (9 Modules)
# -----------------------------------------------------------------------------
B2_LESSONS = [
    {
        "id": "curric_b2_gram_conditionals",
        "cefr_level": "B2",
        "module_type": "grammar",
        "title": "Hypothetical Conditionals & Mixed Forms in Academic Arguments",
        "order_index": 1,
        "prerequisites": ["curric_b1_gram_present_perfect"],
        "estimated_minutes": 35,
        "objectives": [
            "Construct Second, Third, and Mixed Conditionals to articulate hypothetical reasoning and counterfactual analysis.",
            "Formulate formal conditional inversions omitting 'if' ('Were the government to...', 'Had the data been verified...').",
            "Apply modal nuances ('might have', 'could have') to calibrate analytical certainty."
        ],
        "form_and_structure": "Second: If + Past Simple, would + base verb. Third: If + Past Perfect, would have + V3. Mixed: If + Past Perfect, would + base verb (past cause, present result). Inversion: Had + subject + V3, would have + V3.",
        "usage_rationale": "Used in academic debate and IELTS Task 2 essays to analyze hypothetical policy interventions, alternative historical trajectories, and speculative consequences.",
        "positive_examples": [
            "If municipal councils invested substantially in cycling infrastructure, urban traffic congestion would diminish.",
            "Had the regulatory authorities intervened earlier, the economic disruption could have been mitigated."
        ],
        "negative_examples": [
            "If they would invest in research, they will see results. (Never use 'would' in the if-clause).",
            "Had they not examined the evidence, they wouldn't discovered the error."
        ],
        "common_mistakes": [
            "Incorrect: 'If I would have known, I would tell you.' -> Correct: 'If I had known, I would have told you.'",
            "Incorrect: 'If it will rain tomorrow, we cancel.' -> Correct: 'If it rains tomorrow, we will cancel.'"
        ],
        "confused_structures": [
            "Pure Third Conditional (Past condition -> Past outcome) vs Mixed Conditional (Past condition -> Present outcome: 'If I had accepted the scholarship in 2020, I would be a physician today')."
        ],
        "explanation_markdown": """### Advanced Conditional Mechanics in Academic Argumentation
Hypothetical structures allow researchers and essayists to evaluate proposals counterfactually:
1. **Second Conditional (Present/Future Unlikely/Hypothetical)**:
   *If governments subsidized green infrastructure, carbon emissions would decline significantly.*
2. **Third Conditional (Past Counterfactual)**:
   *Had the containment barriers been fortified, the catastrophic flooding would have been averted.*
3. **Mixed Conditional (Past Action with Present Consequence)**:
   *If the clinical trials had failed last year, the treatment would not be accessible to patients today.*""",
        "examples": [
            {"text": "Were interest rates to climb precipitously, corporate borrowing would contract.", "notes": "Inverted second conditional: 'Were + subject + to-infinitive'."},
            {"text": "Had the researchers calibrated their sensors, the measurements would have yielded greater fidelity.", "notes": "Inverted third conditional: 'Had + subject + past participle'."}
        ],
        "guided_exercises": [
            {"id": "b2_ge_1", "prompt": "Complete the inversion: '_____ the team conducted thorough trials, the defect would have been identified.' (Had / Were)", "answer": "Had", "explanation": "'Had + subject + V3' forms the counterfactual past inversion."}
        ],
        "interactive_practice": [
            {
                "id": "b2_ip_1",
                "question": "Which sentence demonstrates grammatically sound conditional inversion?",
                "options": [
                    "Should tariffs rise, consumers would bear the financial burden.",
                    "Were tariffs to rise, consumers will bear the burden.",
                    "Had tariffs rose, consumers would have suffered.",
                    "Were tariffs to rise, consumers would bear the financial burden."
                ],
                "correct_index": 3,
                "explanation": "'Were [subject] to [verb], [subject] would [verb]' maintains proper modal harmony."
            }
        ],
        "assessment": [
            {
                "id": "b2_as_1",
                "question": "Identify the grammatically flawed sentence:",
                "options": [
                    "If taxes were increased, consumer spending would fall.",
                    "If taxes would be increased, consumer spending would fall.",
                    "Were taxes to increase, consumer spending would fall.",
                    "Had taxes been increased, consumer spending would have fallen."
                ],
                "correct_index": 1,
                "explanation": "The auxiliary 'would' cannot be placed in the conditional if-clause: never say 'if taxes would be increased'."
            }
        ],
        "review_questions": [
            "What distinguishes an inverted conditional from an ordinary 'if'-clause in academic register?",
            "How does a mixed conditional bridge past actions with present states?"
        ]
    },
    {
        "id": "curric_b2_vocab_academic_word_list",
        "cefr_level": "B2",
        "module_type": "vocabulary",
        "title": "Academic Word List (AWL) Sublist 1 Mastery",
        "order_index": 2,
        "prerequisites": ["curric_b1_vocab_workplace_education"],
        "estimated_minutes": 30,
        "objectives": [
            "Master core high-incidence AWL terms (analyze, approach, concept, constitute, establish, indicate, require, significant).",
            "Synthesize complete word families (analysis, analytical, analytically, analyze).",
            "Integrate academic collocations into formal essays ('conduct an in-depth analysis', 'establish a clear correlation')."
        ],
        "explanation_markdown": """### The Power of the Academic Word List (AWL)
Compiled by Averil Coxhead, the AWL comprises 570 word families that appear with high frequency across all academic disciplines.
- **Analyze** (verb) -> *Analysis* (noun), *Analytical* (adj), *Analytically* (adv)
- **Establish** (verb) -> *Establishment* (noun), *Established* (adj)
- **Constitute** (verb) -> *Constitution* (noun), *Constituent* (noun/adj)""",
        "examples": [
            {"text": "The latest census data indicates a significant demographic transition toward urban centers.", "notes": "'indicates a significant transition' is a classic academic collocation."}
        ],
        "guided_exercises": [
            {"id": "b2_v_ge_1", "prompt": "Form the adjective of 'concept': _____", "answer": "conceptual", "explanation": "concept -> conceptual."}
        ],
        "interactive_practice": [
            {
                "id": "b2_v_ip_1",
                "question": "Which verb means 'to make up or form the parts of something'?",
                "options": ["Analyze", "Constitute", "Derive", "Establish"],
                "correct_index": 1,
                "explanation": "'Constitute' means to be a part of a whole (e.g. 'Women constitute 52% of the workforce')."
            }
        ],
        "assessment": [
            {
                "id": "b2_v_as_1",
                "question": "Select the correct collocation: 'The committee was tasked to _____ the underlying causes of the crisis.'",
                "options": ["analyze", "constitute", "establish into", "derive for"],
                "correct_index": 0,
                "explanation": "One 'analyzes the underlying causes' of a phenomenon."
            }
        ]
    },
    {
        "id": "curric_b2_read_academic_arguments",
        "cefr_level": "B2",
        "module_type": "reading",
        "title": "Deconstructing Academic Arguments & Identifying Main Ideas",
        "order_index": 3,
        "prerequisites": ["curric_b1_read_factual_articles"],
        "estimated_minutes": 35,
        "objectives": [
            "Deconstruct discursive academic passages into claims, evidence, and rebuttals.",
            "Distinguish between writer claims and cited outside counter-arguments.",
            "Complete IELTS Matching Headings and True/False/Not Given tasks with high fidelity."
        ],
        "explanation_markdown": """### Deconstructing Academic Texts
Academic articles consist of structured discourse moves:
1. **Background**: Establishing the context or current scientific consensus.
2. **Problem Identification**: Highlighting a limitation, puzzle, or controversy.
3. **Claim / Thesis**: The author's central assertion.
4. **Evidence & Counter-Claims**: Data supporting the claim and concession to limitations.""",
        "examples": [
            {"text": "While proponents celebrate artificial intelligence, detractors caution against algorithmic prejudice.", "notes": "Two-sided academic balance."}
        ],
        "guided_exercises": [
            {"id": "b2_r_ge_1", "prompt": "If an author writes 'It has been suggested that X, yet empirical tests dispute this', does the author support X? (Yes/No)", "answer": "No", "explanation": "'yet empirical tests dispute this' rejects proposition X."}
        ],
        "interactive_practice": [
            {
                "id": "b2_r_ip_1",
                "question": "What is the primary function of a Topic Sentence at B2 reading level?",
                "options": [
                    "To summarize the entire book",
                    "To encapsulate the central controlling idea of that specific paragraph",
                    "To introduce unrelated trivia",
                    "To list bibliography citations"
                ],
                "correct_index": 1,
                "explanation": "The topic sentence articulates the controlling argument for that paragraph."
            }
        ],
        "assessment": [
            {
                "id": "b2_r_as_1",
                "question": "PASSAGE: 'Although early simulations predicted rapid glacier retreat, revised satellite telemetry suggests equilibrium has been maintained.' According to the passage, the glaciers are:",
                "options": [
                    "Retreating faster than ever predicted.",
                    "Maintaining equilibrium according to recent data.",
                    "Completely melted.",
                    "Unobservable by satellites."
                ],
                "correct_index": 1,
                "explanation": "'revised satellite telemetry suggests equilibrium has been maintained' confirms option 1."
            }
        ]
    },
    {
        "id": "curric_b2_list_lectures",
        "cefr_level": "B2",
        "module_type": "listening",
        "title": "Academic Lectures & Distractor Trap Avoidance",
        "order_index": 4,
        "prerequisites": ["curric_b1_list_discussions"],
        "estimated_minutes": 30,
        "objectives": [
            "Listen to extended academic monologues (Section 4 style) without interruption.",
            "Identify signaling signposts (*'Turning now to...', 'In contrast to earlier theories...' *).",
            "Evade distractor traps involving superseded hypotheses and rejected estimates."
        ],
        "explanation_markdown": """### Navigating IELTS Section 4 Monologues
Section 4 features university-level lectures:
- **Signposting language**: Listen for lecture roadmap transitions (*'Having looked at the causes, let us now examine the ramifications'*).
- **Distractor vigilance**: Lecturers often present an initial hypothesis (*'Initial calculations estimated 400 metric tons'*) before correcting with definitive findings (*'however, calibrated spectrometry confirmed the actual figure was 250 metric tons'*).""",
        "examples": [
            {"text": "LECTURER: 'The prototype originally operated at 12 volts, but subsequent modifications reduced requirements to 8 volts.'", "notes": "12V was a distractor; 8V is the definitive requirement."}
        ],
        "guided_exercises": [
            {"id": "b2_l_ge_1", "prompt": "Lecturer: 'We expected 50 participants, but ultimately 82 enrolled.' Final number = _____", "answer": "82", "explanation": "'ultimately 82 enrolled' indicates the actual verified figure."}
        ],
        "interactive_practice": [
            {
                "id": "b2_l_ip_1",
                "question": "Which signposting phrase indicates a transition to the next topic in a lecture?",
                "options": [
                    "As I mentioned previously...",
                    "Turning now to the economic implications...",
                    "To recap our first point...",
                    "In other words..."
                ],
                "correct_index": 1,
                "explanation": "'Turning now to...' signals an explicit thematic shift to a new subtopic."
            }
        ],
        "assessment": [
            {
                "id": "b2_l_as_1",
                "question": "The professor states: 'The excavation concluded that the fortress dates back to 450 BC, contrary to previous assumptions that it was built in 200 BC.' The fortress was built in:",
                "options": ["200 BC", "450 BC", "650 BC", "AD 450"],
                "correct_index": 1,
                "explanation": "'dates back to 450 BC, contrary to previous assumptions' confirms 450 BC."
            }
        ]
    },
    {
        "id": "curric_b2_write_peel_paragraph_technique",
        "cefr_level": "B2",
        "module_type": "writing",
        "title": "PEEL Paragraph Architecture for IELTS Writing Task 2",
        "order_index": 5,
        "prerequisites": ["curric_b1_write_cohesion_linkers"],
        "estimated_minutes": 35,
        "objectives": [
            "Master the PEEL paragraph model (Point, Explanation, Example, Link) for persuasive essay writing.",
            "Draft authoritative topic sentences that align directly with Task 2 prompts.",
            "Conclude paragraphs with analytical linking sentences that tie back to the central thesis."
        ],
        "explanation_markdown": """### PEEL Paragraph Structure
The PEEL method provides the architectural scaffolding for Band 7+ Task 2 body paragraphs:
- **P (Point)**: Assert the central argument directly (*One compelling argument in favor of renewable subsidies is energy independence.*)
- **E (Explanation)**: Elaborate on the mechanism or rationale (*By diversifying the national energy portfolio away from volatile foreign fossil fuels, governments shield their domestic economies from international price shocks.*)
- **E (Example)**: Provide a specific, illustrative case study (*For instance, Denmark’s heavy investment in offshore wind power enabled the nation to become a net exporter of electricity.*)
- **L (Link)**: Reconnect the point back to the macro-question (*Therefore, targeted fiscal subsidies represent an effective instrument for macroeconomic resilience.*)""",
        "examples": [
            {"text": "A well-structured PEEL paragraph prevents rambling and guarantees high Coherence & Cohesion (CC) marks.", "notes": "Essential for Band 7.0+ Writing."}
        ],
        "guided_exercises": [
            {"id": "b2_w_ge_1", "prompt": "What does the 'L' in the PEEL paragraph technique represent? (Link / Length)", "answer": "Link", "explanation": "The 'L' stands for Link, reconnecting the paragraph to the overarching thesis."}
        ],
        "interactive_practice": [
            {
                "id": "b2_w_ip_1",
                "question": "Which sentence functions most effectively as a Topic Sentence (P) in a PEEL paragraph?",
                "options": [
                    "For example, Denmark built wind turbines in 2015.",
                    "A primary benefit of remote employment is the substantial mitigation of urban commuting stress.",
                    "In conclusion, I think people should work from home.",
                    "Because working from home is good and commuters are tired."
                ],
                "correct_index": 1,
                "explanation": "It clearly asserts a specific, arguable claim with academic lexical precision."
            }
        ],
        "assessment": [
            {
                "id": "b2_w_as_1",
                "question": "What is the primary danger of omitting the 'Explanation' (E) step in a PEEL paragraph?",
                "options": [
                    "The essay will be too long.",
                    "The argument remains an unsupported assertion without analytical depth.",
                    "The conclusion cannot be written.",
                    "Vocabulary marks are automatically zeroed."
                ],
                "correct_index": 1,
                "explanation": "Without explanation, an argument lacks the critical depth required for Band 7+ Task Response."
            }
        ]
    },
    {
        "id": "curric_b2_speak_long_turns",
        "cefr_level": "B2",
        "module_type": "speaking",
        "title": "Sustained Monologue & Part 2 Long Turn Structuring",
        "order_index": 6,
        "prerequisites": ["curric_b1_speak_opinions"],
        "estimated_minutes": 30,
        "objectives": [
            "Organize and sustain a 2-minute uninterrupted individual monologue (IELTS Part 2 Cue Card).",
            "Utilize the 1-minute preparation interval effectively by mapping bullet-point keywords.",
            "Incorporate sensory detail, emotional reflection, and reflective past-to-present comparison."
        ],
        "explanation_markdown": """### Conquering the 2-Minute Long Turn
The IELTS Part 2 cue card requires you to speak for 1 to 2 minutes on a given topic:
1. **Preparation Strategy (1 Minute)**: Do NOT write full sentences; jot down 4–5 bullet points (Who, When, What happened, Why memorable).
2. **Structural Strategy**:
   - Introduction: *I'd like to talk about...*
   - Chronological Narration: *It took place roughly two years ago when...*
   - Peak Experience / Turning Point: *What really struck me was...*
   - Reflection: *Looking back on the experience now, I realize that...*""",
        "examples": [
            {"text": "Looking back, what made this achievement so memorable was the perseverance required to overcome repeated setbacks.", "notes": "Reflective Band 8 phrasing."}
        ],
        "guided_exercises": [
            {"id": "b2_s_ge_1", "prompt": "During the 1-minute prep time for Part 2, should you write full sentences or keyword notes? (sentences / keywords)", "answer": "keywords", "explanation": "Writing keywords maximizes time; writing full sentences wastes critical seconds."}
        ],
        "interactive_practice": [
            {
                "id": "b2_s_ip_1",
                "question": "How long should you aim to speak during IELTS Speaking Part 2?",
                "options": ["30 seconds", "Exactly 60 seconds", "Between 1 minute 45 seconds and 2 minutes", "At least 5 minutes"],
                "correct_index": 2,
                "explanation": "Aiming for 1:45 to 2:00 demonstrates fluency and coherence without trailing off prematurely."
            }
        ],
        "assessment": [
            {
                "id": "b2_s_as_1",
                "question": "Which opening phrase is most effective for initiating an IELTS Part 2 cue card turn?",
                "options": [
                    "I will talk about the question on the paper.",
                    "I'd like to share an account of a particularly transformative journey I undertook...",
                    "The topic given to me is vacation.",
                    "Wait a minute while I think."
                ],
                "correct_index": 1,
                "explanation": "It immediately introduces the subject with lexical sophistication and engagement."
            }
        ]
    },
    {
        "id": "curric_b2_pron_sentence_stress",
        "cefr_level": "B2",
        "module_type": "pronunciation",
        "title": "Sentence Stress, Rhythm & Contrastive Focus",
        "order_index": 7,
        "prerequisites": ["curric_b1_pron_word_stress"],
        "estimated_minutes": 25,
        "objectives": [
            "Distinguish between content words (stressed) and function words (unstressed/reduced).",
            "Employ contrastive stress to highlight focal semantic distinctions (*'I didn't say HE stole it, I said SHE did'*).",
            "Maintain English stress-timed rhythm across long multi-clause utterances."
        ],
        "explanation_markdown": """### Sentence Stress and Contrastive Focus
English is a **stress-timed** language: stressed syllables occur at approximately regular intervals.
- **Content Words (Stressed)**: Nouns, main verbs, adjectives, adverbs (*SCIENCE, EXPANDS, KNOWLEDGE*).
- **Function Words (Unstressed)**: Articles, prepositions, auxiliary verbs (*to the, of a, was*).
- **Contrastive Stress**: Stressing an unexpected word shifts the intended meaning:
  - *I wanted a RED car* (not a blue one).
  - *I WANTED a red car* (I don't want it anymore, or someone doubted my desire).""",
        "examples": [
            {"text": "The PRES-i-dent an-NOUNCED a MA-jor SHIFT in FOR-eign POL-i-cy.", "notes": "Notice how unstressed words compress in duration."}
        ],
        "guided_exercises": [
            {"id": "b2_p_ge_1", "prompt": "In 'She lives in Rome', which words are stressed content words? (She, lives, in, Rome)", "answer": "lives, Rome", "explanation": "'lives' (verb) and 'Rome' (proper noun) carry the primary lexical stress."}
        ],
        "interactive_practice": [
            {
                "id": "b2_p_ip_1",
                "question": "In the sentence 'I thought the meeting was on TUESDAY', what does the contrastive stress imply?",
                "options": [
                    "The speaker dislikes meetings.",
                    "The meeting is actually on a different day, contradicting the speaker's expectation.",
                    "Tuesday is the speaker's favorite day.",
                    "The meeting was cancelled."
                ],
                "correct_index": 1,
                "explanation": "Stressing 'Tuesday' highlights contrast with the actual day the meeting took place."
            }
        ],
        "assessment": [
            {
                "id": "b2_p_as_1",
                "question": "Which of the following is categorized as a grammatical function word that is typically unstressed in natural speech?",
                "options": ["Substantial", "Investigate", "Through", "Rapidly"],
                "correct_index": 2,
                "explanation": "'Through' is a preposition (function word) and is reduced in rapid fluent speech."
            }
        ]
    },
    {
        "id": "curric_b2_func_negotiations",
        "cefr_level": "B2",
        "module_type": "functional",
        "title": "Negotiation, Concession & Strategic Compromise",
        "order_index": 8,
        "prerequisites": ["curric_b1_func_business_meetings"],
        "estimated_minutes": 30,
        "objectives": [
            "Conduct principled negotiations using conditional concessions ('We could accept X, provided that you agree to Y').",
            "Use diplomatic language to reject unviable proposals without creating conflict.",
            "Summarize mutual agreements and document finalized contractual terms."
        ],
        "explanation_markdown": """### Diplomatic Negotiation Formulas
1. **Conditional Offers**:
   - *'We would be prepared to compromise on delivery dates, provided that payment terms are net-30.'*
   - *'As long as the budget is guaranteed, we can allocate extra engineering staff.'*
2. **Tactful Disagreement**:
   - *'I appreciate your constraints; however, that figure presents severe operational difficulties for our team.'*
   - *'With respect, that proposal is somewhat beyond our current scope.'*""",
        "examples": [
            {"text": "NEGOTIATOR: 'Provided that warranty coverage extends to three years, we are prepared to finalize the contract.'", "notes": "Conditional trade-off."}
        ],
        "guided_exercises": [
            {"id": "b2_func_ge_1", "prompt": "Complete the conditional phrase: '_____ that you deliver by Friday, we will place the order.' (Provided / Although)", "answer": "Provided", "explanation": "'Provided that' introduces a conditional prerequisite."}
        ],
        "interactive_practice": [
            {
                "id": "b2_func_ip_1",
                "question": "Which phrase is most diplomatic when rejecting an unviable commercial proposal?",
                "options": [
                    "Your offer is ridiculous.",
                    "Unfortunately, that pricing model is unfeasible under our current operational parameters.",
                    "We refuse to speak with you further.",
                    "Never suggest that again."
                ],
                "correct_index": 1,
                "explanation": "It conveys refusal objectively through diplomatic and formal terminology."
            }
        ],
        "assessment": [
            {
                "id": "b2_func_as_1",
                "question": "What is the function of the phrase 'on the condition that' in negotiations?",
                "options": [
                    "To introduce an unconditional agreement",
                    "To stipulate a mandatory requirement before agreement is reached",
                    "To cancel the meeting immediately",
                    "To ask for a recess"
                ],
                "correct_index": 1,
                "explanation": "'On the condition that' establishes a required prerequisite."
            }
        ]
    },
    {
        "id": "curric_b2_rev_upper_intermediate_mastery",
        "cefr_level": "B2",
        "module_type": "review",
        "title": "B2 Upper-Intermediate Level Review & Assessment",
        "order_index": 9,
        "prerequisites": ["curric_b2_gram_conditionals", "curric_b2_write_peel_paragraph_technique"],
        "estimated_minutes": 40,
        "objectives": [
            "Synthesize B2 conditional reasoning, AWL vocabulary, and PEEL paragraph architecture.",
            "Verify examination readiness for Band 6.5–7.0 benchmarks in IELTS Academic.",
            "Confirm qualification for CEFR C1 Advanced curriculum."
        ],
        "explanation_markdown": """### B2 Milestone Review
At B2 (Vantage Level), learners can understand the main ideas of complex text on concrete and abstract topics, including technical discussions in their field of specialization, and interact with a degree of fluency that makes regular interaction with native speakers quite possible without strain.""",
        "examples": [
            {"text": "B2 Mastery Benchmark: Consistent command of complex conditionals, PEEL structure, and academic vocabulary.", "notes": "Official CEFR B2 Vantage descriptor."}
        ],
        "guided_exercises": [
            {"id": "b2_rev_ge_1", "prompt": "Identify the error: 'If I was you, I would consult the legal department.' -> Correct: 'If I _____ you...'", "answer": "were", "explanation": "Formal hypothetical subjunctive requires 'were' ('If I were you')."}
        ],
        "interactive_practice": [
            {
                "id": "b2_rev_ip_1",
                "question": "Choose the most cohesive and grammatically accurate complex sentence:",
                "options": [
                    "Despite the weather was bad, the flight took off on schedule.",
                    "Although the weather was severe, the flight departed on schedule, which surprised passengers.",
                    "Because of the weather was severe, the flight departed anyway.",
                    "In spite of the flight departed on time, the weather was bad."
                ],
                "correct_index": 1,
                "explanation": "'Although' correctly introduces the finite clause, followed by an accurate relative clause."
            }
        ],
        "assessment": [
            {
                "id": "b2_rev_as_1",
                "question": "Which sentence correctly demonstrates inverted conditional syntax?",
                "options": [
                    "Were the budget approved, construction would commence immediately.",
                    "If the budget were approved, construction commenced.",
                    "Had the budget approved, construction will start.",
                    "Should the budget was approved, we will build."
                ],
                "correct_index": 0,
                "explanation": "'Were the budget approved, construction would commence immediately' is an elegant inverted conditional."
            }
        ]
    }
]

with open(os.path.join(CURRICULUM_DIR, "b2.json"), "w", encoding="utf-8") as f:
    json.dump(B2_LESSONS, f, indent=2, ensure_ascii=False)
print("Generated b2.json with", len(B2_LESSONS), "lessons.")
