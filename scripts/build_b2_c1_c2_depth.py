# -*- coding: utf-8 -*-
"""
Deep Comprehensive Curriculum Builder for B2, C1, C2 (Phase 13).
Preserves all 27 existing lesson IDs across B2, C1, and C2 with rich educational depth.
"""

import json

# -------------------------------------------------------------
# B2 UPPER INTERMEDIATE (9 Lessons)
# -------------------------------------------------------------
B2_LESSONS = [
    {
        "id": "curric_b2_gram_conditionals",
        "cefr_level": "B2",
        "module_type": "grammar",
        "title": "Conditionals: Real, Unreal & Mixed Conditions",
        "order_index": 1,
        "prerequisites": ["curric_b1_gram_present_perfect"],
        "estimated_minutes": 50,
        "objectives": [
            "Construct Second Conditionals (hypothetical present/future) and Third Conditionals (hypothetical past)",
            "Formulate Mixed Conditionals connecting past actions to ongoing present consequences",
            "Deploy conditional inversions ('Had I known...', 'Were they to agree...') for formal academic register",
            "Eliminate 'would have' in the if-clause and avoid punctuation errors in conditional syntax"
        ],
        "explanation_markdown": """### 1. Second & Third Conditionals
- **Second Conditional (Hypothetical / Unreal Present or Future):**
  * Formula: *If + Past Simple, would/could/might + Base Verb.*
  * Example: *If governments subsidized clean energy, carbon emissions would plummet.* (Note: Use 'were' for all persons in formal English: *If I were you...*).
- **Third Conditional (Unreal Past / Regrets / Historical Alternatives):**
  * Formula: *If + Past Perfect, would/could/might + have + Past Participle.*
  * Example: *If the engineers had identified the micro-fracture earlier, the bridge would not have collapsed.*

### 2. Mixed Conditionals (Cross-Time Boundaries)
1. **Past Action $\\rightarrow$ Present Result:**
   * Formula: *If + Past Perfect (past condition), would + Base Verb (present result).*
   * Example: *If I had accepted that overseas scholarship in 2022, I would be working in Zurich today.*
2. **Present State $\\rightarrow$ Past Result:**
   * Formula: *If + Past Simple (enduring condition), would have + Past Participle (past result).*
   * Example: *If she were not so terrified of public speaking, she would have applied for the keynote role last month.*

### 3. Formal Inverted Conditionals (Band 8+ Stylistics):
- Omit 'if' and invert subject with auxiliary:
  * *If I had known...* $\\rightarrow$ **Had I known** the risks, I would have intervened.
  * *If they were to accept...* $\\rightarrow$ **Were they to accept** the offer, negotiations would conclude.""",
        "examples": [
            {"text": "If municipal authorities had invested in flood defenses a decade ago, thousands of families would not be displaced today.", "notes": "Mixed conditional: Past Perfect condition with present consequence."},
            {"text": "Had the researchers calibrated their instruments more rigorously, the experimental anomalies would have been detected.", "notes": "Formal inverted third conditional replacing 'If they had'."},
            {"text": "If renewable energy were completely cost-neutral, developing economies would adopt it unconditionally.", "notes": "Second conditional with subjunctive 'were'."}
        ],
        "guided_exercises": [
            {
                "id": "b2_g_ge_1",
                "prompt": "Complete the Third Conditional: 'If the team _____ (conduct) the safety audit, the defect would have been discovered.'",
                "answer": "had conducted",
                "explanation": "Third conditional if-clause requires Past Perfect: 'had conducted'."
            },
            {
                "id": "b2_g_ge_2",
                "prompt": "Transform into an inverted conditional: 'If you had informed us earlier...'",
                "answer": "Had you informed us earlier",
                "explanation": "Invert auxiliary 'Had' with subject 'you' and omit 'If'."
            },
            {
                "id": "b2_g_ge_3",
                "prompt": "Complete the mixed conditional: 'If I had studied medicine in college, I _____ (be) a surgeon now.'",
                "answer": "would be",
                "explanation": "Past condition (had studied) yields present consequence (would be now)."
            }
        ],
        "assessment": [
            {
                "id": "b2_g_as_1",
                "question": "Which sentence demonstrates the correct structure of a Mixed Conditional (Past Action ➔ Present Consequence)?",
                "options": [
                    "If she won the lottery last week, she will buy a house today.",
                    "If she had taken the train yesterday, she would be in Edinburgh right now.",
                    "If she took the train yesterday, she would have been in Edinburgh right now.",
                    "If she had taken the train yesterday, she will have been in Edinburgh right now."
                ],
                "correct_index": 1,
                "explanation": "Past condition ('had taken') combined with present hypothetical outcome ('would be right now')."
            },
            {
                "id": "b2_g_as_2",
                "question": "Choose the grammatically correct formal inverted conditional:",
                "options": [
                    "Had the government intervened, the economic crisis would have been mitigated.",
                    "Did the government intervened, the crisis would be mitigated.",
                    "If had the government intervened, the crisis was mitigated.",
                    "Having the government intervened, the crisis will be mitigated."
                ],
                "correct_index": 0,
                "explanation": "'Had + Subject + V3' correctly replaces 'If the government had intervened'."
            },
            {
                "id": "b2_g_as_3",
                "question": "Identify the common conditional error in: 'If I would have known about the deadline, I would have submitted earlier.'",
                "options": [
                    "There is no error; it is standard academic English.",
                    "'Would have' should never be used in the if-clause of a standard conditional.",
                    "The main clause verb should be in present simple.",
                    "The sentence requires 'unless' instead of 'if'."
                ],
                "correct_index": 1,
                "explanation": "In standard English, 'would have' is prohibited in the if-clause (use 'If I had known')."
            }
        ]
    },
    {
        "id": "curric_b2_vocab_technology_environment",
        "cefr_level": "B2",
        "module_type": "vocabulary",
        "title": "Technology, Artificial Intelligence & Environmental Science",
        "order_index": 2,
        "prerequisites": ["curric_b1_vocab_workplace_education"],
        "estimated_minutes": 50,
        "objectives": [
            "Deploy Band 7+ vocabulary for sustainability, biodiversity, and ecosystem preservation",
            "Master technological and machine intelligence terminology (algorithmic, automation, surveillance)",
            "Use precise academic verbs ('mitigate', 'exacerbate', 'proliferate', 'deplete') in context"
        ],
        "explanation_markdown": """### 1. Environmental Science Lexicon (Band 7–8)
- **Sustainability:** Meeting present needs without compromising the ability of future generations to meet theirs.
- **Biodiversity:** The variety of plant and animal life in a particular habitat or biome.
- **Mitigation vs Adaptation:**
  * *Mitigation:* Actions to reduce or prevent greenhouse gas emissions (*afforestation, renewable energy*).
  * *Adaptation:* Actions to manage the unavoidable impacts of climate change (*sea walls, drought-resistant crops*).
- **Carbon Footprint / Offset:** The total greenhouse gases caused by an entity, compensated by ecological investments.

### 2. Technology & Artificial Intelligence Lexicon
- **Algorithmic Bias:** Systematic and unfair discrimination generated by computer algorithms reflecting prejudiced training data.
- **Automation:** The replacement of manual human labor by computational or mechanical systems.
- **Data Sovereignty:** The legal principle that digital information is subject to the laws of the nation where it is collected.

### 3. High-Tier Academic Verbs:
- **mitigate** (v) = to make less severe (*mitigate climate impacts*).
- **exacerbate** (v) = to make a problem or condition worse (*deforestation exacerbates soil erosion*).
- **deplete** (v) = to exhaust a physical supply (*deplete groundwater reserves*).""",
        "examples": [
            {"text": "Unregulated industrial effluent significantly exacerbates riverine pollution in developing regions.", "notes": "Academic verb 'exacerbate' used in environmental context."},
            {"text": "Urban planners must implement robust flood mitigation strategies rather than relying on reactive measures.", "notes": "Distinction between proactive 'mitigation' and reactive response."},
            {"text": "Algorithmic decision-making in credit scoring can perpetuate socio-economic inequality if training datasets are biased.", "notes": "Band 8+ technology discourse."}
        ],
        "guided_exercises": [
            {
                "id": "b2_v_ge_1",
                "prompt": "Insert the verb meaning 'to make less severe': 'Governments must act decisively to _____ the devastating effects of drought.' (mitigate / exacerbate)",
                "answer": "mitigate",
                "explanation": "'Mitigate' means to alleviate or lessen the severity of a crisis."
            },
            {
                "id": "b2_v_ge_2",
                "prompt": "Complete the collocation: 'Overfishing threatens to completely _____ marine fish stocks by 2050.' (deplete / inflate)",
                "answer": "deplete",
                "explanation": "'Deplete' means to exhaust or diminish resources to critical levels."
            },
            {
                "id": "b2_v_ge_3",
                "prompt": "Which term describes systematic unfairness encoded in AI software? (algorithmic bias / computational virtue)",
                "answer": "algorithmic bias",
                "explanation": "'Algorithmic bias' refers to computational discrimination arising from skewed data."
            }
        ],
        "assessment": [
            {
                "id": "b2_v_as_1",
                "question": "What is the critical distinction between climate 'mitigation' and climate 'adaptation'?",
                "options": [
                    "Mitigation addresses root causes by reducing emissions; adaptation adjusts societal systems to live with impacts.",
                    "Mitigation is for animals; adaptation is for plants.",
                    "Adaptation is always free; mitigation requires financial loans.",
                    "There is no distinction in climate science."
                ],
                "correct_index": 0,
                "explanation": "Mitigation seeks to prevent global warming; adaptation adjusts infrastructure to endure it."
            },
            {
                "id": "b2_v_as_2",
                "question": "Which verb means 'to make a bad situation even worse'?",
                "options": [
                    "Ameliorate",
                    "Exacerbate",
                    "Synthesize",
                    "Facilitate"
                ],
                "correct_index": 1,
                "explanation": "'Exacerbate' means to intensify or worsen an existing problem."
            },
            {
                "id": "b2_v_as_3",
                "question": "Select the correct academic collocation:",
                "options": [
                    "Excessive deforestation depletes atmospheric moisture and accelerates desertification.",
                    "Excessive deforestation grows atmospheric moisture and finishes deserts.",
                    "Deforestation makes climate happy.",
                    "Trees are disappearing and making the ground very dry."
                ],
                "correct_index": 0,
                "explanation": "'Depletes moisture' and 'accelerates desertification' are natural Band 8+ academic pairings."
            }
        ]
    },
    {
        "id": "curric_b2_read_claims",
        "cefr_level": "B2",
        "module_type": "reading",
        "title": "Identifying Writer Views & Claims (Y/N/NG & T/F/NG)",
        "order_index": 3,
        "prerequisites": ["curric_b1_read_skimming", "curric_b2_vocab_technology_environment"],
        "estimated_minutes": 55,
        "objectives": [
            "Master the critical distinction between FALSE/NO (explicitly contradicted) and NOT GIVEN (unverified/missing)",
            "Differentiate author opinion and attitude from neutral third-party reporting in academic passages",
            "Identify qualifying adverbs ('partially', 'predominantly', 'allegedly') that alter propositional truth"
        ],
        "explanation_markdown": """### The Golden Rule of IELTS False vs Not Given
This question type is the single biggest trap in IELTS Reading:
- **TRUE / YES:** The passage explicitly confirms the claim, using direct synonyms or identical logical propositions.
- **FALSE / NO:** The passage **directly contradicts or refutes** the claim (i.e. The text says X, but the statement says opposite of X).
- **NOT GIVEN:** The passage neither confirms nor contradicts the claim. The idea might be plausible or generally true in the real world, but **the specific relationship cannot be proven from the text alone**.

#### Passage Excerpt: Automated Agriculture
```
While automated agricultural robotics have proliferated across North America, their capital 
acquisition cost remains prohibitive for smallholder family farming collectives. Proponents 
argue that autonomous seed drills reduce labor costs by up to forty percent. However, independent 
agronomists note that the high frequency of software sensor malfunctions in wet, clay-heavy soils 
often negates these anticipated operational savings. Notably, agricultural technology manufacturers 
have declined to subsidize repair warranties for farming collectives operating on marginal lands.
```

#### Analytical Breakdown:
- *Statement 1:* 'Autonomous seed drills decrease labor expenditures.' $\\rightarrow$ **TRUE** (Text: *reduce labor costs by up to forty percent*).
- *Statement 2:* 'Independent agronomists believe robotics always guarantee net financial profits.' $\\rightarrow$ **FALSE** (Text: *sensor malfunctions often negate anticipated savings*).
- *Statement 3:* 'European smallholders purchase more autonomous equipment than Asian farmers.' $\\rightarrow$ **NOT GIVEN** (The text mentions North America; it does NOT compare European vs Asian farmers).""",
        "examples": [
            {"text": "The statement is FALSE because the author states that sensor errors negate financial savings.", "notes": "Contradiction explicitly documented in the passage."},
            {"text": "The statement is NOT GIVEN because although plausible, the text does not mention European farming rates.", "notes": "Crucial distinction between real-world fact and text evidence."},
            {"text": "Qualifying words like 'often' prevent absolute claims from being classified as TRUE.", "notes": "Attending to modal adverbs."}
        ],
        "guided_exercises": [
            {
                "id": "b2_r_ge_1",
                "prompt": "Evaluate based on text: 'Sensor malfunctions in clay soils occur frequently.' (TRUE / FALSE / NOT GIVEN)",
                "answer": "TRUE",
                "explanation": "Text explicitly notes 'the high frequency of software sensor malfunctions in wet, clay-heavy soils'."
            },
            {
                "id": "b2_r_ge_2",
                "prompt": "Evaluate: 'Agricultural technology manufacturers provide free replacement warranties to marginal farmers.' (TRUE / FALSE / NOT GIVEN)",
                "answer": "FALSE",
                "explanation": "Text explicitly states manufacturers 'have declined to subsidize repair warranties'."
            },
            {
                "id": "b2_r_ge_3",
                "prompt": "Evaluate: 'Autonomous robotics will replace all human farm laborers by 2040.' (TRUE / FALSE / NOT GIVEN)",
                "answer": "NOT GIVEN",
                "explanation": "No timeline or total labor replacement prediction for 2040 appears in the text."
            }
        ],
        "assessment": [
            {
                "id": "b2_r_as_1",
                "question": "What is the primary condition that makes an answer 'FALSE' in an IELTS reading exam?",
                "options": [
                    "The text does not mention the topic at all",
                    "The text explicitly provides factual information that directly contradicts the statement",
                    "The student personally disagrees with the author's opinion",
                    "The statement contains difficult vocabulary"
                ],
                "correct_index": 1,
                "explanation": "'FALSE' strictly requires direct evidential contradiction in the text."
            },
            {
                "id": "b2_r_as_2",
                "question": "Based on the passage above, evaluate: 'Smallholder family farming collectives find the purchasing price of agricultural robotics too expensive.'",
                "options": [
                    "TRUE",
                    "FALSE",
                    "NOT GIVEN",
                    "Cannot be answered"
                ],
                "correct_index": 0,
                "explanation": "The text states 'their capital acquisition cost remains prohibitive for smallholder family farming collectives'."
            },
            {
                "id": "b2_r_as_3",
                "question": "Why would the statement 'Farmers in Canada prefer drones over autonomous tractors' be NOT GIVEN?",
                "options": [
                    "Because Canada is part of North America",
                    "Because the text does not compare farmer preference for drones versus tractors",
                    "Because drones are cheaper than tractors",
                    "Because the statement is false"
                ],
                "correct_index": 1,
                "explanation": "The passage contains zero information comparing drones to autonomous tractors."
            }
        ]
    },
    {
        "id": "curric_b2_listen_debates",
        "cefr_level": "B2",
        "module_type": "listening",
        "title": "Following Academic Debates & Conflicting Views",
        "order_index": 4,
        "prerequisites": ["curric_b1_listen_lectures"],
        "estimated_minutes": 50,
        "objectives": [
            "Track multi-party collegiate discussions featuring disagreement and concession markers",
            "Identify when a speaker concedes a point ('Granted, but...', 'I concede that... nevertheless')",
            "Extract implicit authorial stance from vocal tone, stress, and hesitation markers"
        ],
        "explanation_markdown": """### Transcript-Based Listening Strategy: Academic Colloquia
*(Practice session using authentic IELTS Section 3 seminar scripts.)*

#### Audio Script: Artificial Intelligence in Healthcare
```
DR TRENT: In my view, deploying deep learning neural networks for oncological screening 
is already saving lives. Algorithms detect malignant cellular anomalies up to two years 
before human pathologists spot them on biopsy slides.
DR VASQUEZ: Granted, Trent. No one disputes the algorithmic diagnostic precision under 
sanitized laboratory benchmark datasets. But what concerns clinical ethicists is the 'black box' 
problem. If a clinician cannot interpret how the neural network reached a malignant determination, 
they cannot defend that diagnosis to a terrified patient.
DR TRENT: That is a legitimate ethical objection, Vasquez. However, refusing to implement 
an eighty-five percent more accurate diagnostic instrument solely because its mathematical 
parameters are opaque strikes me as ethically indefensible.
DR VASQUEZ: My proposal isn't abandonment, but phased integration alongside mandatory human consensus.
```

#### Critical Listening Markers:
- **Concession Words:** *'Granted...', 'Admittedly...', 'Up to a point, but...'*
- **Rebuttal Pivot:** *'However, refusing to...', 'The fundamental caveat is...'*
- **Synthesized Compromise:** *'My proposal isn't abandonment, but phased integration...'*""",
        "examples": [
            {"text": "Dr Trent advocates immediate deployment based on early cancer detection rates.", "notes": "Identifying primary speaker thesis."},
            {"text": "Dr Vasquez concedes laboratory precision but highlights the 'black box' interpretability problem.", "notes": "Recognizing concession + qualification."},
            {"text": "Both researchers ultimately agree on phased human-supervised integration.", "notes": "Tracking convergence of academic viewpoints."}
        ],
        "guided_exercises": [
            {
                "id": "b2_l_ge_1",
                "prompt": "What major ethical concern does Dr Vasquez raise regarding deep learning models?",
                "answer": "the black box problem / lack of interpretability",
                "explanation": "Vasquez states 'what concerns clinical ethicists is the black box problem'."
            },
            {
                "id": "b2_l_ge_2",
                "prompt": "How does Dr Trent describe refusing to use a model that is 85% more accurate?",
                "answer": "ethically indefensible",
                "explanation": "Trent states that refusing it 'strikes me as ethically indefensible'."
            },
            {
                "id": "b2_l_ge_3",
                "prompt": "What middle-ground solution does Dr Vasquez propose in the final turn?",
                "answer": "phased integration alongside mandatory human consensus",
                "explanation": "Vasquez proposes 'phased integration alongside mandatory human consensus'."
            }
        ],
        "assessment": [
            {
                "id": "b2_l_as_1",
                "question": "What is Dr Vasquez's actual stance on medical AI models?",
                "options": [
                    "She wants all medical AI banned permanently",
                    "She accepts their diagnostic precision but insists on interpretable, human-verified phased adoption",
                    "She believes human doctors are completely obsolete",
                    "She has no opinion on medical technology"
                ],
                "correct_index": 1,
                "explanation": "Vasquez concedes accuracy while advocating phased implementation with mandatory human consensus."
            },
            {
                "id": "b2_l_as_2",
                "question": "Which spoken conversational phrase indicates that a speaker is temporarily agreeing before presenting an objection?",
                "options": [
                    "Granted, but...",
                    "Never in my life...",
                    "You are completely wrong...",
                    "I don't care..."
                ],
                "correct_index": 0,
                "explanation": "'Granted, but...' is a standard academic concession phrase."
            },
            {
                "id": "b2_l_as_3",
                "question": "What does the 'black box' problem refer to in machine learning discourse?",
                "options": [
                    "A computer monitor that turns off during power outages",
                    "The inability of humans to interpret the internal decision-making pathway of complex algorithms",
                    "A physical container used to ship computer servers",
                    "An encrypted security password"
                ],
                "correct_index": 1,
                "explanation": "A 'black box' algorithm produces accurate outputs without explaining the intermediate reasoning steps."
            }
        ]
    },
    {
        "id": "curric_b2_write_peel",
        "cefr_level": "B2",
        "module_type": "writing",
        "title": "PEEL Paragraphs & Cohesive Linking in Essay Writing",
        "order_index": 5,
        "prerequisites": ["curric_b1_write_paragraphs", "curric_b2_gram_conditionals"],
        "estimated_minutes": 55,
        "objectives": [
            "Execute the PEEL (Point, Explanation, Evidence, Link) paragraph model for IELTS Task 2 essays",
            "Deploy advanced transitional devices ('Furthermore', 'In contrast', 'Thereby', 'Notwithstanding')",
            "Avoid examiner penalties for overused mechanical linkers ('Firstly', 'Secondly', 'In a nutshell')"
        ],
        "explanation_markdown": """### 1. The PEEL Paragraph Framework for IELTS Task 2
Examiners assess **Coherence and Cohesion (CC)** and **Task Response (TR)** through paragraph structure. Each body paragraph must follow the PEEL protocol:

- **P — Point (Topic Sentence):** One clear, focused controlling argument directly addressing the prompt.
  * *'Championing renewable energy subsidies accelerates national economic resilience.'*
- **E — Explanation (The Analytical Mechanism):** Explains *why* and *how* the point operates in reality.
  * *'When governments absorb initial photovoltaic installation costs, manufacturing economies of scale lower energy tariffs across domestic and commercial sectors.'*
- **E — Evidence (Concrete Illustration):** Realistic real-world trend, documented policy, or institutional case study.
  * *'For instance, municipalities across Scandinavia that subsidized solar conversion witnessed a thirty percent reduction in peak-hour grid vulnerability.'*
- **L — Link (Connecting back to the central thesis):**
  * *'Consequently, subsidizing sustainable energy infrastructure represents a fiscally prudent long-term investment.'*

### 2. High-Tier Cohesive Devices vs Overused Clichés
- Avoid: ✗ *Firstly, Secondly, In a nutshell, In the modern world.*
- Deploy: ✓ *Initially, Furthermore, Conversely, Consequently, Notwithstanding these advantages, Thereby facilitating...*""",
        "examples": [
            {"text": "Championing vocational apprenticeships alongside academic degrees mitigates structural unemployment.", "notes": "Clear, arguable PEEL Point."},
            {"text": "By integrating practical on-the-job training, graduates acquire directly transferable technical competencies.", "notes": "Thorough analytical Explanation."},
            {"text": "Consequently, diversifying secondary curricula bridges the persistent skills deficit in contemporary industries.", "notes": "Strong closing Link to essay thesis."}
        ],
        "guided_exercises": [
            {
                "id": "b2_w_ge_1",
                "prompt": "Identify the 'Evidence' component in: 'For instance, Danish offshore wind farms generated over 50% of the nation's electricity in 2023.'",
                "answer": "Evidence",
                "explanation": "This sentence provides concrete empirical data illustrating the general claim."
            },
            {
                "id": "b2_w_ge_2",
                "prompt": "Replace the overused phrase 'In a nutshell' with a formal academic summary phrase:",
                "answer": "In summary / In conclusion",
                "explanation": "'In a nutshell' is informal idiom; use 'In conclusion' or 'In summary'."
            },
            {
                "id": "b2_w_ge_3",
                "prompt": "Insert a participle linker: 'The council expanded bus routes, _____ reducing reliance on private motorcars.' (thereby / but)",
                "answer": "thereby",
                "explanation": "'Thereby + gerund (-ing)' shows direct consequence in formal academic writing."
            }
        ],
        "assessment": [
            {
                "id": "b2_w_as_1",
                "question": "What is the primary flaw in this body paragraph: 'First, cars cause pollution. Second, electric cars are clean. Finally, we must buy bikes.'?",
                "options": [
                    "It has too many advanced words",
                    "It presents an unlinked list of assertions without analytical explanation, evidence, or coherent PEEL development",
                    "It is written in British English",
                    "It lacks bullet points"
                ],
                "correct_index": 1,
                "explanation": "Listing brief assertions with mechanical linkers yields a low Coherence and Cohesion score."
            },
            {
                "id": "b2_w_as_2",
                "question": "Which of the following is a Band 8+ transitional sentence signaling a counter-argument?",
                "options": [
                    "Notwithstanding these undeniable benefits, critics argue that the initial capital outlay is fiscally unsustainable.",
                    "On the other hand I hate this idea.",
                    "Next paragraph is about bad things.",
                    "But some people say no."
                ],
                "correct_index": 0,
                "explanation": "'Notwithstanding these undeniable benefits, critics argue...' demonstrates sophisticated syntax and lexical control."
            },
            {
                "id": "b2_w_as_3",
                "question": "How does the 'Link' sentence in a PEEL paragraph help Task Response?",
                "options": [
                    "It increases word count artificially",
                    "It explicitly proves that the paragraph's evidence answers the prompt question",
                    "It quotes a famous poem",
                    "It changes the topic to something new"
                ],
                "correct_index": 1,
                "explanation": "The link ties the evidence back to the central thesis and demonstrates full task fulfillment."
            }
        ]
    },
    {
        "id": "curric_b2_speak_complex_arguments",
        "cefr_level": "B2",
        "module_type": "speaking",
        "title": "Complex Arguments & Part 3 Discussion Scenarios",
        "order_index": 6,
        "prerequisites": ["curric_b1_speak_opinions_justification"],
        "estimated_minutes": 50,
        "objectives": [
            "Structure extended, nuanced answers to abstract questions in IELTS Speaking Part 3",
            "Contrast societal, economic, and generational perspectives within a single spoken turn",
            "Use concession markers to demonstrate intellectual balance ('While X is valid, Y cannot be ignored')"
        ],
        "explanation_markdown": """### Advanced 2-Sided Balance in Speaking Part 3
In IELTS Speaking Part 3, questions move away from personal habits to broad societal issues. Candidates must demonstrate the ability to evaluate multiple perspectives:

#### Question: *'Do you believe that printed physical books will completely disappear in the digital era?'*

#### High-Scoring Response Architecture:
1. **Concession to Prevailing Trend:**
   * *'While it is indisputable that digital e-readers and tablet applications offer unparalleled portability and convenience...'*
2. **Countervailing Evidence / Sociological Reality:**
   * *'...I am strongly inclined to believe that physical print volumes will endure as prized artifacts.'*
3. **Elaboration & Distinction:**
   * *'From an educational perspective, neurological studies demonstrate that tactile paper interaction fosters superior reading comprehension. Furthermore, collectors value physical books for their aesthetic and archival permanence.'*

### Core Contrasting Markers:
- *While one school of thought suggests... others contend that...*
- *Broadly speaking, older generations prioritize... whereas younger demographics gravitate towards...*
- *Economically speaking, it makes sense; however, from an ethical standpoint...*""",
        "examples": [
            {"text": "While digital automation enhances factory output, it inevitably displaces blue-collar workers in the short term.", "notes": "Concession ('while') balancing economic gain with social cost."},
            {"text": "Generational attitudes differ markedly; whereas senior citizens value face-to-face banking, younger demographics demand instantaneous mobile transactions.", "notes": "Sociological contrast comparing age cohorts."},
            {"text": "From an environmental perspective, renewable subsidies are crucial, yet developing nations face immediate fiscal constraints.", "notes": "Multi-angle evaluation."}
        ],
        "guided_exercises": [
            {
                "id": "b2_sp_ge_1",
                "prompt": "Insert a concession marker: '_____ digital tools offer convenience, excessive screen time impairs cognitive focus.' (While / Despite of)",
                "answer": "While",
                "explanation": "'While' introduces a concession clause followed by subject + verb."
            },
            {
                "id": "b2_sp_ge_2",
                "prompt": "Contrast two cohorts using 'whereas': 'Older citizens prefer cash payments, _____ younger consumers use contactless cards.'",
                "answer": "whereas",
                "explanation": "'Whereas' coordinates two contrasting facts or groups."
            },
            {
                "id": "b2_sp_ge_3",
                "prompt": "Which phrase introduces a sociological viewpoint? (From a sociological perspective / Socially thinking)",
                "answer": "From a sociological perspective",
                "explanation": "'From a [sociological/economic] perspective' is formal academic discourse."
            }
        ],
        "assessment": [
            {
                "id": "b2_sp_as_1",
                "question": "Which response to 'Has technological progress improved modern communication?' best demonstrates Band 7+ intellectual balance?",
                "options": [
                    "Yes, smartphones are fast and good.",
                    "It has produced paradoxical outcomes. While instant messaging facilitates immediate global connectivity, it has simultaneously eroded face-to-face empathetic interaction, leading to increased feelings of social isolation.",
                    "Technology is very bad and we should stop it.",
                    "I use my phone every day to text my friends."
                ],
                "correct_index": 1,
                "explanation": "Acknowledges paradox, balances instant connectivity with eroded face-to-face interaction using sophisticated lexis."
            },
            {
                "id": "b2_sp_as_2",
                "question": "What is the primary role of concession markers like 'Admittedly' or 'While' in speaking exams?",
                "options": [
                    "To show that the candidate knows only one side of the topic",
                    "To demonstrate critical thinking by acknowledging valid counterpoints before reinforcing one's primary stance",
                    "To waste time when unsure what to say",
                    "To apologize to the examiner"
                ],
                "correct_index": 1,
                "explanation": "Concessions prove the speaker can evaluate multi-dimensional arguments."
            },
            {
                "id": "b2_sp_as_3",
                "question": "Which transition phrase effectively shifts focus to an economic analysis?",
                "options": [
                    "Talking about money things...",
                    "From a macroeconomic vantage point...",
                    "Dollars and cents are...",
                    "Economics is something that..."
                ],
                "correct_index": 1,
                "explanation": "'From a macroeconomic vantage point...' is an advanced academic frame."
            }
        ]
    },
    {
        "id": "curric_b2_pron_connected_speech",
        "cefr_level": "B2",
        "module_type": "pronunciation",
        "title": "Connected Speech, Linking & Elision",
        "order_index": 7,
        "prerequisites": ["curric_b1_pron_word_stress"],
        "estimated_minutes": 50,
        "objectives": [
            "Master consonant-to-vowel catenation (linking words smoothly across boundaries)",
            "Identify and produce intrusive consonants (/r/, /j/, /w/) between adjacent vowel sounds",
            "Recognize natural elision (sound dropping) and assimilation in fast authentic spoken English"
        ],
        "explanation_markdown": """### The Mechanics of Connected Speech
In natural fluent English, words do not stop and start with pauses. They flow together:

#### 1. Catenation (Consonant to Vowel Linking):
When a word ends in a consonant and the next begins with a vowel, the consonant shifts onto the following word:
- *an apple* $\\rightarrow$ /əˈnæpl/ (sounds like 'a napple')
- *hold on* $\\rightarrow$ /həʊldˈɒn/ (sounds like 'hol-don')
- *first of all* $\\rightarrow$ /fɜːst ə vɔːl/

#### 2. Intrusive Linking Consonants:
When two vowels meet across words, native speakers insert an intrusive consonant to bridge the gap:
- **Intrusive /r/:** *law and order* $\\rightarrow$ /lɔː r ən ɔːdə/ | *media interest* $\\rightarrow$ /ˈmiːdiə r ˈɪntrəst/
- **Intrusive /j/:** *I agree* $\\rightarrow$ /aɪ j əˈɡriː/ | *she asked* $\\rightarrow$ /ʃiː j ɑːskt/
- **Intrusive /w/:** *go out* $\\rightarrow$ /ɡəʊ w aʊt/ | *two hours* $\\rightarrow$ /tuː w ˈaʊəz/

#### 3. Elision (Omission of Sounds in Rapid Speech):
In fast speech, weak /t/ and /d/ between consonants are dropped:
- *next door* $\\rightarrow$ /neks dɔː/ (the /t/ disappears)
- *you and me* $\\rightarrow$ /juː ən miː/ (the /d/ disappears)""",
        "examples": [
            {"text": "Law and order must be maintained across regional jurisdictions.", "notes": "Intrusive /r/ bridges 'law' /lɔː/ and 'and' /ænd/."},
            {"text": "Could you please hold on for a couple of minutes?", "notes": "Catenation: 'hold on' /həʊldˈɒn/."},
            {"text": "She asked if they could go out for dinner.", "notes": "Intrusive /j/ in 'she asked' and intrusive /w/ in 'go out'."}
        ],
        "guided_exercises": [
            {
                "id": "b2_p_ge_1",
                "prompt": "Which intrusive sound links 'two' and 'apples'? (/r/ / /j/ / /w/)",
                "answer": "/w/",
                "explanation": "Rounded vowel /uː/ links to the following vowel with an intrusive /w/: /tuː w ˈæplz/."
            },
            {
                "id": "b2_p_ge_2",
                "prompt": "Which intrusive sound links 'I' and 'always'? (/r/ / /j/ / /w/)",
                "answer": "/j/",
                "explanation": "Spread diphthong /aɪ/ links with an intrusive /j/: /aɪ j ˈɔːlweɪz/."
            },
            {
                "id": "b2_p_ge_3",
                "prompt": "In the phrase 'last night', which sound is typically dropped (elided) in rapid speech? (/s/ / /t/ / /n/)",
                "answer": "/t/",
                "explanation": "The /t/ in 'last' is sandwiched between consonants and is elided: /lɑːs naɪt/."
            }
        ],
        "assessment": [
            {
                "id": "b2_p_as_1",
                "question": "What is the phenomenon called when the final consonant of one word attaches to the opening vowel of the next?",
                "options": [
                    "Catenation (or linking)",
                    "Vowel mutation",
                    "Palatalization",
                    "Aspiration"
                ],
                "correct_index": 0,
                "explanation": "Catenation links a final consonant smoothly to an initial vowel."
            },
            {
                "id": "b2_p_as_2",
                "question": "In British Received Pronunciation, which intrusive sound is inserted in 'the idea of it'?",
                "options": [
                    "Intrusive /p/",
                    "Intrusive /r/",
                    "Intrusive /k/",
                    "Intrusive /m/"
                ],
                "correct_index": 1,
                "explanation": "Non-rhotic accents insert an intrusive /r/ between schwa and /ɒv/: /aɪˈdɪə r əv ɪt/."
            },
            {
                "id": "b2_p_as_3",
                "question": "Why is understanding connected speech critical for IELTS Listening candidates?",
                "options": [
                    "Because words sound different in connected stream-of-speech than in isolated dictionary forms",
                    "Because examiners speak with fake accents",
                    "Because listening exams are always whisper tests",
                    "There is no connection between pronunciation and listening"
                ],
                "correct_index": 0,
                "explanation": "Elision and linking cause words to blend, making individual word boundary identification challenging."
            }
        ]
    },
    {
        "id": "curric_b2_func_meetings",
        "cefr_level": "B2",
        "module_type": "functional",
        "title": "Leading Meetings & Diplomatic Disagreement",
        "order_index": 8,
        "prerequisites": ["curric_b1_func_business_emails"],
        "estimated_minutes": 50,
        "objectives": [
            "Chair professional meetings, set agendas, and steer discussion towards consensus",
            "Express diplomatic and respectful disagreement without sounding confrontational or blunt",
            "Summarize opposing proposals and formulate actionable next steps"
        ],
        "explanation_markdown": """### 1. Chairing & Steering Workplace Meetings
- **Opening & Agenda Setting:**
  * *'Thank you for joining, everyone. The objective of today's meeting is to evaluate our Q3 product deployment schedule.'*
- **Inviting Input:**
  * *'Marcus, could you share the engineering team's perspective on this timeline?'*
- **Managing Interruptions:**
  * *'Could we please let Elena finish her point, and then we will open the floor to questions?'*

### 2. The Diplomatic Disagreement Formula
In professional international business English, direct contradiction (*'You are wrong'*) is considered abrasive and uncollaborative. Use the **Acknowledge $\\rightarrow$ Pivot $\\rightarrow$ Counter** formula:
1. **Acknowledge:** *'I take your point regarding budget constraints...'*
2. **Pivot:** *'...however, we need to bear in mind that...'*
3. **Counter / Solution:** *'...skimping on QA testing now will result in much higher warranty expenses later.'*

### Diplomatic Softeners:
- *'I see what you mean, but from an operational perspective...'*
- *'I have some reservations about that approach, primarily because...'*
- *'Could we explore an alternative solution where we compromise on...'*""",
        "examples": [
            {"text": "I take your point about marketing spend; however, diverting funds away from product engineering carries substantial risks.", "notes": "Diplomatic disagreement formula in business context."},
            {"text": "Could we table that topic for our next session so that we can conclude today's primary agenda?", "notes": "Effective meeting management and timeboxing."},
            {"text": "To summarize today's consensus: Sarah will revise the draft timeline by Friday, and David will review the budget.", "notes": "Action-oriented meeting conclusion."}
        ],
        "guided_exercises": [
            {
                "id": "b2_f_ge_1",
                "prompt": "Soften this blunt contradiction: 'Your plan is too expensive.'",
                "answer": "I have some reservations regarding the projected budget.",
                "explanation": "Use 'I have some reservations about...' or 'I see what you mean, however the fiscal cost is substantial'."
            },
            {
                "id": "b2_f_ge_2",
                "prompt": "Which idiom means to postpone a discussion for a future meeting? (to table / to chair)",
                "answer": "to table",
                "explanation": "To 'table' an item means to postpone or set it aside for future deliberation."
            },
            {
                "id": "b2_f_ge_3",
                "prompt": "Complete the meeting opening: 'The _____ of today's meeting is to finalize the project scope.' (objective / story)",
                "answer": "objective",
                "explanation": "'The objective / purpose of today's meeting' is standard business procedure."
            }
        ],
        "assessment": [
            {
                "id": "b2_f_as_1",
                "question": "Which statement expresses professional disagreement most diplomatically in an executive board meeting?",
                "options": [
                    "That idea makes no sense whatsoever.",
                    "I understand the rationale behind that proposal; nevertheless, I have serious reservations regarding its regulatory feasibility.",
                    "You don't understand the business.",
                    "Stop talking because I disagree."
                ],
                "correct_index": 1,
                "explanation": "Acknowledges rationale before articulating calibrated reservations diplomatically."
            },
            {
                "id": "b2_f_as_2",
                "question": "What is the primary role of a meeting chairperson when two participants begin arguing aggressively?",
                "options": [
                    "Join the argument and shout louder",
                    "Intervene calmly, acknowledge both viewpoints, and refocus the discussion onto the agreed agenda",
                    "Immediately cancel the project",
                    "Leave the room"
                ],
                "correct_index": 1,
                "explanation": "The chairperson must steer the meeting objectively back to productive agenda items."
            },
            {
                "id": "b2_f_as_3",
                "question": "How should a professional summarize action items at the conclusion of a meeting?",
                "options": [
                    "By assigning specific owners, actionable deliverables, and agreed deadlines",
                    "By saying 'Someone do something next week'",
                    "By deleting the meeting minutes",
                    "By asking attendees to forget what was discussed"
                ],
                "correct_index": 0,
                "explanation": "Action items must feature clear ownership, specific tasks, and clear deadlines."
            }
        ]
    },
    {
        "id": "curric_b2_review_milestone",
        "cefr_level": "B2",
        "module_type": "review",
        "title": "B2 Milestone Review & Comprehensive Evaluation",
        "order_index": 9,
        "prerequisites": ["curric_b2_gram_conditionals", "curric_b2_write_peel"],
        "estimated_minutes": 60,
        "objectives": [
            "Demonstrate mastery of Mixed Conditionals, PEEL essay paragraphing, and academic collocations",
            "Certify readiness for CEFR C1 Advanced coursework and IELTS Band 6.5–7.5 performance",
            "Synthesize diplomatic disagreement, connected speech decoding, and multi-perspective argumentation"
        ],
        "explanation_markdown": """### B2 Milestone Comprehensive Synthesis
Attaining CEFR B2 certifies operational competence in demanding academic and professional contexts:
1. **Conditional Mastery:** Accurate command of Second, Third, and Mixed Conditionals without 'would have' errors in the if-clause.
2. **PEEL Essay Architecture:** Delivering authoritative Points, Explanations, Evidence, and Links.
3. **Reading Precision:** Flawless distinction between FALSE/NO (contradicted) and NOT GIVEN (unverified).
4. **Phonetic Connected Speech:** Navigating catenation, intrusive /r/, /j/, /w/, and vowel reduction.

Complete this capstone evaluation to certify your progression into C1 Advanced.""",
        "examples": [
            {"text": "Had regional governments subsidized micro-grid solar storage, thousands of households would not be experiencing rolling blackouts today.", "notes": "Inverted mixed conditional with advanced academic vocabulary."},
            {"text": "Notwithstanding these undeniable economic benefits, critics argue that aggressive automation exacerbates technological inequality.", "notes": "Sophisticated concessive discourse linking."},
            {"text": "The statement is NOT GIVEN because although plausible, the author never explicitly confirms European adoption rates.", "notes": "Critical analytical reading distinction."}
        ],
        "guided_exercises": [
            {
                "id": "b2_rev_ge_1",
                "prompt": "Combine into an inverted conditional: 'If she had known the terms, she would not have signed.'",
                "answer": "Had she known the terms, she would not have signed.",
                "explanation": "'Had + subject + past participle' replaces 'If she had'."
            },
            {
                "id": "b2_rev_ge_2",
                "prompt": "Complete: 'Electric cars produce zero emissions, _____ reducing urban air pollution.' (thereby / but)",
                "answer": "thereby",
                "explanation": "'Thereby + gerund' demonstrates formal cause-and-effect consequence."
            },
            {
                "id": "b2_rev_ge_3",
                "prompt": "What intrusive sound links 'law' and 'expert' in connected speech? (/r/ / /j/ / /w/)",
                "answer": "/r/",
                "explanation": "/lɔː r ˈekspɜːt/ inserts an intrusive /r/ across vowel boundaries."
            }
        ],
        "assessment": [
            {
                "id": "b2_rev_as_1",
                "question": "Which sentence demonstrates 100% flawless grammatical, conditional, and lexical control?",
                "options": [
                    "If the company would have invested in AI, they will be successful now.",
                    "Had the company invested in automation three years ago, it would be dominating the regional market today.",
                    "If the company invested in automation three years ago, it would dominated the market today.",
                    "Had the company invest in automation, it will dominate the market."
                ],
                "correct_index": 1,
                "explanation": "Inverted mixed conditional: 'Had the company invested' (past) + 'it would be dominating... today' (present)."
            },
            {
                "id": "b2_rev_as_2",
                "question": "In an IELTS reading exam, why is an answer marked NOT GIVEN instead of FALSE?",
                "options": [
                    "Because the reader personally thinks the statement is untrue",
                    "Because the passage lacks sufficient evidence to verify or refute the statement",
                    "Because the passage directly states the opposite",
                    "Because the question is an error"
                ],
                "correct_index": 1,
                "explanation": "NOT GIVEN means the text does not contain enough information to confirm or deny the claim."
            },
            {
                "id": "b2_rev_as_3",
                "question": "Which of the following represents an optimal PEEL link sentence for a paragraph on public transit subsidies?",
                "options": [
                    "That is all I have to say about buses.",
                    "Consequently, municipal funding for public transport constitutes an essential catalyst for equitable urban mobility.",
                    "Secondly, trains are also very clean.",
                    "In a nutshell, transit is good."
                ],
                "correct_index": 1,
                "explanation": "Authoritative, formal concluding link reconnecting evidence back to the essay prompt."
            }
        ]
    }
]

with open("content/curriculum/b2.json", "w", encoding="utf-8") as f:
    json.dump(B2_LESSONS, f, indent=2, ensure_ascii=False)
print("Saved B2:", len(B2_LESSONS), "lessons.")
