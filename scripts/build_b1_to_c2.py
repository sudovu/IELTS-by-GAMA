"""
build_b1_to_c2.py
Generates B1, B2, C1, and C2 curriculum JSON files with 9 modules each.
Preserves existing starter lesson IDs and expands with comprehensive instructional design.
"""

import os
import json

CURRICULUM_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "curriculum")
os.makedirs(CURRICULUM_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# B1 — INTERMEDIATE (9 Modules)
# -----------------------------------------------------------------------------
B1_LESSONS = [
    {
        "id": "curric_b1_gram_present_perfect",
        "cefr_level": "B1",
        "module_type": "grammar",
        "title": "Present Perfect vs. Past Simple Distinction",
        "order_index": 1,
        "prerequisites": ["curric_a2_gram_past_simple"],
        "estimated_minutes": 30,
        "objectives": [
            "Distinguish between completed past events (Past Simple) and past actions with current relevance (Present Perfect).",
            "Use temporal markers ('since', 'for', 'already', 'yet', 'just') with grammatical precision.",
            "Formulate experiential queries with 'Have you ever...'."
        ],
        "form_and_structure": "Subject + have/has + Past Participle (V3). Negative: have/has not (haven't/hasn't) + V3. Question: Have/has + subject + V3?",
        "usage_rationale": "Used for actions that occurred at an indefinite time, ongoing states connecting past to present, or actions with present consequences.",
        "positive_examples": [
            "Scientists have discovered a novel antibiotic in soil bacteria.",
            "She has lived in Cambridge since October 2021."
        ],
        "negative_examples": [
            "They have not published the official findings yet.",
            "He has not completed his dissertation draft."
        ],
        "common_mistakes": [
            "Incorrect: 'I have seen him yesterday.' -> Correct: 'I saw him yesterday.' (Specific past time markers forbid Present Perfect).",
            "Incorrect: 'She lives here since two years.' -> Correct: 'She has lived here for two years.'"
        ],
        "confused_structures": [
            "'For' (duration: for five years) vs 'Since' (starting point: since 2019).",
            "'Been to' (visited and returned) vs 'Gone to' (currently still there)."
        ],
        "explanation_markdown": """### Present Perfect vs. Past Simple Mechanics
1. **Past Simple**: Used when the event is locked in a finished time period (*in 1998, last week, three days ago*).
2. **Present Perfect**: Used for events connected to the present moment, lifetime experiences, or unfinished time periods (*this week, recently, ever*).""",
        "examples": [
            {"text": "Dr. Aris has published twenty journal articles throughout his career.", "notes": "Ongoing lifetime accomplishment (he is still alive and writing)."},
            {"text": "Alexander Fleming discovered penicillin in 1928.", "notes": "Historical completed event in a finished past year."}
        ],
        "guided_exercises": [
            {"id": "b1_ge_1", "prompt": "She _____ (live) in Manchester for three years, and she still loves it.", "answer": "has lived", "explanation": "Unfinished state continuing into the present requires Present Perfect."}
        ],
        "interactive_practice": [
            {
                "id": "b1_ip_1",
                "question": "Which sentence demonstrates the correct use of tense?",
                "options": [
                    "I have visited Kyoto last summer.",
                    "I visited Kyoto last summer.",
                    "I have visit Kyoto last summer.",
                    "I am visiting Kyoto last summer."
                ],
                "correct_index": 1,
                "explanation": "'last summer' is a closed past time frame, demanding Past Simple 'visited'."
            }
        ],
        "assessment": [
            {
                "id": "b1_as_1",
                "question": "Select the correct option: 'The engineers _____ the structural inspection yet.'",
                "options": [
                    "haven't finished",
                    "didn't finished",
                    "haven't finish",
                    "don't finish"
                ],
                "correct_index": 0,
                "explanation": "'yet' in negative statements requires Present Perfect: 'haven't finished'."
            }
        ],
        "review_questions": [
            "Why is 'I have graduated university in 2020' grammatically incorrect?",
            "What is the difference between 'has been to Rome' and 'has gone to Rome'?"
        ]
    },
    {
        "id": "curric_b1_vocab_workplace_education",
        "cefr_level": "B1",
        "module_type": "vocabulary",
        "title": "Workplace Dynamics, Careers & Higher Education",
        "order_index": 2,
        "prerequisites": ["curric_a2_vocab_travel_transport"],
        "estimated_minutes": 25,
        "objectives": [
            "Deploy professional terminology for career progression, qualifications, and workplace roles.",
            "Distinguish between 'job', 'work', 'career', 'occupation', and 'profession'.",
            "Use collocations for higher education ('enroll in', 'graduate from', 'major in', 'conduct research')."
        ],
        "explanation_markdown": """### Career & Academic Lexis
- **Occupation**: Broad category of employment (*e.g. medical practitioner*).
- **Profession**: An occupation requiring specialized prolonged training and academic credentials (*e.g. surgeon, barrister*).
- **Collocations**: *meet deadlines, acquire skills, career prospects, tertiary education*.""",
        "examples": [
            {"text": "Graduates with STEM degrees possess enhanced career prospects in global markets.", "notes": "'Career prospects' refers to future advancement possibilities."}
        ],
        "guided_exercises": [
            {"id": "b1_v_ge_1", "prompt": "She decided to _____ (enroll / apply) in the master's degree program.", "answer": "enroll", "explanation": "One enrolls 'in' a course or university program."}
        ],
        "interactive_practice": [
            {
                "id": "b1_v_ip_1",
                "question": "Which noun is uncountable in English?",
                "options": ["job", "profession", "work", "career"],
                "correct_index": 2,
                "explanation": "'work' is generally uncountable (e.g. 'I have a lot of work to do today')."
            }
        ],
        "assessment": [
            {
                "id": "b1_v_as_1",
                "question": "Complete the phrase: 'Candidates must be capable of working under pressure to _____ tight deadlines.'",
                "options": ["catch", "meet", "hold", "take"],
                "correct_index": 1,
                "explanation": "The idiomatic professional collocation is 'meet deadlines'."
            }
        ]
    },
    {
        "id": "curric_b1_read_factual_articles",
        "cefr_level": "B1",
        "module_type": "reading",
        "title": "Factual Articles & Paraphrase Recognition",
        "order_index": 3,
        "prerequisites": ["curric_a2_read_scanning_notices"],
        "estimated_minutes": 30,
        "objectives": [
            "Read intermediate informational articles and identify paragraph main ideas.",
            "Recognize lexical paraphrasing and synonym replacement between text and questions.",
            "Understand cohesive referencing words ('this phenomenon', 'such measures', 'the former')."
        ],
        "explanation_markdown": """### Paraphrase Recognition in Reading
Examinations rarely repeat the exact words from the question in the text:
- Question: *The project received financial backing from the state.*
- Passage: *Government subsidies funded the initiative.*
Recognizing that *financial backing* = *subsidies* and *state* = *government* is fundamental to comprehension.""",
        "examples": [
            {"text": "TEXT: 'Automated vehicles reduce traffic accidents.' PARAPHRASE: 'Self-driving cars decrease collisions.'", "notes": "Demonstrates synonym mapping."}
        ],
        "guided_exercises": [
            {"id": "b1_r_ge_1", "prompt": "Find the synonym for 'significant growth' in: 'The firm experienced a massive expansion.'", "answer": "massive expansion", "explanation": "'significant growth' maps directly to 'massive expansion'."}
        ],
        "interactive_practice": [
            {
                "id": "b1_r_ip_1",
                "question": "If a text states 'Consumption of fossil fuels plummeted', what happened to fuel usage?",
                "options": [
                    "It increased moderately.",
                    "It dropped dramatically.",
                    "It stayed constant.",
                    "It fluctuated unpredictably."
                ],
                "correct_index": 1,
                "explanation": "'Plummet' means to fall rapidly and sharply."
            }
        ],
        "assessment": [
            {
                "id": "b1_r_as_1",
                "question": "Which pair represents an accurate academic paraphrase?",
                "options": [
                    "'solve a problem' -> 'exacerbate a dilemma'",
                    "'mitigate the risk' -> 'reduce the danger'",
                    "'prohibit an activity' -> 'encourage an action'",
                    "'accelerate the process' -> 'delay the timeline'"
                ],
                "correct_index": 1,
                "explanation": "'mitigate the risk' means to reduce the danger."
            }
        ]
    },
    {
        "id": "curric_b1_list_discussions",
        "cefr_level": "B1",
        "module_type": "listening",
        "title": "Following Workplace & Academic Discussions",
        "order_index": 4,
        "prerequisites": ["curric_a2_list_conversations"],
        "estimated_minutes": 25,
        "objectives": [
            "Follow discussions between two or three speakers discussing schedules and projects.",
            "Identify agreement, concession, and disagreement markers ('I see your point, but...', 'Exactly').",
            "Take structured notes during an audio briefing."
        ],
        "explanation_markdown": """### Tracking Multi-Speaker Conversations
When multiple speakers converse:
1. Identify who holds which viewpoint.
2. Listen for transition cues:
   - Agreement: *'Absolutely', 'I couldn't agree more', 'Precisely'.*
   - Disagreement: *'I'm not so sure about that', 'On the other hand', 'True, but...'.*""",
        "examples": [
            {"text": "SPEAKER A: 'We should postpone the seminar.' SPEAKER B: 'I agree, the hall is booked.'", "notes": "Clear agreement consensus."}
        ],
        "guided_exercises": [
            {"id": "b1_l_ge_1", "prompt": "Does the speaker agree or disagree: 'I take your point, but cost is an issue.'", "answer": "disagree", "explanation": "'I take your point, but...' expresses partial concession followed by disagreement."}
        ],
        "interactive_practice": [
            {
                "id": "b1_l_ip_1",
                "question": "What does 'I couldn't agree more' indicate?",
                "options": ["Complete disagreement", "Complete agreement", "Neutrality", "Confusion"],
                "correct_index": 1,
                "explanation": "'I couldn't agree more' means 100% full agreement."
            }
        ],
        "assessment": [
            {
                "id": "b1_l_as_1",
                "question": "PROFESSOR: 'The assignment was due on Monday, but because of the holiday, you have until Wednesday midnight.' Final deadline is:",
                "options": ["Monday 5 PM", "Wednesday midnight", "Holiday morning", "Next week"],
                "correct_index": 1,
                "explanation": "The extension sets the final deadline to Wednesday midnight."
            }
        ]
    },
    {
        "id": "curric_b1_write_cohesion_linkers",
        "cefr_level": "B1",
        "module_type": "writing",
        "title": "Paragraph Architecture & Cohesive Discourse Linkers",
        "order_index": 5,
        "prerequisites": ["curric_a2_write_informal_emails"],
        "estimated_minutes": 30,
        "objectives": [
            "Structure logical paragraphs using Topic Sentence, Supporting Explanation, and Example.",
            "Master cohesive discourse linkers of addition ('furthermore'), contrast ('however'), and result ('consequently').",
            "Eliminate run-on sentences and comma splices."
        ],
        "explanation_markdown": """### Cohesive Paragraph Structure
A strong paragraph maintains thematic focus:
1. **Topic Sentence**: Introduces the central argument.
2. **Supporting Elaboration**: Explains *why* or *how*.
3. **Evidence / Example**: Cites a concrete case (*For instance, ...*).
4. **Linkers**:
   - Contrast: *However, In contrast, On the contrary*.
   - Result: *Therefore, Consequently, As a result*.
   - Addition: *Furthermore, Moreover, In addition*.""",
        "examples": [
            {"text": "Public transit reduces traffic congestion. Furthermore, it significantly curbs urban carbon emissions.", "notes": "'Furthermore' introduces a synergistic supplementary point."}
        ],
        "guided_exercises": [
            {"id": "b1_w_ge_1", "prompt": "Insert the linker of result: 'The battery failed; _____, the device shut down.' (consequently / however)", "answer": "consequently", "explanation": "'consequently' introduces the logical consequence."}
        ],
        "interactive_practice": [
            {
                "id": "b1_w_ip_1",
                "question": "Which linker indicates an addition to an existing argument?",
                "options": ["Nevertheless", "Consequently", "Moreover", "Whereas"],
                "correct_index": 2,
                "explanation": "'Moreover' adds supplementary supportive evidence."
            }
        ],
        "assessment": [
            {
                "id": "b1_w_as_1",
                "question": "Select the correct punctuation for transition words joining independent clauses:",
                "options": [
                    "Solar power is clean, however it is weather-dependent.",
                    "Solar power is clean; however, it is weather-dependent.",
                    "Solar power is clean however, it is weather-dependent.",
                    "Solar power is clean; however it is weather-dependent."
                ],
                "correct_index": 1,
                "explanation": "Semicolon before transition adverb, comma after: '; however,'."
            }
        ]
    },
    {
        "id": "curric_b1_speak_opinions",
        "cefr_level": "B1",
        "module_type": "speaking",
        "title": "Expressing Opinions, Agreement & Disagreement",
        "order_index": 6,
        "prerequisites": ["curric_a2_speak_narrating_events"],
        "estimated_minutes": 25,
        "objectives": [
            "Express personal perspectives with appropriate degree of certainty ('In my view', 'I am convinced that').",
            "Politely qualify opinions with concession phrases ('While that may be true, I believe...').",
            "Sustain spoken answers for 45–60 seconds without long hesitations."
        ],
        "explanation_markdown": """### Formulating Opinions in Spoken English
Move beyond simple *'I think'*:
- **Strong Stance**: *I firmly believe that... / It is obvious that...*
- **Balanced Stance**: *From my perspective... / As far as I am concerned...*
- **Concession**: *I understand why people argue X; nevertheless, I maintain that Y...*""",
        "examples": [
            {"text": "In my view, online education offers tremendous flexibility, although practical laboratory work still requires in-person attendance.", "notes": "Balanced opinion with concession."}
        ],
        "guided_exercises": [
            {"id": "b1_s_ge_1", "prompt": "Complete the phrase: 'As far as I am _____, public libraries remain essential.' (concerned / considered)", "answer": "concerned", "explanation": "The set phrase is 'As far as I am concerned'."}
        ],
        "interactive_practice": [
            {
                "id": "b1_s_ip_1",
                "question": "Which phrase is most suitable for introducing a balanced, professional opinion in IELTS Speaking Part 3?",
                "options": [
                    "Like, you know...",
                    "From my perspective, ...",
                    "I tell you that...",
                    "Everybody knows..."
                ],
                "correct_index": 1,
                "explanation": "'From my perspective' is academically appropriate and natural."
            }
        ],
        "assessment": [
            {
                "id": "b1_s_as_1",
                "question": "When conceding a point before stating your counter-argument, which phrase works best?",
                "options": [
                    "While I acknowledge that..., I still believe...",
                    "Because I agree with everything, I think...",
                    "Since you are wrong, I conclude that...",
                    "Without question, no one thinks that..."
                ],
                "correct_index": 0,
                "explanation": "'While I acknowledge that..., I still believe...' politely concedes before presenting your viewpoint."
            }
        ]
    },
    {
        "id": "curric_b1_pron_word_stress",
        "cefr_level": "B1",
        "module_type": "pronunciation",
        "title": "Word Stress Patterns in Multi-Syllable Words",
        "order_index": 7,
        "prerequisites": ["curric_a2_pron_past_ed_endings"],
        "estimated_minutes": 20,
        "objectives": [
            "Identify primary and secondary stress in three- and four-syllable academic words.",
            "Understand how suffixes alter stress placement (-tion, -ic, -ity, -graphy).",
            "Master the schwa /ə/ sound in unstressed syllables."
        ],
        "explanation_markdown": """### Stress Shifts with Suffixes
In English, adding suffixes frequently causes the primary stress to shift:
- **PHO-to-graph** (stress on 1st syllable)
- **pho-TO-gra-pher** (stress on 2nd syllable)
- **pho-to-GRA-phic** (stress on 3rd syllable before -ic)
Rules: Words ending in **-tion**, **-sion**, or **-ic** usually have stress on the syllable immediately preceding the suffix.""",
        "examples": [
            {"text": "e-DU-cate -> edu-CA-tion -> e-du-CA-tio-nal", "notes": "Notice how the stressed vowel changes."}
        ],
        "guided_exercises": [
            {"id": "b1_p_ge_1", "prompt": "Where is the primary stress in 'economic': eco-NOM-ic or E-conomic?", "answer": "eco-NOM-ic", "explanation": "Words ending in -ic take stress on the penultimate syllable."}
        ],
        "interactive_practice": [
            {
                "id": "b1_p_ip_1",
                "question": "Which syllable receives primary stress in 'information'?",
                "options": ["First (IN-)", "Second (-for-)", "Third (-MA-)", "Fourth (-tion)"],
                "correct_index": 2,
                "explanation": "-tion suffixes place stress on the penultimate syllable: in-for-MA-tion."
            }
        ],
        "assessment": [
            {
                "id": "b1_p_as_1",
                "question": "In which word is the primary stress on the second syllable?",
                "options": ["Photograph", "Democracy", "Economic", "Education"],
                "correct_index": 1,
                "explanation": "de-MOC-ra-cy has primary stress on the second syllable."
            }
        ]
    },
    {
        "id": "curric_b1_func_business_meetings",
        "cefr_level": "B1",
        "module_type": "functional",
        "title": "Functional English: Professional Meetings & Inquiries",
        "order_index": 8,
        "prerequisites": ["curric_b1_vocab_workplace_education"],
        "estimated_minutes": 25,
        "objectives": [
            "Open, contribute to, and conclude business and study group meetings.",
            "Ask clarifying questions politely ('Could you elaborate on that point?').",
            "Interrupt constructively without causing offense."
        ],
        "explanation_markdown": """### Meeting Formulas
- **Opening**: *Shall we get started? / The objective of today's meeting is...*
- **Inviting Input**: *What are your thoughts on this, David?*
- **Clarification**: *Could you clarify what you mean by 'budget revisions'?*
- **Polite Interruption**: *May I just jump in here for a moment?*""",
        "examples": [
            {"text": "CHAIRPERSON: 'If no one has further objections, let's move to item three.'", "notes": "Effective meeting management."}
        ],
        "guided_exercises": [
            {"id": "b1_func_ge_1", "prompt": "Complete the polite interruption: 'May I _____ in here for a second?' (jump / hit)", "answer": "jump", "explanation": "'jump in' is the standard conversational idiom."}
        ],
        "interactive_practice": [
            {
                "id": "b1_func_ip_1",
                "question": "Which phrase is best for asking a colleague to clarify an unclear statement?",
                "options": [
                    "You make no sense.",
                    "Could you elaborate on that point, please?",
                    "Repeat everything you just said.",
                    "I reject that statement completely."
                ],
                "correct_index": 1,
                "explanation": "'Could you elaborate on that point, please?' is professional and courteous."
            }
        ],
        "assessment": [
            {
                "id": "b1_func_as_1",
                "question": "How do you politely summarize agreed actions at the conclusion of a meeting?",
                "options": [
                    "Let's recap the key action items we've agreed on.",
                    "We are finished, go work now.",
                    "Nobody forgets anything today.",
                    "The time has passed, leave quickly."
                ],
                "correct_index": 0,
                "explanation": "'Let's recap the key action items...' is professional meeting protocol."
            }
        ]
    },
    {
        "id": "curric_b1_rev_intermediate_mastery",
        "cefr_level": "B1",
        "module_type": "review",
        "title": "B1 Intermediate Level Review & Comprehensive Assessment",
        "order_index": 9,
        "prerequisites": ["curric_b1_gram_present_perfect", "curric_b1_write_cohesion_linkers"],
        "estimated_minutes": 35,
        "objectives": [
            "Synthesize B1 grammar (present perfect vs past simple) and cohesive linking.",
            "Verify lexical accuracy in professional and academic domains.",
            "Confirm readiness for CEFR B2 Upper-Intermediate curriculum."
        ],
        "explanation_markdown": """### B1 Milestone Review
At B1 (Threshold Level), learners can understand main points of clear standard input on familiar matters, deal with most travel situations, and produce connected text on topics of personal or career interest.""",
        "examples": [
            {"text": "B1 Benchmark: Confident command of basic and intermediate grammatical tenses and paragraph cohesion.", "notes": "Official CEFR B1 threshold."}
        ],
        "guided_exercises": [
            {"id": "b1_rev_ge_1", "prompt": "Correct the tense: 'I am knowing Dr. Smith since 2018.'", "answer": "I have known Dr. Smith since 2018.", "explanation": "'know' is a stative verb; ongoing state since 2018 requires Present Perfect 'have known'."}
        ],
        "interactive_practice": [
            {
                "id": "b1_rev_ip_1",
                "question": "Which sentence is completely correct in grammar and cohesion?",
                "options": [
                    "Although he worked hard, but he failed the exam.",
                    "Although he worked hard, he passed the exam with distinction.",
                    "Despite he worked hard, he passed the exam.",
                    "Because he worked hard, however he passed."
                ],
                "correct_index": 1,
                "explanation": "'Although' introduces a concession clause and does not take 'but' in the main clause."
            }
        ],
        "assessment": [
            {
                "id": "b1_rev_as_1",
                "question": "Choose the sentence that correctly uses the Present Perfect:",
                "options": [
                    "The company has launched three new products in 2019.",
                    "The company has launched three new products this year.",
                    "The company launched three new products since January.",
                    "The company have launched three new products yesterday."
                ],
                "correct_index": 1,
                "explanation": "'this year' is an open, ongoing time period suitable for Present Perfect."
            }
        ]
    }
]

with open(os.path.join(CURRICULUM_DIR, "b1.json"), "w", encoding="utf-8") as f:
    json.dump(B1_LESSONS, f, indent=2, ensure_ascii=False)
print("Generated b1.json with", len(B1_LESSONS), "lessons.")
