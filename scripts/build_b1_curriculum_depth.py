# -*- coding: utf-8 -*-
"""
Deep Comprehensive Curriculum Builder for B1 Intermediate (Phase 13).
Preserves all 9 existing B1 lesson IDs with rich educational depth.
"""

import json

B1_LESSONS = [
    {
        "id": "curric_b1_gram_present_perfect",
        "cefr_level": "B1",
        "module_type": "grammar",
        "title": "Present Perfect vs Past Simple & Aspectual Contrast",
        "order_index": 1,
        "prerequisites": ["curric_a2_gram_past_simple"],
        "estimated_minutes": 45,
        "objectives": [
            "Distinguish between indefinite past experiences (Present Perfect) and definite finished events (Past Simple)",
            "Deploy temporal markers accurately: 'since' (point in time), 'for' (duration), 'already', 'yet', 'just'",
            "Express unfinished states and habits connecting the past directly to the present moment",
            "Eliminate common tense-aspect errors in IELTS Writing Task 1 and Speaking Part 1"
        ],
        "explanation_markdown": """### 1. Form & Linguistic Mechanics
The Present Perfect links a past action or state directly to the present moment.

#### Structural Formulas:
- **Affirmative:** Subject + have/has + Past Participle (V3).
  * Example: *I have lived here for five years.* | *She has written three essays.*
- **Negative:** Subject + have/has not (haven't/hasn't) + Past Participle.
  * Example: *They haven't finished the report yet.*
- **Interrogative:** Have/Has + Subject + Past Participle?
  * Example: *Have you ever visited Singapore?*

### 2. Present Perfect vs Past Simple: The Crucial Boundary
- **Past Simple (Finished Time):** Definite time specified or understood (*yesterday, in 2019, five minutes ago, when I was at university*).
  * ✓ *I graduated in 2022.* (NOT *I have graduated in 2022*).
- **Present Perfect (Unfinished / Indefinite Time):** Time period continues up to now, or the exact moment is irrelevant to the present outcome.
  * ✓ *I have visited ten countries so far.* (Life experience; time period ongoing).

### 3. 'Since' vs 'For'
- **SINCE + Starting Point in Time:** *since 2015, since Monday, since 9:00 AM, since I left school.*
- **FOR + Duration / Period of Time:** *for three hours, for ten years, for a long time, for centuries.*

### 4. Common Learner Traps:
1. **Specific Past Marker with Present Perfect:** ✗ *I have seen him yesterday.* ➔ ✓ *I saw him yesterday.*
2. **Confusing 'Since' and 'For':** ✗ *I have worked here since five years.* ➔ ✓ *I have worked here for five years.*
3. **'Been to' vs 'Gone to':**
   * *'She has gone to Italy.'* (She is still in Italy now).
   * *'She has been to Italy.'* (She visited and has now returned).""",
        "examples": [
            {"text": "The company has developed three new software tools since the beginning of this year.", "notes": "'Since' with starting point; unfinished present timeframe."},
            {"text": "Dr Evans conducted extensive field research in Brazil between 2018 and 2021.", "notes": "Past simple used because the historical dates specify a closed past period."},
            {"text": "I haven't submitted my university application yet, but I have already completed my personal statement.", "notes": "'Yet' in negative clause; 'already' for completed expectation."}
        ],
        "guided_exercises": [
            {
                "id": "b1_g_ge_1",
                "prompt": "Insert 'since' or 'for': 'She has lived in Manchester _____ six years.'",
                "answer": "for",
                "explanation": "'Six years' is a measurable duration of time, requiring 'for'."
            },
            {
                "id": "b1_g_ge_2",
                "prompt": "Correct the tense error: 'I have graduated from college in 2021.'",
                "answer": "I graduated from college in 2021.",
                "explanation": "'In 2021' is a closed, finished past time anchor, requiring Past Simple 'graduated'."
            },
            {
                "id": "b1_g_ge_3",
                "prompt": "Complete with 'been' or 'gone': 'Marcus is not at his desk; he has _____ to the post office.'",
                "answer": "gone",
                "explanation": "'Gone' indicates he has travelled there and has not yet returned."
            }
        ],
        "assessment": [
            {
                "id": "b1_g_as_1",
                "question": "Which sentence demonstrates the correct tense-aspect contrast?",
                "options": [
                    "I have lived in Bristol in 2015, but then I moved to London.",
                    "I lived in Bristol in 2015, but since 2018 I have lived in London.",
                    "I have lived in Bristol since 2015 to 2018.",
                    "I live in Bristol since 2018."
                ],
                "correct_index": 1,
                "explanation": "'lived' for completed 2015 past period, followed by 'have lived' with 'since 2018' for continuing state."
            },
            {
                "id": "b1_g_as_2",
                "question": "Select the sentence with accurate usage of 'since' and 'for':",
                "options": [
                    "They have been married since twenty years.",
                    "They have been married for twenty years.",
                    "They are married since twenty years ago.",
                    "They were married for 2004."
                ],
                "correct_index": 1,
                "explanation": "'Twenty years' is a duration, requiring 'for'."
            },
            {
                "id": "b1_g_as_3",
                "question": "What is the difference between 'She has been to Madrid' and 'She has gone to Madrid'?",
                "options": [
                    "'Been' means she is currently in Madrid; 'gone' means she returned.",
                    "'Been' means she visited and returned; 'gone' means she is still there.",
                    "There is no difference in British English.",
                    "'Gone' can only be used with past simple."
                ],
                "correct_index": 1,
                "explanation": "'Has been' denotes completed travel with return; 'has gone' indicates current absence."
            }
        ]
    },
    {
        "id": "curric_b1_vocab_workplace_education",
        "cefr_level": "B1",
        "module_type": "vocabulary",
        "title": "Workplace Dynamics, Careers & Higher Education",
        "order_index": 2,
        "prerequisites": ["curric_a2_vocab_travel_food"],
        "estimated_minutes": 40,
        "objectives": [
            "Command tertiary education and employment lexis (vocational, syllabus, probation, salary)",
            "Derive morphological word families accurately (employ, employer, employee, employment)",
            "Use formal workplace collocations ('meet deadlines', 'acquire skills', 'pursue qualifications')"
        ],
        "explanation_markdown": """### 1. Tertiary Education Lexicon
- **Higher Education (HE):** University-level academic study leading to undergraduate and postgraduate degrees.
- **Vocational Training:** Practical technical instruction preparing students for specific trades (plumbing, nursing, electrical engineering).
- **Curriculum vs Syllabus:**
  * *Curriculum:* The entire programme of courses offered by an institution.
  * *Syllabus:* The detailed outline of topics, assignments, and exams for one specific course.

### 2. Workplace Terminology
- **Probationary Period:** A trial phase (usually 3–6 months) where a new employee's suitability is evaluated.
- **Remuneration / Salary:** The formal term for employee financial compensation.
- **Appraisal / Performance Review:** Periodic formal assessment of employee productivity.

### 3. Core Academic Word Families:
- **employ** (v) $\\rightarrow$ **employer** (n, person hiring) $\\rightarrow$ **employee** (n, worker) $\\rightarrow$ **employment** (n, state of having a job) $\\rightarrow$ **unemployed** (adj).
- **qualify** (v) $\\rightarrow$ **qualification** (n) $\\rightarrow$ **qualified** (adj) $\\rightarrow$ **disqualify** (v).""",
        "examples": [
            {"text": "Vocational education provides hands-on technical competencies alongside theoretical instruction.", "notes": "Contrast between vocational and purely theoretical studies."},
            {"text": "Candidates must possess recognized professional qualifications in financial accounting.", "notes": "Collocation: 'possess professional qualifications'."},
            {"text": "During his six-month probationary period, the junior engineer demonstrated remarkable diligence.", "notes": "Workplace context: 'probationary period'."}
        ],
        "guided_exercises": [
            {
                "id": "b1_v_ge_1",
                "prompt": "Complete with the correct word family form: 'The factory provides steady _____ for over 500 local residents.' (employ)",
                "answer": "employment",
                "explanation": "The noun form indicating the state of having a job is 'employment'."
            },
            {
                "id": "b1_v_ge_2",
                "prompt": "Which term describes practical, job-oriented technical training? (vocational / theoretical)",
                "answer": "vocational",
                "explanation": "'Vocational' refers specifically to practical trade and career training."
            },
            {
                "id": "b1_v_ge_3",
                "prompt": "Complete the collocation: 'Employees must work cooperatively to _____ tight project deadlines.' (reach / meet / do)",
                "answer": "meet",
                "explanation": "The standard professional collocation is 'meet deadlines'."
            }
        ],
        "assessment": [
            {
                "id": "b1_v_as_1",
                "question": "What is the difference between a 'curriculum' and a 'syllabus'?",
                "options": [
                    "A curriculum is for sports; a syllabus is for literature.",
                    "A curriculum encompasses the entire academic program; a syllabus is the outline of a specific subject.",
                    "There is no difference in modern education.",
                    "A syllabus is decided by students; a curriculum is set by governments."
                ],
                "correct_index": 1,
                "explanation": "A curriculum is the overarching institutional course program; a syllabus details a single subject."
            },
            {
                "id": "b1_v_as_2",
                "question": "Which word correctly completes: 'After completing his undergraduate degree, he decided to _____ a master's in data science.'?",
                "options": [
                    "chase",
                    "pursue",
                    "catch",
                    "run"
                ],
                "correct_index": 1,
                "explanation": "The academic collocation is 'to pursue a degree / career'."
            },
            {
                "id": "b1_v_as_3",
                "question": "What is an employee's 'probationary period'?",
                "options": [
                    "A permanent paid holiday",
                    "A trial period at the start of employment to assess performance",
                    "A punishment for making mistakes",
                    "The retirement notice period"
                ],
                "correct_index": 1,
                "explanation": "Probation is a temporary trial period before confirming permanent employment."
            }
        ]
    },
    {
        "id": "curric_b1_read_skimming",
        "cefr_level": "B1",
        "module_type": "reading",
        "title": "Skimming for Gist & Scanning for Details",
        "order_index": 3,
        "prerequisites": ["curric_b1_vocab_workplace_education"],
        "estimated_minutes": 45,
        "objectives": [
            "Skim academic and general texts within 60 seconds to identify central themes and headings",
            "Scan passages under timed conditions for specific proper nouns, dates, and quantitative data",
            "Differentiate between topic sentences and supplementary illustration in academic paragraphs"
        ],
        "explanation_markdown": """### Reading Technique: Skimming vs Scanning
In the IELTS Reading examination (60 minutes, 40 questions), candidates cannot read all 2,750 words thoroughly.

#### 1. Skimming (Reading for the Gist / Big Picture):
- **Purpose:** Understand what each paragraph is broadly about in order to match headings.
- **Method:** Read the **first sentence** (Topic Sentence), glance at middle keywords, and read the **final concluding sentence**. Do NOT stop for unfamiliar words.

#### 2. Scanning (Reading for Specific Micro-Data):
- **Purpose:** Find exact names, numbers, years, and specific technical terms.
- **Method:** Keep the question keyword in your mind, move your eyes zigzagging across the text, and stop only when the target appears.

#### Reading Text: Remote Work Adaptation
```
The shift towards hybrid employment models has transformed urban commercial architecture. 
Prior to 2020, multinational corporations in major metropolitan hubs leased expansive 
multi-storey office complexes to accommodate their workforce. However, surveys conducted 
in late 2024 revealed that over 68% of knowledge workers now prefer splitting their working 
week between home and regional co-working hubs. Consequently, commercial real estate developers 
are retrofitting vacant corporate towers into flexible residential apartments and communal spaces.
```""",
        "examples": [
            {"text": "The main theme of the paragraph is the transformation of urban commercial buildings due to hybrid work.", "notes": "Skimming identifying central topic sentence."},
            {"text": "68% of knowledge workers favor split work weeks.", "notes": "Scanning locating exact numerical percentage."},
            {"text": "Vacant office towers are being converted into residential apartments.", "notes": "Scanning locating specific consequence."}
        ],
        "guided_exercises": [
            {
                "id": "b1_r_ge_1",
                "prompt": "According to the passage, what percentage of knowledge workers prefer hybrid work?",
                "answer": "68%",
                "explanation": "Scanning directly for the percentage symbol yields 'over 68%'."
            },
            {
                "id": "b1_r_ge_2",
                "prompt": "What are developers retrofitting vacant corporate towers into?",
                "answer": "flexible residential apartments and communal spaces",
                "explanation": "Scanning for 'retrofitting' leads to the final sentence."
            },
            {
                "id": "b1_r_ge_3",
                "prompt": "What is the primary function of the first sentence in the paragraph?",
                "answer": "Topic sentence",
                "explanation": "The first sentence introduces the controlling overarching idea of the paragraph."
            }
        ],
        "assessment": [
            {
                "id": "b1_r_as_1",
                "question": "Which heading best summarizes the paragraph?",
                "options": [
                    "The Complete Collapse of Remote Work",
                    "How Flexible Employment is Reshaping Urban Real Estate",
                    "High Construction Costs in Metropolitan Centres",
                    "The Decline of Suburban Housing"
                ],
                "correct_index": 1,
                "explanation": "The paragraph explains how hybrid work trends caused commercial buildings to be converted into residential spaces."
            },
            {
                "id": "b1_r_as_2",
                "question": "What is the recommended method for skimming a paragraph in an IELTS reading exam?",
                "options": [
                    "Read every word slowly with a bilingual dictionary",
                    "Read the first and last sentences to grasp the controlling idea",
                    "Translate every paragraph into your first language",
                    "Read only the middle three lines"
                ],
                "correct_index": 1,
                "explanation": "Skimming focuses on topic and concluding sentences to ascertain gist quickly."
            },
            {
                "id": "b1_r_as_3",
                "question": "What occurred prior to 2020 according to the passage?",
                "options": [
                    "Companies converted offices to apartments",
                    "Multinational firms leased large multi-storey office complexes",
                    "68% of employees worked exclusively from home",
                    "Office rents were abolished by metropolitan authorities"
                ],
                "correct_index": 1,
                "explanation": "The text states 'Prior to 2020, multinational corporations... leased expansive multi-storey office complexes'."
            }
        ]
    },
    {
        "id": "curric_b1_listen_lectures",
        "cefr_level": "B1",
        "module_type": "listening",
        "title": "Note-Taking from Short Academic Lectures",
        "order_index": 4,
        "prerequisites": ["curric_b1_vocab_workplace_education"],
        "estimated_minutes": 45,
        "objectives": [
            "Recognize lecture discourse signposts that signal transitions, definitions, and contrasting viewpoints",
            "Deploy shorthand symbols ($\\rightarrow$, $\\ne$, w/, e.g., vs) for high-speed academic note-taking",
            "Extract numerical evidence and research findings without losing track of spoken arguments"
        ],
        "explanation_markdown": """### Transcript-Based Listening Strategy: Academic Lectures
*(Practice session using authentic IELTS Section 4 / academic lecture scripts.)*

#### Audio Script: Marine Microplastics
```
LECTURER: Good morning, everyone. In today's oceanography seminar, we examine marine plastic pollution, 
specifically microplastics—particles measuring less than five millimetres across. 
Now, turning first to their primary origin: surprisingly, over thirty-five percent originate from synthetic 
textiles during household machine washing. 
Furthermore, secondary microplastics result when larger debris, such as discarded fishing nets, degrades 
under solar ultraviolet radiation. 
This brings me to the core environmental hazard. These micro-particles absorb toxic organic pollutants 
from surrounding seawater. When plankton ingest them, these toxins enter the trophic food web, 
eventually bioaccumulating in commercial seafood harvested for human consumption.
```

#### Note-Taking Signposts:
- **Topic Announcement:** *'In today's seminar, we examine...'*
- **Transition to First Point:** *'Now, turning first to...'*
- **Additional Point:** *'Furthermore, secondary...'*
- **Consequential Impact:** *'This brings me to the core hazard...'*""",
        "examples": [
            {"text": "Microplastics are defined as particles measuring under five millimetres.", "notes": "Definitional statement extraction."},
            {"text": "Over 35% of primary microplastics originate from synthetic textiles in washing machines.", "notes": "Quantitative statistical finding."},
            {"text": "Toxins bioaccumulate in the food chain via plankton ingestion.", "notes": "Causal scientific sequence."}
        ],
        "guided_exercises": [
            {
                "id": "b1_l_ge_1",
                "prompt": "What is the maximum diameter of a particle categorized as a microplastic?",
                "answer": "five millimetres",
                "explanation": "The lecturer defines them as 'measuring less than five millimetres across'."
            },
            {
                "id": "b1_l_ge_2",
                "prompt": "What percentage of primary microplastics comes from synthetic clothing in laundry?",
                "answer": "over thirty-five percent",
                "explanation": "The script specifies 'over thirty-five percent originate from synthetic textiles'."
            },
            {
                "id": "b1_l_ge_3",
                "prompt": "What environmental radiation causes larger debris like fishing nets to break down into secondary microplastics?",
                "answer": "solar ultraviolet radiation",
                "explanation": "The lecture states debris 'degrades under solar ultraviolet radiation'."
            }
        ],
        "assessment": [
            {
                "id": "b1_l_as_1",
                "question": "What is the major ecological hazard highlighted by the lecturer?",
                "options": [
                    "They cool ocean temperatures too rapidly",
                    "They absorb toxic chemicals and bioaccumulate in the seafood chain",
                    "They block submarine sonar navigation",
                    "They prevent ocean waves from forming"
                ],
                "correct_index": 1,
                "explanation": "The lecturer notes microplastics absorb toxins which enter the food web and bioaccumulate."
            },
            {
                "id": "b1_l_as_2",
                "question": "Which spoken signpost phrase signals that the lecturer is moving to the next main sub-topic?",
                "options": [
                    "By the way...",
                    "Now, turning first to...",
                    "I forgot to say...",
                    "Anyway, as I said..."
                ],
                "correct_index": 1,
                "explanation": "'Now, turning first to...' is a formal academic discourse transition."
            },
            {
                "id": "b1_l_as_3",
                "question": "How should a student efficiently abbreviate 'with regards to synthetic textiles' in lecture notes?",
                "options": [
                    "Write every single letter in full longhand",
                    "w/r/t synth textiles",
                    "Stop taking notes entirely",
                    "Draw a picture of a shirt"
                ],
                "correct_index": 1,
                "explanation": "'w/r/t' is standard academic shorthand for 'with regard to'."
            }
        ]
    },
    {
        "id": "curric_b1_write_paragraphs",
        "cefr_level": "B1",
        "module_type": "writing",
        "title": "Paragraph Architecture & Topic Sentences",
        "order_index": 5,
        "prerequisites": ["curric_a2_write_emails", "curric_b1_gram_present_perfect"],
        "estimated_minutes": 50,
        "objectives": [
            "Draft authoritative Topic Sentences containing a clear subject and controlling idea",
            "Develop body paragraphs using explanation, empirical evidence, and concluding links",
            "Deploy cohesive transition words ('Furthermore', 'In contrast', 'As a consequence') to ensure paragraph flow"
        ],
        "explanation_markdown": """### 1. The Anatomy of an Academic Paragraph
An academic paragraph must focus on **one single main idea**. A robust model follows a 4-part structure:
1. **Topic Sentence (TS):** States the topic and the controlling opinion/claim.
2. **Explanation (EX):** Expands on why or how this is true in 1–2 sentences.
3. **Evidence / Example (EV):** Provides a concrete illustration, case study, or real-world trend.
4. **Concluding Link (LK):** Connects the paragraph back to the overarching essay prompt.

### 2. Crafting Effective Topic Sentences
- Weak / Incomplete (Factual statement without argument):
  * ✗ *Many people use smartphones today.*
- Strong (Topic + Controlling Idea):
  * ✓ *The widespread adoption of smartphones in secondary education offers substantial pedagogical benefits, provided digital usage is strictly regulated.*

### 3. Cohesive Transitions:
- **Adding Information:** *Furthermore, Additionally, In addition.*
- **Contrasting:** *In contrast, Conversely, On the other hand.*
- **Cause and Effect:** *Consequently, As a result, Therefore.*""",
        "examples": [
            {"text": "Investing in renewable energy infrastructure yields long-term economic resilience.", "notes": "Clear, arguable topic sentence with controlling idea."},
            {"text": "For instance, municipalities that subsidized residential solar panels reduced grid strain by 28%.", "notes": "Concrete supporting evidence with statistical illustration."},
            {"text": "Consequently, allocating fiscal budgets to green power is economically prudent.", "notes": "Concluding link reinforcing the initial topic sentence."}
        ],
        "guided_exercises": [
            {
                "id": "b1_w_ge_1",
                "prompt": "Identify the controlling idea in: 'Urban cycling infrastructure reduces traffic congestion significantly.'",
                "answer": "reduces traffic congestion significantly",
                "explanation": "The topic is 'urban cycling infrastructure'; the controlling claim is that it reduces congestion significantly."
            },
            {
                "id": "b1_w_ge_2",
                "prompt": "Choose a formal transition indicating consequence: (In contrast / Consequently / Furthermore)",
                "answer": "Consequently",
                "explanation": "'Consequently' signals cause-and-effect / consequence."
            },
            {
                "id": "b1_w_ge_3",
                "prompt": "Which transition should introduce an opposing perspective? (However / Moreover)",
                "answer": "However",
                "explanation": "'However' signals counter-argument or contrast."
            }
        ],
        "assessment": [
            {
                "id": "b1_w_as_1",
                "question": "Which of the following functions as the most effective academic Topic Sentence?",
                "options": [
                    "This paragraph is about universities in Europe.",
                    "Higher education institutions play an indispensable role in stimulating regional technological innovation.",
                    "I think college is good for young people.",
                    "There are many universities in London and Paris."
                ],
                "correct_index": 1,
                "explanation": "Presents an authoritative, debatable controlling claim about universities and regional innovation."
            },
            {
                "id": "b1_w_as_2",
                "question": "What is the primary role of the 'Link' sentence at the conclusion of a body paragraph?",
                "options": [
                    "To introduce a completely unrelated second topic",
                    "To summarize the evidence and reconnect directly to the essay question",
                    "To list vocabulary definitions",
                    "To apologize for any grammatical mistakes"
                ],
                "correct_index": 1,
                "explanation": "The link ties the evidence back to the central thesis and prompt."
            },
            {
                "id": "b1_w_as_3",
                "question": "Which linking adverb correctly fills the blank: 'Electric vehicles produce zero tailpipe emissions. _____, their widespread adoption significantly improves urban air quality.'?",
                "options": [
                    "In contrast",
                    "Consequently",
                    "Nevertheless",
                    "Whereas"
                ],
                "correct_index": 1,
                "explanation": "Improving air quality is the direct consequence of zero emissions, requiring 'Consequently'."
            }
        ]
    },
    {
        "id": "curric_b1_speak_opinions_justification",
        "cefr_level": "B1",
        "module_type": "speaking",
        "title": "Expressing Opinions & Justifying Viewpoints",
        "order_index": 6,
        "prerequisites": ["curric_a2_speak_past_experiences"],
        "estimated_minutes": 45,
        "objectives": [
            "Use varied stance markers ('In my estimation', 'From my standpoint', 'I am convinced that')",
            "Deploy the 3-step IELTS Advantage speaking method: Direct Stance $\\rightarrow$ Logical Justification $\\rightarrow$ Concrete Example",
            "Extend answers in IELTS Speaking Part 1 and Part 3 beyond simplistic one-sentence replies"
        ],
        "explanation_markdown": """### The 3-Step Speaking Justification Method
In IELTS Speaking (especially Parts 1 and 3), examiners penalize short, unextended answers. Always follow the 3-Step Strategy:

1. **Step 1: Direct Answer (Stance):**
   * *'In my view, public transportation should undoubtedly be free for senior citizens.'*
2. **Step 2: Reason / Justification (Why):**
   * *'The primary rationale is that many elderly individuals live on fixed retirement pensions and cannot afford escalating transit fares.'*
3. **Step 3: Example / Extension (Evidence):**
   * *'For example, in my hometown, when bus fares were waived for pensioners, their participation in community and health programs increased dramatically.'*

### Stance Markers Bank:
- *From my perspective...*
- *In my estimation...*
- *I am inclined to believe that...*
- *It seems to me that...*""",
        "examples": [
            {"text": "From my perspective, remote learning offers immense flexibility, particularly for mature students balancing employment with academic commitments.", "notes": "Direct stance + justification."},
            {"text": "The main justification is economic; subsidizing green transit reduces long-term healthcare expenditures caused by air pollution.", "notes": "Analytical reasoning linking economics to health."},
            {"text": "For instance, cities that invested in separated cycling lanes witnessed a forty percent drop in vehicular accidents.", "notes": "Concrete statistical example reinforcing stance."}
        ],
        "guided_exercises": [
            {
                "id": "b1_sp_ge_1",
                "prompt": "Insert a formal opinion marker: '_____, vocational training is just as valuable as university education.' (In my view / Me think)",
                "answer": "In my view",
                "explanation": "'In my view' or 'From my perspective' is standard formal English."
            },
            {
                "id": "b1_sp_ge_2",
                "prompt": "Complete the 3-Step formula: Direct Stance $\\rightarrow$ Reason $\\rightarrow$ _____.",
                "answer": "Example",
                "explanation": "Step 3 is providing a concrete example or illustration to substantiate the claim."
            },
            {
                "id": "b1_sp_ge_3",
                "prompt": "Transform into an extended answer: 'Do you like reading books?'",
                "answer": "Yes, absolutely. I read historical fiction every evening because it helps me decompress after work.",
                "explanation": "Extends beyond 'yes' with specific genre and personal justification."
            }
        ],
        "assessment": [
            {
                "id": "b1_sp_as_1",
                "question": "Which response to 'Should schools teach financial management?' represents a complete Band 6.5+ 3-Step answer?",
                "options": [
                    "Yes, it is very good idea.",
                    "Without doubt. In my view, learning to budget prepares teenagers for adult autonomy. For instance, high schoolers who take basic financial literacy courses manage debt far more effectively at university.",
                    "Schools only teach math and science, not money.",
                    "I think money is important for everyone in the world."
                ],
                "correct_index": 1,
                "explanation": "Executes the 3-step strategy: Direct stance ('Without doubt'), reason ('prepares for autonomy'), example ('courses manage debt')."
            },
            {
                "id": "b1_sp_as_2",
                "question": "Which phrase is an informal colloquialism that should be AVOIDED in academic speaking tests?",
                "options": [
                    "In my estimation...",
                    "Like, you know, it's pretty cool...",
                    "From my standpoint...",
                    "I am strongly convinced that..."
                ],
                "correct_index": 1,
                "explanation": "'Like, you know, it's pretty cool' is overly informal and lacks academic register."
            },
            {
                "id": "b1_sp_as_3",
                "question": "What is the primary risk of giving one-word answers in the IELTS Speaking interview?",
                "options": [
                    "The examiner will automatically end the test",
                    "It severely limits your score for Fluency and Coherence because you fail to extend your answers",
                    "There is no penalty if the word is correct",
                    "You will receive an automatic Band 9 for brevity"
                ],
                "correct_index": 1,
                "explanation": "IELTS Fluency & Coherence rubrics explicitly require candidates to speak at length without noticeable effort."
            }
        ]
    },
    {
        "id": "curric_b1_pron_word_stress",
        "cefr_level": "B1",
        "module_type": "pronunciation",
        "title": "Word Stress Patterns & The Neutral Schwa (/ə/)",
        "order_index": 7,
        "prerequisites": ["curric_a2_pron_past_endings"],
        "estimated_minutes": 45,
        "objectives": [
            "Master syllable stress shifts between noun-verb homographs ('record vs re'cord, 'present vs pre'sent)",
            "Articulate the neutral schwa sound (/ə/) in unstressed syllables of multisyllabic words",
            "Identify primary and secondary stress marks in IPA dictionary entries"
        ],
        "explanation_markdown": """### 1. Noun-Verb Stress Shift Rule
Many two-syllable words in English change their part of speech depending on which syllable is stressed:
- **NOUNS / ADJECTIVES (Stress on FIRST Syllable):**
  * **'record** /ˈrekɔːd/ (noun: *a world record*)
  * **'present** /ˈpreznt/ (noun: *a birthday present*)
  * **'object** /ˈɒbdʒɪkt/ (noun: *a physical object*)
  * **'conduct** /ˈkɒndʌkt/ (noun: *professional conduct*)
- **VERBS (Stress on SECOND Syllable):**
  * **re'cord** /rɪˈkɔːd/ (verb: *to record an interview*)
  * **pre'sent** /prɪˈzent/ (verb: *to present findings*)
  * **ob'ject** /əbˈdʒekt/ (verb: *to object to a proposal*)
  * **con'duct** /kənˈdʌkt/ (verb: *to conduct an experiment*)

### 2. The Schwa (/ə/)
The schwa is the most frequent sound in English. It occurs ONLY in **unstressed syllables**. It is a short, relaxed central vowel:
- *a-bout* /əˈbaʊt/ (first syllable is schwa)
- *doc-tor* /ˈdɒktə/ (second syllable is schwa)
- *com-pu-ter* /kəmˈpjuːtə/ (first and third syllables are schwas)""",
        "examples": [
            {"text": "The research team will con'duct a comprehensive survey on student 'conduct.", "notes": "Contrast between verb con'duct (/kənˈdʌkt/) and noun 'conduct (/ˈkɒndʌkt/)."},
            {"text": "He wants to re'cord a podcast about the historical 'record.", "notes": "Verb re'cord vs noun 'record."},
            {"text": "The pro'fessor gave in'struction to the com'mittee.", "notes": "Unstressed vowels reduced to schwa (/ə/)."}
        ],
        "guided_exercises": [
            {
                "id": "b1_p_ge_1",
                "prompt": "Where is the stress placed in the NOUN 'progress'? (first syllable / second syllable)",
                "answer": "first syllable",
                "explanation": "Two-syllable nouns take stress on the first syllable: /ˈprəʊɡres/."
            },
            {
                "id": "b1_p_ge_2",
                "prompt": "Where is the stress placed in the VERB 'progress'? (first syllable / second syllable)",
                "answer": "second syllable",
                "explanation": "Two-syllable verbs take stress on the second syllable: /prəˈɡres/."
            },
            {
                "id": "b1_p_ge_3",
                "prompt": "Which syllable contains the schwa /ə/ in 'banana'? (first / second / both first and last)",
                "answer": "both first and last",
                "explanation": "/bəˈnɑːnə/ has schwas on both the first and final unstressed syllables."
            }
        ],
        "assessment": [
            {
                "id": "b1_p_as_1",
                "question": "In the sentence 'They plan to _____ their findings tomorrow', which pronunciation is correct for the verb?",
                "options": [
                    "/'preznt/ (stress on first syllable)",
                    "/prɪ'zent/ (stress on second syllable)",
                    "Both are equally acceptable",
                    "Neither is used in British English"
                ],
                "correct_index": 1,
                "explanation": "The verb 'to present' is stressed on the second syllable /prɪˈzent/."
            },
            {
                "id": "b1_p_as_2",
                "question": "What is the defining characteristic of the schwa /ə/ sound?",
                "options": [
                    "It is always heavily stressed and spoken loudly",
                    "It occurs only in unstressed syllables as a relaxed central vowel",
                    "It only appears in American English",
                    "It is identical to the long vowel /iː/"
                ],
                "correct_index": 1,
                "explanation": "The schwa is the quintessential unstressed vowel in spoken English."
            },
            {
                "id": "b1_p_as_3",
                "question": "Which of the following words has the primary stress on the SECOND syllable?",
                "options": [
                    "'photograph",
                    "pho'tography",
                    "'photographic",
                    "'photo"
                ],
                "correct_index": 1,
                "explanation": "pho'tography /fəˈtɒɡrəfi/ shifts stress to the second syllable."
            }
        ]
    },
    {
        "id": "curric_b1_func_business_emails",
        "cefr_level": "B1",
        "module_type": "functional",
        "title": "Professional Emails & Formal Requests",
        "order_index": 8,
        "prerequisites": ["curric_a2_write_emails", "curric_b1_vocab_workplace_education"],
        "estimated_minutes": 45,
        "objectives": [
            "Write professional business correspondence with appropriate subject lines and formal salutations",
            "Soften direct commands using polite modal inquiry formulas ('I would be grateful if you could...')",
            "Select suitable formal sign-offs ('Yours sincerely' vs 'Yours faithfully')"
        ],
        "explanation_markdown": """### 1. Formal Business Email Structure
- **Subject Line:** Specific, concise, capitalized (*Inquiry regarding Master of Science Admissions Autumn 2026*).
- **Formal Salutation Rules:**
  * If you know the recipient's surname: *Dear Mr Davies, / Dear Dr Alvarez,*
  * If you do not know the recipient's name: *Dear Sir/Madam,*
- **Statement of Purpose:**
  * *'I am writing to inquire about the scholarship opportunities available for international postgraduates.'*
- **Polite Request Formulas:**
  * *'Could you please clarify whether...' / 'I would be extremely grateful if you could forward me the syllabus.'*
- **Call to Action / Closing:**
  * *'I look forward to hearing from you at your earliest convenience.'*
- **Formal Sign-Offs (Strict Convention):**
  * If you addressed by name (*Dear Dr Smith*): sign off **Yours sincerely,**
  * If you addressed anonymously (*Dear Sir/Madam*): sign off **Yours faithfully,**""",
        "examples": [
            {"text": "Dear Professor Higgins, I am writing with regard to the upcoming symposium schedule.", "notes": "Formal salutation by name with standard opening statement of purpose."},
            {"text": "I would be grateful if you could confirm the submission deadline for the research proposal.", "notes": "Modal softening with 'I would be grateful if you could'."},
            {"text": "Yours sincerely, Julian Sterling.", "notes": "Accurate formal sign-off matching a named salutation."}
        ],
        "guided_exercises": [
            {
                "id": "b1_f_ge_1",
                "prompt": "Which sign-off must be paired with 'Dear Sir/Madam'? (Yours sincerely / Yours faithfully)",
                "answer": "Yours faithfully",
                "explanation": "When the recipient's name is unknown ('Dear Sir/Madam'), formal convention requires 'Yours faithfully'."
            },
            {
                "id": "b1_f_ge_2",
                "prompt": "Soften this blunt sentence: 'Send me the contract.'",
                "answer": "Could you please send me the contract?",
                "explanation": "Use 'Could you please send...' or 'I would appreciate it if you could send...'."
            },
            {
                "id": "b1_f_ge_3",
                "prompt": "Complete the formal closing: 'I look forward to _____ from you.' (hear / hearing)",
                "answer": "hearing",
                "explanation": "'Look forward to' is followed by a gerund (-ing): 'hearing'."
            }
        ],
        "assessment": [
            {
                "id": "b1_f_as_1",
                "question": "If you begin a formal business letter with 'Dear Ms Henderson,', how must you sign off?",
                "options": [
                    "Yours faithfully,",
                    "Yours sincerely,",
                    "Cheers,",
                    "Later,"
                ],
                "correct_index": 1,
                "explanation": "When addressing a known person by surname, the rule is 'Yours sincerely,'."
            },
            {
                "id": "b1_f_as_2",
                "question": "Which sentence expresses a professional request with the most appropriate polite register?",
                "options": [
                    "I want you to email the report immediately.",
                    "I would be grateful if you could provide an update on the project timeline.",
                    "Give me the file today.",
                    "Why didn't you send the update yet?"
                ],
                "correct_index": 1,
                "explanation": "'I would be grateful if you could...' is standard diplomatic business English."
            },
            {
                "id": "b1_f_as_3",
                "question": "Which subject line is most effective for a formal university application inquiry?",
                "options": [
                    "help me please!!",
                    "Question",
                    "Application Inquiry: MSc Biomedical Science — Autumn 2026",
                    "Hi"
                ],
                "correct_index": 2,
                "explanation": "Clear, professional, and includes the specific program and intake year."
            }
        ]
    },
    {
        "id": "curric_b1_review_milestone",
        "cefr_level": "B1",
        "module_type": "review",
        "title": "B1 Milestone Review & Comprehensive Evaluation",
        "order_index": 9,
        "prerequisites": ["curric_b1_gram_present_perfect", "curric_b1_write_paragraphs"],
        "estimated_minutes": 55,
        "objectives": [
            "Demonstrate command of aspectual contrasts, paragraph architecture, and academic vocabulary",
            "Validate readiness for upper-intermediate CEFR B2 and IELTS Band 6.0–6.5 preparation",
            "Synthesize professional correspondence and spoken opinion justification under timed conditions"
        ],
        "explanation_markdown": """### B1 Milestone Comprehensive Synthesis
Graduation to CEFR B2 certifies that a learner has bridged the gap from basic functional communication to academic English competence:
1. **Aspectual Tense Control:** Zero confusion between Past Simple (closed past) and Present Perfect (open timeframe).
2. **Structural Paragraphing:** Clear topic sentences followed by reasoned explanations and evidence.
3. **Professional Register:** Appropriate choice of formal discourse markers and courteous modal softening.
4. **Phonetic Stress Awareness:** Distinguishing noun-verb stress pairs and recognizing the schwa.

Review your notes on lessons B1.1 through B1.8 before taking this milestone examination.""",
        "examples": [
            {"text": "Since joining the engineering faculty in 2022, she has conducted several breakthrough experiments.", "notes": "'Since' with starting year + Present Perfect 'has conducted'."},
            {"text": "Consequently, allocating resources to vocational training reduces youth unemployment significantly.", "notes": "Causal connector with academic lexical collocations."},
            {"text": "I would be grateful if you could confirm your availability for an interview on Thursday.", "notes": "Polite professional request formula."}
        ],
        "guided_exercises": [
            {
                "id": "b1_rev_ge_1",
                "prompt": "Find and correct the tense error: 'She has completed her internship last week.'",
                "answer": "She completed her internship last week.",
                "explanation": "'Last week' is a closed past anchor requiring Past Simple 'completed'."
            },
            {
                "id": "b1_rev_ge_2",
                "prompt": "Combine with 'consequently': 'The laboratory lacked funding. The project was postponed.'",
                "answer": "The laboratory lacked funding; consequently, the project was postponed.",
                "explanation": "'Consequently' shows the logical outcome."
            },
            {
                "id": "b1_rev_ge_3",
                "prompt": "Where is the stress in the verb 'to conduct'? (first / second syllable)",
                "answer": "second syllable",
                "explanation": "Verbs of this class place stress on the second syllable: /kənˈdʌkt/."
            }
        ],
        "assessment": [
            {
                "id": "b1_rev_as_1",
                "question": "Which sentence demonstrates 100% accurate grammatical and lexical usage?",
                "options": [
                    "I lived in London since four years and work like a software engineer.",
                    "I have lived in London for four years and work as a software engineer.",
                    "I have lived in London since four years and work as a software engineer.",
                    "I am living in London for four years and work like an engineer."
                ],
                "correct_index": 1,
                "explanation": "'have lived' + 'for four years' (duration) + 'work as an engineer' (profession)."
            },
            {
                "id": "b1_rev_as_2",
                "question": "Choose the most appropriate Topic Sentence for an essay on remote work:",
                "options": [
                    "Remote work is something that people do at home with computers.",
                    "The shift to telecommuting has substantially augmented employee autonomy while presenting novel collaboration challenges for corporate management.",
                    "I like working at home because my bed is near.",
                    "Computers are very fast nowadays."
                ],
                "correct_index": 1,
                "explanation": "Provides a balanced, academic, arguable controlling claim suitable for upper-intermediate essays."
            },
            {
                "id": "b1_rev_as_3",
                "question": "In formal correspondence, if you open with 'Dear Sir/Madam,', which sign-off is mandatory?",
                "options": [
                    "Yours sincerely,",
                    "Yours faithfully,",
                    "Kind regards,",
                    "Warmly,"
                ],
                "correct_index": 1,
                "explanation": "Anonymous formal opening ('Dear Sir/Madam') strictly pairs with 'Yours faithfully,'."
            }
        ]
    }
]

with open("content/curriculum/b1.json", "w", encoding="utf-8") as f:
    json.dump(B1_LESSONS, f, indent=2, ensure_ascii=False)
print("Saved B1:", len(B1_LESSONS), "lessons.")
