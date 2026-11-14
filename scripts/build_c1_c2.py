"""
build_c1_c2.py
Generates C1 and C2 curriculum JSON files with 9 modules each.
Preserves existing starter lesson IDs and adheres to 12 pedagogical components.
"""

import os
import json

CURRICULUM_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "curriculum")
os.makedirs(CURRICULUM_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# C1 — ADVANCED (9 Modules)
# -----------------------------------------------------------------------------
C1_LESSONS = [
    {
        "id": "curric_c1_gram_inversion",
        "cefr_level": "C1",
        "module_type": "grammar",
        "title": "Negative & Restrictive Adverbial Inversion",
        "order_index": 1,
        "prerequisites": ["curric_b2_gram_conditionals"],
        "estimated_minutes": 40,
        "objectives": [
            "Construct negative adverbial fronted inversions ('Rarely have we witnessed...', 'Under no circumstances should...').",
            "Employ limiting adverbs ('hardly... when', 'scarcely... before', 'no sooner... than') to express rapid chronological sequence.",
            "Utilize 'not only... but also' with auxiliary inversion to enhance rhetorical impact."
        ],
        "form_and_structure": "Negative Adverbial + Auxiliary Verb + Subject + Main Verb. (e.g. Seldom + do + researchers + encounter).",
        "usage_rationale": "Used in formal academic registers, scholarly critiques, and high-band IELTS writing/speaking to establish emphatic rhetorical contrast.",
        "positive_examples": [
            "Seldom has an economic policy triggered such profound societal restructuring.",
            "Not only did the intervention curtail infection rates, but it also bolstered healthcare resilience."
        ],
        "negative_examples": [
            "Seldom the government has intervened in market forces. (Inversion requires auxiliary before subject).",
            "Under no circumstances you should disclose participant confidentiality."
        ],
        "common_mistakes": [
            "Incorrect: 'Rarely I have seen such dedication.' -> Correct: 'Rarely have I seen such dedication.'",
            "Incorrect: 'No sooner had we arrived when the storm began.' -> Correct: 'No sooner had we arrived THAN the storm began.'"
        ],
        "confused_structures": [
            "'No sooner... than' vs 'Hardly / Scarcely... when'. Pairings must never be cross-contaminated."
        ],
        "explanation_markdown": """### The Architecture of Formal Inversion
When a negative or restrictive adverbial is fronted for emphasis, subject and auxiliary invert:
1. **Frequency & Degree Restrictions**:
   *Rarely do empirical observations diverge so starkly from theoretical models.*
2. **Prohibition & Strict Conditions**:
   *Under no circumstances should clinical data be published without ethical sanction.*
3. **Correlation & Succession**:
   *No sooner had the legislation been ratified than market volatility intensified.*""",
        "examples": [
            {"text": "Scarcely had the symposium concluded when the peer-review committee issued their verdict.", "notes": "'Scarcely... when' pairing with inverted past perfect."},
            {"text": "Only by examining longitudinal cohorts can epidemiologists identify causal correlations.", "notes": "'Only by...' requires inversion in the main clause ('can epidemiologists identify')."}
        ],
        "guided_exercises": [
            {"id": "c1_ge_1", "prompt": "Complete the inversion: 'Little _____ (do) the administration anticipate the public backlash.'", "answer": "did", "explanation": "Past tense inversion with 'Little' requires auxiliary 'did'."}
        ],
        "interactive_practice": [
            {
                "id": "c1_ip_1",
                "question": "Which sentence contains an error in correlative pairing?",
                "options": [
                    "No sooner had the bell rung than the students departed.",
                    "Hardly had the meeting commenced when the fire alarm sounded.",
                    "Scarcely had the treaty been signed than border disputes erupted anew.",
                    "Barely had the plane touched down when the passengers applauded."
                ],
                "correct_index": 2,
                "explanation": "'Scarcely' pairs with 'when' (or 'before'), NEVER with 'than'. ('No sooner' takes 'than')."
            }
        ],
        "assessment": [
            {
                "id": "c1_as_1",
                "question": "Select the grammatically flawless inverted sentence:",
                "options": [
                    "Under no circumstances employees must enter the server vault alone.",
                    "Under no circumstances must employees enter the server vault alone.",
                    "Under no circumstances employees should enter the server vault alone.",
                    "Under no circumstances do employees must enter the server vault alone."
                ],
                "correct_index": 1,
                "explanation": "Fronted 'Under no circumstances' requires modal auxiliary 'must' immediately preceding the subject 'employees'."
            }
        ],
        "review_questions": [
            "What happens to sentence word order when 'Not only' begins a sentence?",
            "Which conjunction pairs with 'No sooner', and which pairs with 'Hardly'?"
        ]
    },
    {
        "id": "curric_c1_vocab_academic_collocations",
        "cefr_level": "C1",
        "module_type": "vocabulary",
        "title": "Nuanced Academic Collocations & Collocational Chains",
        "order_index": 2,
        "prerequisites": ["curric_b2_vocab_academic_word_list"],
        "estimated_minutes": 35,
        "objectives": [
            "Deploy sophisticated verb-noun collocations ('cast doubt upon', 'lend credence to', 'exert influence', 'pose a threat').",
            "Incorporate adjective-noun collocational chains ('profound societal ramifications', 'rigorous empirical inquiry').",
            "Eliminate awkward, non-idiomatic literal translations in scholarly writing."
        ],
        "explanation_markdown": """### Unlocking Natural Academic Collocations
At C1, lexical resource is measured by natural, flexible collocations rather than isolated complex words:
- **Lend credence to**: *These demographic trends lend credence to the sociologist's thesis.*
- **Cast doubt upon**: *Recent experimental anomalies cast doubt upon the prevailing consensus.*
- **Pose a grave threat**: *Soil salinization poses a grave threat to agrarian food security.*""",
        "examples": [
            {"text": "The latest archaeological excavations shed substantial light on Bronze Age trade networks.", "notes": "'shed light on' is a high-yield academic collocation."}
        ],
        "guided_exercises": [
            {"id": "c1_v_ge_1", "prompt": "Complete the collocation: 'The evidence lends _____ to his claim.' (credence / credit)", "answer": "credence", "explanation": "The set academic collocation is 'lend credence to'."}
        ],
        "interactive_practice": [
            {
                "id": "c1_v_ip_1",
                "question": "Which verb collocates idiomatically with 'a threat to biodiversity'?",
                "options": ["Make", "Pose", "Do", "Give"],
                "correct_index": 1,
                "explanation": "Something 'poses a threat' or 'poses a challenge'."
            }
        ],
        "assessment": [
            {
                "id": "c1_v_as_1",
                "question": "Choose the most sophisticated academic collocation for indicating strong disagreement:",
                "options": [
                    "I am completely against this foolish idea.",
                    "The empirical evidence casts serious doubt upon the author's primary premise.",
                    "The writer tells lies about the situation.",
                    "Nobody agrees with this wrong argument."
                ],
                "correct_index": 1,
                "explanation": "'casts serious doubt upon the author's primary premise' embodies Band 8+ academic style."
            }
        ]
    },
    {
        "id": "curric_c1_read_complex_texts",
        "cefr_level": "C1",
        "module_type": "reading",
        "title": "Complex Evaluative Texts, Hedging & Counter-Arguments",
        "order_index": 3,
        "prerequisites": ["curric_b2_read_academic_arguments"],
        "estimated_minutes": 40,
        "objectives": [
            "Analyze dense, multifaceted academic texts across specialized domains.",
            "Decode epistemic hedging markers ('it appears plausible that', 'tends to indicate').",
            "Synthesize subtext, irony, and implicit stance in IELTS Academic Reading Passages 2 and 3."
        ],
        "explanation_markdown": """### Deconstructing Epistemic Hedging in Scholarly Writing
Scholarly authors rarely make unhedged, absolute claims. They qualify conclusions to reflect scientific caution:
- **Hedging verbs**: *suggest, indicate, imply, tend to, appear to*.
- **Modal qualifiers**: *may, might, could, arguably, conceivably*.
- **Attitudinal adverbs**: *ostensibly, ostensibly, reportedly, purportedly*.""",
        "examples": [
            {"text": "The data arguably points toward a correlation, though confounding variables preclude definitive causal claims.", "notes": "Sophisticated academic hedging."}
        ],
        "guided_exercises": [
            {"id": "c1_r_ge_1", "prompt": "If an author describes a theory as 'ostensibly plausible', does the author completely endorse it? (Yes/No)", "answer": "No", "explanation": "'Ostensibly' implies that while it appears plausible on the surface, deeper inspection may reveal flaws."}
        ],
        "interactive_practice": [
            {
                "id": "c1_r_ip_1",
                "question": "What is the rhetorical function of the phrase 'It is arguably premature to conclude...'?",
                "options": [
                    "To assert that the conclusion is definitely correct.",
                    "To urge caution against hasty deduction before complete evidence is assembled.",
                    "To agree with the previous speaker completely.",
                    "To state that time has expired."
                ],
                "correct_index": 1,
                "explanation": "It functions as an intellectual hedge cautioning against premature assertions."
            }
        ],
        "assessment": [
            {
                "id": "c1_r_as_1",
                "question": "PASSAGE: 'While advocates proclaim nanotechnology as a panacea for environmental degradation, critics contend that its ecological toxicity profile remains insufficiently characterized.' The author's tone toward nanotechnology is best described as:",
                "options": [
                    "Uncritically enthusiastic",
                    "Cautiously analytical and balanced",
                    "Dismissive and cynical",
                    "Apathetic"
                ],
                "correct_index": 1,
                "explanation": "The author juxtaposes promises against legitimate toxicity concerns, maintaining balanced scrutiny."
            }
        ]
    },
    {
        "id": "curric_c1_list_subtle_arguments",
        "cefr_level": "C1",
        "module_type": "listening",
        "title": "Nuanced Academic Debates & Implicit Speaker Attitudes",
        "order_index": 4,
        "prerequisites": ["curric_b2_list_lectures"],
        "estimated_minutes": 35,
        "objectives": [
            "Decode implicit attitudes, skepticism, and irony in rapid academic symposia and panel debates.",
            "Differentiate between consensus viewpoints and idiosyncratic dissenting opinions.",
            "Extract implicit conclusions from indirect communicative cues."
        ],
        "explanation_markdown": """### Detecting Tone, Stance, and Implicit Attitude
At C1, listening assessments test what is *implied* as well as what is stated:
- **Tone inflection**: A rising intonation on *'Indeed...'* may signal polite doubt rather than endorsement.
- **Rhetorical questions**: *'Are we truly to assume that resource consumption can expand infinitely?'* (Implies: No, obviously not).""",
        "examples": [
            {"text": "PROFESSOR: 'That is a rather daring hypothesis, to say the least.'", "notes": "British academic understatement implying the hypothesis is wildly unproven or reckless."}
        ],
        "guided_exercises": [
            {"id": "c1_l_ge_1", "prompt": "When a reviewer says 'The methodology leaves much to be desired', is the evaluation positive or negative?", "answer": "negative", "explanation": "'Leaves much to be desired' is an idiom indicating serious inadequacy."}
        ],
        "interactive_practice": [
            {
                "id": "c1_l_ip_1",
                "question": "SPEAKER: 'To term this initiative a success would be stretching the definition of the word.' The speaker believes the initiative was:",
                "options": [
                    "An unprecedented triumph",
                    "A distinct failure or disappointment",
                    "Grammatically difficult",
                    "Exceedingly profitable"
                ],
                "correct_index": 1,
                "explanation": "The understatement clarifies that the initiative was in fact not a success."
            }
        ],
        "assessment": [
            {
                "id": "c1_l_as_1",
                "question": "If a speaker introduces a point with 'With all due deference to the committee's findings...', what typically follows?",
                "options": [
                    "Total unqualified praise",
                    "A polite, formal critique or disagreement",
                    "An immediate resignation",
                    "A confirmation of unanimous voting"
                ],
                "correct_index": 1,
                "explanation": "'With all due deference' introduces polite formal disagreement or qualification."
            }
        ]
    },
    {
        "id": "curric_c1_write_academic_synthesis",
        "cefr_level": "C1",
        "module_type": "writing",
        "title": "Synthesizing Complex Data & Evaluative Argumentation",
        "order_index": 5,
        "prerequisites": ["curric_b2_write_peel_paragraph_technique"],
        "estimated_minutes": 40,
        "objectives": [
            "Synthesize multi-variable quantitative datasets in Academic Task 1 (trends, correlations, anomalies).",
            "Construct nuanced, non-binary arguments for Task 2 discussion essays.",
            "Achieve seamless lexical cohesion through nominalization and varied syntactic inversion."
        ],
        "explanation_markdown": """### Achieving Band 8.0+ in Task 2 Evaluative Essays
High-band writing transcends simple five-paragraph templates:
1. **Nuanced Thesis**: Avoid simplistic black-or-white claims; embrace dialectical synthesis (*'Although economic growth is indispensable for poverty alleviation, unfettered industrialization devoid of ecological safeguards proves self-defeating'*).
2. **Nominalization**: Converting verbs/adjectives into nouns enhances academic conciseness (*'Because the climate is warming rapidly, sea levels are rising'* -> *'Rapid climate warming has accelerated sea level rise'*).""",
        "examples": [
            {"text": "The proliferation of digital surveillance platforms has engendered acute apprehensions regarding civil liberties.", "notes": "Nominalization ('proliferation', 'apprehensions') produces authoritative academic register."}
        ],
        "guided_exercises": [
            {"id": "c1_w_ge_1", "prompt": "Nominalize: 'Scientists discovered the molecule, which allowed them to develop the drug.' -> 'The _____ of the molecule enabled drug development.'", "answer": "discovery", "explanation": "'discovered' nominalizes to 'discovery'."}
        ],
        "interactive_practice": [
            {
                "id": "c1_w_ip_1",
                "question": "Which sentence demonstrates the most sophisticated academic nominalization?",
                "options": [
                    "Because people moved to cities, factories grew very fast.",
                    "The rapid migration of agrarian populations to metropolitan centers catalyzed industrial expansion.",
                    "People moved to cities and factories became bigger because of that.",
                    "Factories expanded because city moving happened."
                ],
                "correct_index": 1,
                "explanation": "'migration ... catalyzed industrial expansion' is nominalized, precise, and academically elegant."
            }
        ],
        "assessment": [
            {
                "id": "c1_w_as_1",
                "question": "In IELTS Task 2, what distinguishes a Band 8 Task Response from Band 6?",
                "options": [
                    "Writing 600 words instead of 250.",
                    "Presenting a fully developed, nuanced response to all parts of the prompt with thoroughly elaborated arguments.",
                    "Using five idioms in every sentence.",
                    "Quoting famous philosophers throughout the text."
                ],
                "correct_index": 1,
                "explanation": "Band 8 requires a well-developed, nuanced response with relevant, extended, and supported ideas."
            }
        ]
    },
    {
        "id": "curric_c1_speak_discourse_markers",
        "cefr_level": "C1",
        "module_type": "speaking",
        "title": "Spoken Fluency Discourse Markers & Epistemic Stance",
        "order_index": 6,
        "prerequisites": ["curric_b2_speak_long_turns"],
        "estimated_minutes": 30,
        "objectives": [
            "Use natural spoken discourse markers to structure speech seamlessly without hesitation.",
            "Articulate an epistemic stance calibrating subjective doubt and certainty.",
            "Address complex abstract societal questions in IELTS Part 3 with spontaneity and precision."
        ],
        "explanation_markdown": """### Advanced Discourse Markers in Part 3
Discourse markers act as signposts guiding the listener through complex reasoning:
- **Structuring**: *In the first instance... / Looking at this from a broader perspective...*
- **Reformulation**: *Or to put it more accurately... / What I essentially mean to say is...*
- **Concession**: *That being said... / Be that as it may...*
- **Epistemic Stance**: *It strikes me as highly improbable that... / There is every likelihood that...*""",
        "examples": [
            {"text": "Be that as it may, one cannot overlook the ethical dilemmas inherent in genetic modification.", "notes": "'Be that as it may' executes a graceful concession."}
        ],
        "guided_exercises": [
            {"id": "c1_s_ge_1", "prompt": "Complete the concession: 'That _____ said, technology also presents distinct advantages.' (being / having)", "answer": "being", "explanation": "'That being said' is the standard transition."}
        ],
        "interactive_practice": [
            {
                "id": "c1_s_ip_1",
                "question": "Which discourse marker is most effective for reformulating an argument with greater precision?",
                "options": [
                    "Like, whatever...",
                    "Or to put it in more precise terms, ...",
                    "I talk again now...",
                    "Forget what I said..."
                ],
                "correct_index": 1,
                "explanation": "'Or to put it in more precise terms' signals an intentional refinement of thought."
            }
        ],
        "assessment": [
            {
                "id": "c1_s_as_1",
                "question": "In IELTS Speaking Part 3, how should a candidate handle an abstract speculative question about the future?",
                "options": [
                    "State that predicting the future is impossible and stay silent.",
                    "Use modal speculation ('It is conceivable that...', 'One potential trajectory is...') and explore multiple plausible scenarios.",
                    "Memorize a general quote about technology.",
                    "Answer with a simple 'Yes' or 'No'."
                ],
                "correct_index": 1,
                "explanation": "Part 3 evaluates the ability to speculate abstractly, analyze hypotheticals, and weigh probabilities."
            }
        ]
    },
    {
        "id": "curric_c1_pron_connected_speech",
        "cefr_level": "C1",
        "module_type": "pronunciation",
        "title": "Connected Speech: Elision, Assimilation & Intrusion",
        "order_index": 7,
        "prerequisites": ["curric_b2_pron_sentence_stress"],
        "estimated_minutes": 25,
        "objectives": [
            "Recognize and produce natural connected speech phenomena.",
            "Understand **Elision** (omission of sounds: 'next door' -> /neks dɔː/).",
            "Understand **Assimilation** (sounds influencing adjacent sounds: 'ten boys' -> /tem bɔɪz/).",
            "Produce intrusive glides (/r/, /j/, /w/) across vowel-vowel word boundaries."
        ],
        "explanation_markdown": """### The Mechanics of Connected Speech
Native English speech is not a string of isolated dictionary words; speech organs flow continuously:
1. **Linking /r/**: *car engine* -> /kɑːr ˈendʒɪn/
2. **Intrusive /j/**: *I agree* -> /aɪ j əˈɡriː/
3. **Intrusive /w/**: *Go out* -> /ɡəʊ w aʊt/
4. **Elision of /t/ and /d/**: *last night* -> /lɑːs naɪt/""",
        "examples": [
            {"text": "The idea of it (/ði aɪˈdɪər əv ɪt/) utilizes intrusive /r/.", "notes": "Intrusive /r/ bridges vowel hiatus."}
        ],
        "guided_exercises": [
            {"id": "c1_p_ge_1", "prompt": "Which intrusive glide sound links 'you are': /w/ or /j/?", "answer": "/w/", "explanation": "Rounding of the lips on /uː/ produces an intrusive /w/ glide before 'are'."}
        ],
        "interactive_practice": [
            {
                "id": "c1_p_ip_1",
                "question": "What phonetic process occurs when 'good boy' is pronounced /ɡʊb bɔɪ/?",
                "options": ["Elision", "Assimilation", "Epenthesis", "Aspiration"],
                "correct_index": 1,
                "explanation": "The alveolar /d/ assimilates to bilabial /b/ under the influence of the following consonant."
            }
        ],
        "assessment": [
            {
                "id": "c1_p_as_1",
                "question": "Why is awareness of connected speech critical for high-band IELTS Listening?",
                "options": [
                    "Examiners deduct points if candidates don't use British slang.",
                    "Words blend and reduce in rapid natural speech, making boundary recognition challenging without connected speech mastery.",
                    "All IELTS recordings are digitally sped up.",
                    "Spelling rules change when sounds link."
                ],
                "correct_index": 1,
                "explanation": "Connected speech changes the surface acoustic realization of words, making auditory decoding difficult without training."
            }
        ]
    },
    {
        "id": "curric_c1_func_scholarly_discourse",
        "cefr_level": "C1",
        "module_type": "functional",
        "title": "Academic Defenses, Panel Presentations & Critical Rebuttal",
        "order_index": 8,
        "prerequisites": ["curric_b2_func_negotiations"],
        "estimated_minutes": 35,
        "objectives": [
            "Deliver structured academic briefings and research paper defenses.",
            "Field hostile or skeptical questions from peers and examiners with intellectual composure.",
            "Formulate precise, evidenced rebuttals without personalizing disagreement."
        ],
        "explanation_markdown": """### Defending Research Intellectually
1. **Acknowledging the Question**:
   - *'That is a pertinent critique, and one that we grappled with extensively during initial methodology design.'*
2. **Defending Methodological Integrity**:
   - *'While I concede the sample size was bounded, the statistical power was corroborated through rigorous bootstrapping.'*
3. **Redirecting to Broader Findings**:
   - *'What is paramount, however, is that our primary findings remain robust across sensitivity analyses.'*""",
        "examples": [
            {"text": "SPEAKER: 'With respect to your observation on selection bias, our control group design explicitly accounted for that variable.'", "notes": "Scholarly defense."}
        ],
        "guided_exercises": [
            {"id": "c1_func_ge_1", "prompt": "Complete the phrase: 'Our findings remain _____ across multiple iterations.' (robust / strongness)", "answer": "robust", "explanation": "'robust' is the standard academic adjective for resilient findings."}
        ],
        "interactive_practice": [
            {
                "id": "c1_func_ip_1",
                "question": "Which response is most academically professional when a panelist challenges your survey methodology?",
                "options": [
                    "You clearly did not read my paper.",
                    "I appreciate that concern; however, we mitigated that potential bias by utilizing randomized stratified sampling.",
                    "My professor approved it, so it is correct.",
                    "I prefer not to discuss this question."
                ],
                "correct_index": 1,
                "explanation": "It addresses the critique substantively and explains the precise methodological safeguard."
            }
        ],
        "assessment": [
            {
                "id": "c1_func_as_1",
                "question": "What is the primary objective of an academic defense?",
                "options": [
                    "To win an argument at all costs.",
                    "To demonstrate intellectual rigor, transparent methodology, and reasoned defense of empirical conclusions.",
                    "To speak continuously without allowing interruptions.",
                    "To flatter the examining committee."
                ],
                "correct_index": 1,
                "explanation": "Academic defenses demonstrate methodological validity, rigor, and scholarly integrity."
            }
        ]
    },
    {
        "id": "curric_c1_rev_advanced_mastery",
        "cefr_level": "C1",
        "module_type": "review",
        "title": "C1 Advanced Level Review & Assessment",
        "order_index": 9,
        "prerequisites": ["curric_c1_gram_inversion", "curric_c1_write_academic_synthesis"],
        "estimated_minutes": 45,
        "objectives": [
            "Synthesize C1 inverted syntax, nominalization, academic collocations, and evaluative argumentation.",
            "Confirm readiness for Band 7.5–8.0 benchmarks in IELTS Academic.",
            "Prepare for C2 Mastery and Proficient English discourse."
        ],
        "explanation_markdown": """### C1 Milestone Review
At C1 (Effective Operational Proficiency), learners can understand a wide range of demanding, longer texts and recognize implicit meaning; express ideas fluently and spontaneously without much obvious searching for expressions; and produce clear, well-structured, detailed text on complex subjects showing controlled use of organizational patterns, connectors, and cohesive devices.""",
        "examples": [
            {"text": "C1 Mastery Benchmark: Flawless command of complex sentence structures, sophisticated lexical range, and academic discourse fluency.", "notes": "Official CEFR C1 descriptor."}
        ],
        "guided_exercises": [
            {"id": "c1_rev_ge_1", "prompt": "Invert: 'We rarely see such results.' -> 'Rarely _____ we see such results.'", "answer": "do", "explanation": "Present simple inversion: 'Rarely do we see...'"}
        ],
        "interactive_practice": [
            {
                "id": "c1_rev_ip_1",
                "question": "Select the sentence exhibiting the highest degree of grammatical sophistication and academic style:",
                "options": [
                    "If people don't recycle, pollution will be worse everywhere.",
                    "Seldom has the imperative for rigorous environmental stewardship been as pressing as in the contemporary epoch.",
                    "People really must recycle because pollution is getting so bad.",
                    "Under no circumstances pollution is good for anyone."
                ],
                "correct_index": 1,
                "explanation": "It seamlessly utilizes negative adverbial inversion ('Seldom has...') with advanced lexical resource."
            }
        ],
        "assessment": [
            {
                "id": "c1_rev_as_1",
                "question": "Which sentence contains a grammatical error in inversion?",
                "options": [
                    "Seldom have I encountered such dedication.",
                    "Not only did they achieve the target, but they also exceeded expectations.",
                    "Scarcely had she entered the room when the applause began.",
                    "Only after the audit was concluded the committee released the findings."
                ],
                "correct_index": 3,
                "explanation": "After 'Only after [clause]', the main clause MUST invert: 'did the committee release the findings'."
            }
        ]
    }
]

with open(os.path.join(CURRICULUM_DIR, "c1.json"), "w", encoding="utf-8") as f:
    json.dump(C1_LESSONS, f, indent=2, ensure_ascii=False)
print("Generated c1.json with", len(C1_LESSONS), "lessons.")


# -----------------------------------------------------------------------------
# C2 — PROFICIENT (9 Modules)
# -----------------------------------------------------------------------------
C2_LESSONS = [
    {
        "id": "curric_c2_gram_cleft_sentences",
        "cefr_level": "C2",
        "module_type": "grammar",
        "title": "Cleft Sentences & Discourse Topicalization",
        "order_index": 1,
        "prerequisites": ["curric_c1_gram_inversion"],
        "estimated_minutes": 40,
        "objectives": [
            "Construct 'It-clefts' (*It was X that Y*) and 'Wh-clefts' (*What X did was Y*) to calibrate information focus.",
            "Employ Reversed Wh-clefts and All-clefts (*All they wanted was clarity*) to elevate rhetorical elegance.",
            "Topicalize discourse themes dynamically across multi-clause complex sentences."
        ],
        "form_and_structure": "It-cleft: It + be + Focus + that/who + Clause. Wh-cleft: What/All + Clause + be + Focus. Reversed: Focus + be + What-clause.",
        "usage_rationale": "Used to explicitly direct reader cognitive attention toward a specific element of an argument, highlighting causality, responsibility, or contrast.",
        "positive_examples": [
            "It was the profound negligence of regulatory bodies that precipitated the catastrophic market contagion.",
            "What the experimental evidence undeniably demonstrates is the non-linear nature of thermodynamic dissipation."
        ],
        "negative_examples": [
            "It was the manager which made the decision. (Use 'that' or 'who' for persons).",
            "What happened was he forgot his notes. (Ensure grammatical concord across the copula verb)."
        ],
        "common_mistakes": [
            "Incorrect: 'What we need is more investments.' -> Correct: 'What we need are more investments' OR 'What we need is greater investment.'",
            "Incorrect: 'It was in 1999 when the law was passed.' -> In formal syntax: 'It was in 1999 that the law was passed.'"
        ],
        "confused_structures": [
            "It-cleft vs Pronoun 'It' dummy subject. An It-cleft can be collapsed back into a simple sentence without loss of semantic propositional content."
        ],
        "explanation_markdown": """### Cleft Sentences and Information Packaging
A cleft sentence 'cleaves' (divides) a single clause into two sections to highlight the new or contrastive information:
1. **It-cleft**:
   *Standard: Climate change drove the extinction event.*
   *Cleft: **It was climate change that** drove the extinction event.*
2. **Wh-cleft (Pseudo-cleft)**:
   *Standard: The administration neglected preventive healthcare.*
   *Cleft: **What the administration neglected was** preventive healthcare.*
3. **All-cleft**:
   ***All the researchers sought was** an equitable peer review.*""",
        "examples": [
            {"text": "It was precisely through longitudinal ethnographic inquiry that the sociologist unmasked systemic institutional bias.", "notes": "It-cleft focusing on the prepositional phrase of instrument."},
            {"text": "What remains deeply contentious among bioethicists is the permissibility of germline editing.", "notes": "Wh-cleft focusing on the contentious issue."}
        ],
        "guided_exercises": [
            {"id": "c2_ge_1", "prompt": "Transform into an It-cleft: 'Human error caused the disaster.' -> 'It was human error _____ caused the disaster.'", "answer": "that", "explanation": "It-clefts use 'that' (or 'which'/'who') to link the focus to the relative clause."}
        ],
        "interactive_practice": [
            {
                "id": "c2_ip_1",
                "question": "Which sentence represents a grammatically immaculate Wh-cleft?",
                "options": [
                    "What we discovered it was astonishing.",
                    "What surprised the investigative panel was the total absence of digital audit logs.",
                    "What that happened was bad.",
                    "What did the committee decide was unexpected."
                ],
                "correct_index": 1,
                "explanation": "'What surprised the investigative panel was [noun phrase]' represents flawless pseudo-cleft syntax."
            }
        ],
        "assessment": [
            {
                "id": "c2_as_1",
                "question": "Transform the following for maximum rhetorical focus on the methodology: 'Dr. Vance proved the hypothesis using cryogenic microscopy.'",
                "options": [
                    "Dr. Vance used cryogenic microscopy to prove the hypothesis.",
                    "It was by utilizing cryogenic microscopy that Dr. Vance substantiated the hypothesis.",
                    "Cryogenic microscopy was used by Dr. Vance.",
                    "The hypothesis was proven because cryogenic microscopy happened."
                ],
                "correct_index": 1,
                "explanation": "The It-cleft 'It was by utilizing cryogenic microscopy that...' directs precise focus onto the investigative methodology."
            }
        ],
        "review_questions": [
            "How does a pseudo-cleft differ structurally and rhetorically from an It-cleft?",
            "Why is 'that' preferred over 'when' in formal temporal It-clefts?"
        ]
    },
    {
        "id": "curric_c2_vocab_idiomatic_register",
        "cefr_level": "C2",
        "module_type": "vocabulary",
        "title": "Stylistic Register & Idiomatic Sophistication",
        "order_index": 2,
        "prerequisites": ["curric_c1_vocab_academic_collocations"],
        "estimated_minutes": 40,
        "objectives": [
            "Master rare, highly specific academic and intellectual vocabulary (*panacea, ubiquitous, watershed, ephemeral, visceral*).",
            "Command sophisticated metaphorical idioms without descending into conversational clichés.",
            "Calibrate stylistic register appropriately across legal, scholarly, literary, and diplomatic domains."
        ],
        "explanation_markdown": """### C2 Lexical Precision & Register Control
At C2, lexical choice demonstrates total command of semantic nuance, tone, and register:
- **Panacea**: A remedy for all difficulties (*e.g. 'Technology is no panacea for societal polarization'*).
- **Watershed moment**: A pivotal turning point (*e.g. 'The 2015 agreement marked a watershed in international climate diplomacy'*).
- **Sea change**: A profound transformation in perspective or policy.
- **Ubiquitous**: Present or found everywhere (*e.g. 'Smartphones have become ubiquitous across the globe'*).""",
        "examples": [
            {"text": "The discovery heralded a sea change in astrophysical paradigm modeling.", "notes": "'sea change' metaphorically depicts a sweeping structural transformation."}
        ],
        "guided_exercises": [
            {"id": "c2_v_ge_1", "prompt": "Which noun denotes a universal cure or solution: panacea or paradox?", "answer": "panacea", "explanation": "'panacea' means a universal remedy."}
        ],
        "interactive_practice": [
            {
                "id": "c2_v_ip_1",
                "question": "Which sentence uses idiomatic language appropriately for a formal academic treatise?",
                "options": [
                    "The politicians were beating around the bush big time.",
                    "The publication represented a watershed moment in the historiography of the industrial revolution.",
                    "The company bit off more than it could chew with that deal.",
                    "It was raining cats and dogs outside the laboratory."
                ],
                "correct_index": 1,
                "explanation": "'watershed moment in the historiography' is academically dignified, unlike colloquial clichés."
            }
        ],
        "assessment": [
            {
                "id": "c2_v_as_1",
                "question": "Select the most accurate synonym for 'ephemeral':",
                "options": ["Permanent", "Transitory and short-lived", "Substantial", "Destructive"],
                "correct_index": 1,
                "explanation": "'Ephemeral' means lasting for a very short time; transitory."
            }
        ]
    },
    {
        "id": "curric_c2_read_implicit_author_stance",
        "cefr_level": "C2",
        "module_type": "reading",
        "title": "Deconstructing Irony, Hedging & Implicit Author Stance",
        "order_index": 3,
        "prerequisites": ["curric_c1_read_complex_texts"],
        "estimated_minutes": 45,
        "objectives": [
            "Deconstruct satire, irony, intellectual detachment, and implicit skepticism in complex prose.",
            "Analyze dense syntactic embeddings, parenthetical qualifications, and rhetorical questions.",
            "Achieve complete accuracy in the most challenging IELTS Academic Passage 3 inference tasks."
        ],
        "explanation_markdown": """### Navigating Deep Implicit Meaning
Proficient reading requires interpreting what remains unsaid:
- **Understatement**: Expressing a monumental critique through restrained praise (*'The author's arguments are not without a certain naive charm'* -> Translation: The arguments are fundamentally flawed and simplistic).
- **Rhetorical Incongruity**: Deliberate juxtaposition of elevated diction with mundane reality to mock pretension.""",
        "examples": [
            {"text": "CRITIC: 'One cannot help but admire the sheer audacity of asserting that such correlation constitutes proof.'", "notes": "Ironic framing dismissing the claim as baseless arrogance."}
        ],
        "guided_exercises": [
            {"id": "c2_r_ge_1", "prompt": "If a reviewer writes 'The proposal is ambitious, if entirely unencumbered by economic reality', is the review favorable? (Yes/No)", "answer": "No", "explanation": "'Unencumbered by economic reality' is an intellectual critique meaning hopelessly impractical."}
        ],
        "interactive_practice": [
            {
                "id": "c2_r_ip_1",
                "question": "TEXT: 'To claim that market forces alone will resolve environmental degradation requires a leap of faith that few sober economists are willing to take.' What is the author's stance?",
                "options": [
                    "Market forces are fully capable of solving environmental issues.",
                    "Relying solely on market forces is an irrational and perilous strategy.",
                    "Economists are universally religious.",
                    "Environmental issues are solved."
                ],
                "correct_index": 1,
                "explanation": "'requires a leap of faith that few sober economists are willing to take' rejects the proposition as irrational."
            }
        ],
        "assessment": [
            {
                "id": "c2_r_as_1",
                "question": "Which literary device is employed when an academic writes: 'The committee’s exhaustive five-year investigation produced the breathtaking insight that water is, indeed, wet'?",
                "options": [
                    "Metaphor",
                    "Hyperbolic sarcasm / irony",
                    "Alliteration",
                    "Onomatopoeia"
                ],
                "correct_index": 1,
                "explanation": "The author utilizes hyperbolic irony to satirize an expensive study that yielded trivial, obvious results."
            }
        ]
    },
    {
        "id": "curric_c2_list_dense_lectures",
        "cefr_level": "C2",
        "module_type": "listening",
        "title": "Deconstructing Dense Multi-Perspective Academic Symposia",
        "order_index": 4,
        "prerequisites": ["curric_c1_list_subtle_arguments"],
        "estimated_minutes": 40,
        "objectives": [
            "Follow unscripted, fast-paced academic exchanges featuring overlapping dialogue and rapid shifts in register.",
            "Identify allegorical references, cultural idioms, and subtle acoustic sarcasm.",
            "Record complex abstract frameworks under intense time pressure."
        ],
        "explanation_markdown": """### Mastery of High-Speed Natural Speech
At C2, listening materials incorporate natural unscripted traits:
- **Speech rate**: Rapid tempo exceeding 160–180 words per minute.
- **Overlapping discourse**: Speakers interrupting, modifying, or building on peer contributions.
- **Abstract conceptual frameworks**: Unpacking theoretical jargon across interdisciplinary fields.""",
        "examples": [
            {"text": "PANELIST: 'While Dr. Evans’ thesis appears plausible prima facie, it crumbles the moment one introduces non-equilibrium dynamics.'", "notes": "Rapid critique drawing on Latinate academic terminology."}
        ],
        "guided_exercises": [
            {"id": "c2_l_ge_1", "prompt": "What does 'prima facie' mean in academic discourse? (at first sight / never)", "answer": "at first sight", "explanation": "'prima facie' means based on initial impression before closer investigation."}
        ],
        "interactive_practice": [
            {
                "id": "c2_l_ip_1",
                "question": "In a recorded debate, a speaker chuckles softly and murmurs 'Indeed.' What is the most probable meaning in academic context?",
                "options": [
                    "Complete enthusiasm and agreement",
                    "Polite, skeptical irony doubting the validity of the previous speaker's claim",
                    "The speaker has fallen asleep",
                    "A request for coffee"
                ],
                "correct_index": 1,
                "explanation": "A chuckle accompanying a soft 'Indeed' conveys polite academic skepticism."
            }
        ],
        "assessment": [
            {
                "id": "c2_l_as_1",
                "question": "What is the primary listening strategy for tracking multi-perspective symposia?",
                "options": [
                    "Attempting to transcribe every spoken word verbatim.",
                    "Mapping speakers to their conceptual paradigms and tracking where they agree or diverge.",
                    "Closing your eyes and guessing at the end.",
                    "Focusing solely on numerical dates."
                ],
                "correct_index": 1,
                "explanation": "Tracking conceptual frameworks and inter-speaker divergence allows accurate comprehension of high-level discourse."
            }
        ]
    },
    {
        "id": "curric_c2_write_stylistic_flair",
        "cefr_level": "C2",
        "module_type": "writing",
        "title": "Stylistic Nuance, Subtlety & Rhetorical Elegance",
        "order_index": 5,
        "prerequisites": ["curric_c1_write_academic_synthesis"],
        "estimated_minutes": 45,
        "objectives": [
            "Produce prose marked by syntactic flexibility, varied sentence length, and rhetorical rhythm.",
            "Integrate advanced figurative devices, balanced antitheses, and periodic sentences.",
            "Attain flawless Band 9 performance in IELTS Academic Task 2 essays."
        ],
        "explanation_markdown": """### The Anatomy of Band 9.0 Prose
Band 9 prose reads with effortless fluency and natural authorial voice:
1. **Rhythmic Cadence**: Alternating between expansive periodic sentences and punchy, decisive assertions.
2. **Antithesis**: Balancing contrasting ideas in parallel grammatical structures (*'Not because the task is facile, but because the stakes are existential'*).
3. **Flawless Precision**: Utilizing the exact word with zero awkwardness or semantic mismatch.""",
        "examples": [
            {"text": "To dismantle these structural impediments requires not merely financial capitalization, but an overhaul of institutional culture itself.", "notes": "Balanced antithesis elevating persuasive impact."}
        ],
        "guided_exercises": [
            {"id": "c2_w_ge_1", "prompt": "Complete the antithesis: 'Not for private enrichment, but for the _____ good.' (public / commonness)", "answer": "public", "explanation": "'the public good' forms the natural parallel antithesis."}
        ],
        "interactive_practice": [
            {
                "id": "c2_w_ip_1",
                "question": "Which sentence achieves the most compelling rhetorical impact for an essay conclusion?",
                "options": [
                    "In conclusion, I think education is good and we should pay for it.",
                    "Ultimately, the preservation of academic independence is not merely an institutional luxury; it is the cornerstone upon which democratic resilience itself is erected.",
                    "To summarize, universities need money from taxes to do work.",
                    "Finally, all arguments show that studying is helpful."
                ],
                "correct_index": 1,
                "explanation": "It demonstrates grand rhetorical balance, metaphoric elevation, and authoritative finality."
            }
        ],
        "assessment": [
            {
                "id": "c2_w_as_1",
                "question": "In the IELTS Band Descriptors, what characterizes Band 9 for Grammatical Range and Accuracy?",
                "options": [
                    "Using passive voice in every single sentence.",
                    "Uses a wide range of structures with full flexibility and accuracy; rare minor errors occur only as 'slips'.",
                    "Writing sentences that exceed 60 words.",
                    "Avoiding all complex sentences."
                ],
                "correct_index": 1,
                "explanation": "Band 9 requires full flexibility, effortless accuracy, and wide structural variety with only rare slips."
            }
        ]
    },
    {
        "id": "curric_c2_speak_spontaneous_debate",
        "cefr_level": "C2",
        "module_type": "speaking",
        "title": "Spontaneous Argumentation, Sophisticated Discourse & Fluency",
        "order_index": 6,
        "prerequisites": ["curric_c1_speak_discourse_markers"],
        "estimated_minutes": 35,
        "objectives": [
            "Engage in spontaneous, unhesitating intellectual debate on contentious abstract subjects.",
            "Handle adversarial cross-examination with poise, humor, and analytical depth.",
            "Achieve effortless Band 9 speaking performance characterized by natural idiomatic precision."
        ],
        "explanation_markdown": """### Band 9 Spoken Fluency Dynamics
Band 9 speaking is indistinguishable from an articulate, educated native speaker:
- **Zero search for language**: Any hesitation is content-related (thinking *what* to say, not *how* to say it).
- **Subtle humor & irony**: Employing gentle understatement or wit when appropriate.
- **Rhetorical scaffolding**: Framing answers with instant structural cohesion (*'There are two distinct angles from which this dilemma must be scrutinized...'*).""",
        "examples": [
            {"text": "That is an intriguing proposition; however, if one peels back the rhetorical veneer, the empirical premise proves tenuous at best.", "notes": "Spontaneous academic debate phrasing."}
        ],
        "guided_exercises": [
            {"id": "c2_s_ge_1", "prompt": "Complete the metaphor: 'If one peels back the _____ veneer...' (rhetorical / wordy)", "answer": "rhetorical", "explanation": "'rhetorical veneer' is an advanced metaphor for superficial argumentation."}
        ],
        "interactive_practice": [
            {
                "id": "c2_s_ip_1",
                "question": "What separates Band 9 Fluency from Band 7 in IELTS Speaking?",
                "options": [
                    "Speaking as fast as humanly possible.",
                    "Fluency is completely natural; any hesitation is content-based to formulate ideas, with full coherence throughout.",
                    "Never pausing even to breathe.",
                    "Memorizing long passages from textbooks."
                ],
                "correct_index": 1,
                "explanation": "Band 9 hesitations are purely conceptual (thinking about ideas), never linguistic (searching for words or grammar)."
            }
        ],
        "assessment": [
            {
                "id": "c2_s_as_1",
                "question": "When challenged by an examiner with a provocative counter-example in Part 3, the ideal Band 9 response is:",
                "options": [
                    "Admit that you are wrong immediately.",
                    "Acknowledge the validity of the anomaly, contextualize it, and integrate it into a more comprehensive thesis.",
                    "Argue aggressively with the examiner.",
                    "Repeat your previous answer word for word."
                ],
                "correct_index": 1,
                "explanation": "Integrating counter-examples into a broader synthesis demonstrates intellectual maturity and linguistic agility."
            }
        ]
    },
    {
        "id": "curric_c2_pron_prosody_intonation",
        "cefr_level": "C2",
        "module_type": "pronunciation",
        "title": "Intonational Nuance, Attitudinal Pacing & Voice Modulation",
        "order_index": 7,
        "prerequisites": ["curric_c1_pron_connected_speech"],
        "estimated_minutes": 30,
        "objectives": [
            "Command subtle pitch contours (fall-rise, rise-fall) to convey nuance, reservation, and irony.",
            "Modulate tempo and micro-pausing to emphasize key rhetorical assertions.",
            "Eliminate monotonous cadence and achieve total prosodic expressiveness."
        ],
        "explanation_markdown": """### Pitch Contours and Attitudinal Intonation
In English, pitch direction conveys attitude and certainty:
1. **Falling Intonation (↘)**: Finality, certainty, factual assertion (*The experiment is complete. ↘*).
2. **Rising Intonation (↗)**: Questions, invitations to respond (*Are you certain? ↗*).
3. **Fall-Rise Intonation (↘↗)**: Reservation, conditional doubt, polite warning (*Well, technically that is true... ↘↗ [but practically unfeasible]*).
4. **Rise-Fall Intonation (↗↘)**: Strong emotional impression, surprise, or profound conviction (*Fascinating! ↗↘*).""",
        "examples": [
            {"text": "I can do it on Tuesday (fall-rise) implies: ...but Wednesday would be much better for me.", "notes": "Fall-rise conveys reservation."}
        ],
        "guided_exercises": [
            {"id": "c2_p_ge_1", "prompt": "Which pitch contour indicates doubt or reservation: falling or fall-rise?", "answer": "fall-rise", "explanation": "The fall-rise contour (↘↗) signals reservation or unstated conditions."}
        ],
        "interactive_practice": [
            {
                "id": "c2_p_ip_1",
                "question": "What does a fall-rise tone on the word 'possible' indicate in: 'It is possible... ↘↗'?",
                "options": [
                    "100% certainty that it will happen.",
                    "The speaker concedes possibility, but harbors severe doubts or reservations.",
                    "The speaker is asking a question.",
                    "The speaker has completed their entire thought."
                ],
                "correct_index": 1,
                "explanation": "Fall-rise intonation signals a concession tempered with skepticism or reservation."
            }
        ],
        "assessment": [
            {
                "id": "c2_p_as_1",
                "question": "What is the primary characteristic of Band 9 Pronunciation in IELTS?",
                "options": [
                    "Having an exaggerated Upper-Class English accent.",
                    "Uses a full range of phonological features with complete flexibility, subtle nuance, and effortless intelligibility throughout.",
                    "Speaking very loudly.",
                    "Omitting all unstressed vowels completely."
                ],
                "correct_index": 1,
                "explanation": "Band 9 requires effortless intelligibility, full flexibility of phonological features, and nuanced expressiveness."
            }
        ]
    },
    {
        "id": "curric_c2_func_high_stakes_negotiation",
        "cefr_level": "C2",
        "module_type": "functional",
        "title": "Diplomatic Discourse, High-Level Mediation & Global Advocacy",
        "order_index": 8,
        "prerequisites": ["curric_c1_func_scholarly_discourse"],
        "estimated_minutes": 40,
        "objectives": [
            "Facilitate multilateral diplomatic mediation and resolve complex impasses.",
            "Draft and deliver binding executive resolutions and consensus communiqués.",
            "Deploy consummate diplomatic tact under high-stakes adversarial conditions."
        ],
        "explanation_markdown": """### The Lexicon of International Diplomacy & Mediation
High-stakes mediation requires language that bridges irreconcilable viewpoints:
- **Strategic Ambiguity**: Phrasing agreements so both parties can claim victory (*'Constructive ambiguity'*).
- **De-escalation**: *'Let us set aside peripheral grievances to concentrate upon fundamental mutual interests.'*
- **Finalizing Protocols**: *'Subject to bilateral ratification, this protocol enshrines mutual compliance.'*""",
        "examples": [
            {"text": "MEDIATOR: 'While ideological positions diverge, our shared imperative remains the prevention of humanitarian fallout.'", "notes": "Diplomatic consensus building."}
        ],
        "guided_exercises": [
            {"id": "c2_func_ge_1", "prompt": "Complete the diplomatic phrase: 'To build a _____ between our nations...' (bridge / wall)", "answer": "bridge", "explanation": "'build a bridge' is standard diplomatic imagery for reconciliation."}
        ],
        "interactive_practice": [
            {
                "id": "c2_func_ip_1",
                "question": "Which statement demonstrates master-level diplomatic mediation?",
                "options": [
                    "Party A is wrong and Party B is right.",
                    "While acknowledging the legitimate historical grievances articulated by both delegations, our current mandate necessitates forging a forward-looking framework for peaceful co-existence.",
                    "Stop arguing or we leave the room.",
                    "Nobody gets what they want today."
                ],
                "correct_index": 1,
                "explanation": "It balances past grievances while firmly reorienting focus toward a collaborative future mandate."
            }
        ],
        "assessment": [
            {
                "id": "c2_func_as_1",
                "question": "In international treaty drafting, what does a 'caveat' represent?",
                "options": [
                    "A celebration banquet",
                    "A formal condition, limitation, or warning qualifying an agreement",
                    "A declaration of war",
                    "An economic subsidy"
                ],
                "correct_index": 1,
                "explanation": "A caveat is a formal stipulation or qualifying limitation."
            }
        ]
    },
    {
        "id": "curric_c2_rev_proficiency_mastery",
        "cefr_level": "C2",
        "module_type": "review",
        "title": "C2 Proficiency Level Review & Comprehensive Assessment",
        "order_index": 9,
        "prerequisites": ["curric_c2_gram_cleft_sentences", "curric_c2_write_stylistic_flair"],
        "estimated_minutes": 50,
        "objectives": [
            "Synthesize full C2 English proficiency across all 9 academic domains.",
            "Demonstrate total command of cleft syntax, stylistic register, and implicit rhetorical nuance.",
            "Certify readiness for native-equivalent IELTS Band 8.5–9.0 academic and professional performance."
        ],
        "explanation_markdown": """### C2 Mastery Milestone
At C2 (Mastery), the learner can understand with ease virtually everything heard or read; summarize information from different spoken and written sources, reconstructing arguments and accounts in a coherent presentation; and express themselves spontaneously, very fluently and precisely, differentiating finer shades of meaning even in the most complex situations.""",
        "examples": [
            {"text": "C2 Mastery Summit: The pinnacle of English language learning, enabling seamless participation in global academia, diplomacy, and professional leadership.", "notes": "Official CEFR C2 Mastery descriptor."}
        ],
        "guided_exercises": [
            {"id": "c2_rev_ge_1", "prompt": "Form an It-cleft: 'Dr. Jones formulated the theory.' -> 'It was Dr. Jones _____ formulated the theory.'", "answer": "who", "explanation": "'who' or 'that' completes the It-cleft focusing on Dr. Jones."}
        ],
        "interactive_practice": [
            {
                "id": "c2_rev_ip_1",
                "question": "Which sentence embodies flawless C2 stylistic sophistication and syntactical agility?",
                "options": [
                    "What the comprehensive data demonstrates is that only through systemic decarbonization can modern industrial societies avert environmental catastrophe.",
                    "If we don't stop polluting the world will suffer a lot.",
                    "It was environmental catastrophe that was caused because people polluted.",
                    "Only through systemic decarbonization modern societies can avert disaster."
                ],
                "correct_index": 0,
                "explanation": "It combines a Wh-cleft ('What the data demonstrates is...') with negative adverbial inversion ('only through... can modern societies avert...')."
            }
        ],
        "assessment": [
            {
                "id": "c2_rev_as_1",
                "question": "Which sentence correctly applies an It-cleft to emphasize the cause of the failure?",
                "options": [
                    "The failure happened because the team lacked funding.",
                    "It was a severe lack of funding that precipitated the project's ultimate collapse.",
                    "Because of funding was lacking, the project failed.",
                    "What failed was the project because of money."
                ],
                "correct_index": 1,
                "explanation": "'It was a severe lack of funding that precipitated...' places unmistakable, authoritative emphasis on the underlying cause."
            }
        ]
    }
]

with open(os.path.join(CURRICULUM_DIR, "c2.json"), "w", encoding="utf-8") as f:
    json.dump(C2_LESSONS, f, indent=2, ensure_ascii=False)
print("Generated c2.json with", len(C2_LESSONS), "lessons.")
