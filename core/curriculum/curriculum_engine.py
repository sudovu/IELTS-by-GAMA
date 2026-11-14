"""
Curriculum Engine for IELTS by GAMA.
Delivers a structured, pedagogically sound English Learning Academy curriculum
from CEFR A1 (Beginner) through C2 (Proficiency) across Grammar, Vocabulary,
Reading, Listening, Writing, and Speaking.
"""

import json
from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import CurriculumRepository, LearnerRepository, MistakeBookRepository


STARTER_LESSONS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # CEFR A1 — BEGINNER
    # -------------------------------------------------------------------------
    {
        "id": "curric_a1_gram_present_simple",
        "cefr_level": "A1",
        "module_type": "grammar",
        "title": "Present Simple & Subject-Verb Concord",
        "order_index": 1,
        "objectives": [
            "Understand when to use the Present Simple for habits, routines, and universal truths.",
            "Master third-person singular inflection ('-s' / '-es').",
            "Formulate accurate negative sentences using 'do not' and 'does not'."
        ],
        "explanation_markdown": """### Present Simple Mechanics
The Present Simple is the foundational tense used to express:
1. **Habits and Daily Routines**: *I review vocabulary every morning.*
2. **Permanent States & Facts**: *Water boils at 100 degrees Celsius.*

#### Structural Rules:
- **I / You / We / They**: Base verb (*walk, study, live*)
- **He / She / It**: Base verb + **-s / -es** (*walks, studies, lives*)
- **Negative Concord**: Subject + **do not (don't) / does not (doesn't)** + base verb. (Never add '-s' to the main verb after 'does not').""",
        "examples": [
            {"text": "She studies English for forty minutes every evening.", "notes": "Third-person singular 'she' requires 'studies'."},
            {"text": "They do not live in the city center.", "notes": "'They' takes auxiliary 'do not' + base form 'live'."},
            {"text": "The library opens at eight o'clock in the morning.", "notes": "Factual schedule uses simple present."}
        ],
        "guided_exercises": [
            {"id": "a1_ge_1", "prompt": "My brother _____ (work) in a hospital in Manchester.", "answer": "works", "explanation": "'My brother' is third-person singular (he), requiring '-s'."},
            {"id": "a1_ge_2", "prompt": "We _____ (not / understand) this difficult sentence.", "answer": "do not understand", "explanation": "'We' requires 'do not' (or 'don't') followed by base verb."}
        ],
        "interactive_practice": [
            {
                "id": "a1_ip_1",
                "question": "Which sentence demonstrates correct third-person singular subject concord?",
                "options": [
                    "He watch documentary films on weekends.",
                    "He watches documentary films on weekends.",
                    "He is watches documentary films on weekends.",
                    "He watching documentary films on weekends."
                ],
                "correct_index": 1,
                "explanation": "Verbs ending in '-ch' take '-es' in third-person singular: 'watches'."
            }
        ],
        "assessment": [
            {
                "id": "a1_as_1",
                "question": "Choose the correct negative form: 'Sarah _____ coffee after dinner.'",
                "options": [
                    "doesn't drinks",
                    "don't drink",
                    "doesn't drink",
                    "not drinks"
                ],
                "correct_index": 2,
                "explanation": "'Sarah' (she) takes 'doesn't' + base verb 'drink'."
            },
            {
                "id": "a1_as_2",
                "question": "Select the correct sentence:",
                "options": [
                    "The Earth orbits around the Sun.",
                    "The Earth orbit around the Sun.",
                    "The Earth is orbit around the Sun.",
                    "The Earth orbiting around the Sun."
                ],
                "correct_index": 0,
                "explanation": "Universal scientific facts take the present simple singular: 'orbits'."
            }
        ]
    },
    {
        "id": "curric_a1_vocab_everyday_essentials",
        "cefr_level": "A1",
        "module_type": "vocabulary",
        "title": "Everyday Essentials: Numbers, Family & Time",
        "order_index": 2,
        "objectives": [
            "Learn essential foundational vocabulary for time, dates, and family relationships.",
            "Use cardinal and ordinal numbers accurately in spoken and written contexts.",
            "Express daily schedules using appropriate prepositions of time ('at', 'in', 'on')."
        ],
        "explanation_markdown": """### Core Daily Lexis
Mastering everyday terms provides the essential building blocks for basic conversational fluency.

#### Prepositions of Time:
- **AT**: Specific times & points (*at 7:30 PM, at midnight, at noon*)
- **ON**: Days and specific dates (*on Monday, on October 15th*)
- **IN**: Months, years, seasons, and long periods (*in November, in 2026, in the morning*)""",
        "examples": [
            {"text": "The introductory lecture begins at nine o'clock on Monday.", "notes": "'At' for specific time, 'on' for day."},
            {"text": "My grandmother was born in 1952.", "notes": "'In' for calendar years."}
        ],
        "guided_exercises": [
            {"id": "a1_v_ge_1", "prompt": "The examination takes place _____ Tuesday afternoon.", "answer": "on", "explanation": "Days of the week take the preposition 'on'."}
        ],
        "interactive_practice": [
            {
                "id": "a1_v_ip_1",
                "question": "Select the correct preposition: 'The flight departs _____ midnight.'",
                "options": ["in", "on", "at", "to"],
                "correct_index": 2,
                "explanation": "Points of time like 'midnight' and 'noon' require 'at'."
            }
        ],
        "assessment": [
            {
                "id": "a1_v_as_1",
                "question": "Which phrase correctly states a morning schedule?",
                "options": [
                    "The class begins at 8:00 AM on Friday.",
                    "The class begins in 8:00 AM at Friday.",
                    "The class begins on 8:00 AM in Friday.",
                    "The class begins to 8:00 AM by Friday."
                ],
                "correct_index": 0,
                "explanation": "'At' for exact hour, 'on' for day of the week."
            }
        ]
    },
    {
        "id": "curric_a1_speak_introductions",
        "cefr_level": "A1",
        "module_type": "speaking",
        "title": "Self-Introductions & Personal Information",
        "order_index": 3,
        "objectives": [
            "Introduce oneself clearly and naturally in a formal or informal setting.",
            "State your nationality, occupation, and home city accurately.",
            "Spell your name using clear English phonetics."
        ],
        "explanation_markdown": """### Personal Identification & Introductions
In IELTS Speaking Part 1 and daily interactions, examiners expect fluent, confident delivery of basic personal details.

#### Key Formulae:
- *Greeting + Name*: 'Good morning, my name is [Name], but you can call me [Nickname].'
- *Origin & Residence*: 'I am originally from [City/Country], which is situated in...'
- *Occupation*: 'At present, I am an undergraduate student majoring in [Field] / working as a [Job].'""",
        "examples": [
            {"text": "Good morning. My name is Bhuwan Gautam, and I come from Kathmandu, Nepal.", "notes": "Clear, professional, and grammatically complete opening statement."}
        ],
        "guided_exercises": [
            {"id": "a1_sp_ge_1", "prompt": "Complete: 'I am _____ from Pokhara, a scenic city in Nepal.'", "answer": "originally", "explanation": "'Originally' indicates birth or hometown origin."}
        ],
        "interactive_practice": [
            {
                "id": "a1_sp_ip_1",
                "question": "Which response is the most natural answer to 'Where are you from?'",
                "options": [
                    "I am coming from Spain.",
                    "I am from Valencia, which is on the eastern coast of Spain.",
                    "I come to Spain since five years.",
                    "My country is Spain from where I am."
                ],
                "correct_index": 1,
                "explanation": "State city, origin, and an informative geographical clause for natural fluency."
            }
        ],
        "assessment": [
            {
                "id": "a1_sp_as_1",
                "question": "In an official interview, how should you introduce your occupation?",
                "options": [
                    "I work like an accountant.",
                    "I am working as an accountant at an international firm.",
                    "My job is make accounting.",
                    "I do accountant since three months."
                ],
                "correct_index": 1,
                "explanation": "'Work as a/an [profession]' is the natural, idiomatic construction."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # CEFR A2 — ELEMENTARY
    # -------------------------------------------------------------------------
    {
        "id": "curric_a2_gram_past_simple",
        "cefr_level": "A2",
        "module_type": "grammar",
        "title": "Past Simple & Completed Actions",
        "order_index": 1,
        "objectives": [
            "Use the Past Simple to narrate finished past events at a specific time.",
            "Distinguish between regular verbs ('-ed') and common irregular verbs.",
            "Construct accurate negative and question forms with auxiliary 'did'."
        ],
        "explanation_markdown": """### Past Simple Mechanics
The Past Simple denotes actions completed in the past with a definite time reference (explicit or implied).

#### Key Formulations:
- **Affirmative**: Subject + Past Verb (*walked, bought, went*)
- **Negative**: Subject + **did not (didn't)** + **base verb** (*She didn't visit Paris*, NOT *didn't visited*)
- **Questions**: **Did** + Subject + **base verb**? (*Did you complete the assignment?*)""",
        "examples": [
            {"text": "The international committee published their initial findings yesterday.", "notes": "Regular '-ed' verb with explicit time marker 'yesterday'."},
            {"text": "We did not receive the official confirmation letter last week.", "notes": "'Did not' takes base verb 'receive'."}
        ],
        "guided_exercises": [
            {"id": "a2_ge_1", "prompt": "Yesterday, they _____ (see) an informative documentary on renewable energy.", "answer": "saw", "explanation": "Irregular past of 'see' is 'saw'."}
        ],
        "interactive_practice": [
            {
                "id": "a2_ip_1",
                "question": "Identify the grammatically correct past negative sentence:",
                "options": [
                    "He didn't went to the laboratory yesterday.",
                    "He didn't go to the laboratory yesterday.",
                    "He not went to the laboratory yesterday.",
                    "He wasn't go to the laboratory yesterday."
                ],
                "correct_index": 1,
                "explanation": "Auxiliary 'didn't' must be paired with the base verb 'go'."
            }
        ],
        "assessment": [
            {
                "id": "a2_as_1",
                "question": "Choose the correct past question form:",
                "options": [
                    "Did she finished the report on time?",
                    "Did she finish the report on time?",
                    "Does she finished the report on time?",
                    "Was she finish the report on time?"
                ],
                "correct_index": 1,
                "explanation": "'Did' + subject + base form 'finish'."
            }
        ]
    },
    {
        "id": "curric_a2_vocab_travel_transport",
        "cefr_level": "A2",
        "module_type": "vocabulary",
        "title": "Travel, Commuting & Urban Geography",
        "order_index": 2,
        "objectives": [
            "Expand lexis related to public transportation, urban transit, and travel logistics.",
            "Understand functional transit terms like 'commute', 'fare', 'congestion', 'delay'.",
            "Discuss transport advantages and drawbacks accurately."
        ],
        "explanation_markdown": """### Transit & Urban Vocabulary
Transportation is a frequent topic in IELTS Speaking Part 1 and General Training Reading.

#### High-Yield Terms:
- **Commute**: The daily journey between home and work.
- **Congestion**: Heavy traffic blocking roadways.
- **Transit network**: The system of buses, trains, and subways in a metropolitan area.
- **Fare**: The money paid for a ticket on public transport.""",
        "examples": [
            {"text": "Many urban professionals commute by underground train to avoid road congestion.", "notes": "Demonstrates high-frequency transport lexis."}
        ],
        "guided_exercises": [
            {"id": "a2_v_ge_1", "prompt": "Traffic _____ (congestion / ticket) causes significant delays during rush hour.", "answer": "congestion", "explanation": "'Congestion' specifically describes blocked road traffic."}
        ],
        "interactive_practice": [
            {
                "id": "a2_v_ip_1",
                "question": "What is the term for the daily journey people make to their workplace?",
                "options": ["Voyage", "Commute", "Expedition", "Excursion"],
                "correct_index": 1,
                "explanation": "'Commute' specifically refers to routine travel to and from work."
            }
        ],
        "assessment": [
            {
                "id": "a2_v_as_1",
                "question": "Fill in the blank: 'Rail subsidies ensure that public transport _____ remain affordable.'",
                "options": ["fares", "prices", "debts", "penalties"],
                "correct_index": 0,
                "explanation": "The price paid for transit journeys is specifically called a 'fare'."
            }
        ]
    },
    {
        "id": "curric_a2_read_scanning_notices",
        "cefr_level": "A2",
        "module_type": "reading",
        "title": "Scanning Notices & Informational Announcements",
        "order_index": 3,
        "objectives": [
            "Distinguish skimming for general gist from scanning for specific facts.",
            "Locate opening hours, eligibility rules, and contact information rapidly.",
            "Avoid common distractor options in informational matching questions."
        ],
        "explanation_markdown": """### Scanning Strategy
Scanning is reading rapidly with a specific keyword or data point in mind (names, dates, figures, capitalized terms).

#### Essential Technique:
1. Identify the **question keyword** (e.g. 'registration deadline').
2. Move your eyes systematically over the text looking **only** for that keyword or its synonym.
3. Once located, read the **surrounding clause** carefully to verify the exact meaning.""",
        "examples": [
            {"text": "Notice: 'Submissions accepted until 5:00 PM on Friday, November 14th.' Keyword: deadline -> Friday, Nov 14th.", "notes": "Direct keyword-to-text correlation."}
        ],
        "guided_exercises": [
            {"id": "a2_r_ge_1", "prompt": "Text: 'Members receive free admission; non-members pay £12.' Q: How much is admission for members? (Answer: free)", "answer": "free", "explanation": "Targeted scanning directly yields 'free'."}
        ],
        "interactive_practice": [
            {
                "id": "a2_r_ip_1",
                "question": "What is the primary difference between skimming and scanning?",
                "options": [
                    "Skimming is looking for a specific number; scanning is understanding the whole text.",
                    "Skimming captures the overall gist; scanning searches for specific pieces of information.",
                    "Skimming is reading backwards; scanning is reading out loud.",
                    "There is no difference between the two techniques."
                ],
                "correct_index": 1,
                "explanation": "Skimming grasps the general theme; scanning locates precise target details."
            }
        ],
        "assessment": [
            {
                "id": "a2_r_as_1",
                "question": "Notice: 'The facility is closed for routine maintenance on alternate Mondays.' Is the facility open every Monday?",
                "options": ["Yes", "No", "Not Given"],
                "correct_index": 1,
                "explanation": "'Alternate Mondays' means every other Monday it is closed, so it is not open every Monday."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # CEFR B1 — INTERMEDIATE
    # -------------------------------------------------------------------------
    {
        "id": "curric_b1_gram_present_perfect",
        "cefr_level": "B1",
        "module_type": "grammar",
        "title": "Present Perfect vs. Past Simple Distinction",
        "order_index": 1,
        "objectives": [
            "Accurately differentiate between unfinished time (Present Perfect) and finished time (Past Simple).",
            "Use 'for' (duration) and 'since' (starting point) with precision.",
            "Avoid combining finished past time markers with the Present Perfect."
        ],
        "explanation_markdown": """### The Crucial Tense Boundary
A universal IELTS error is using the Present Perfect with finished time expressions.

#### Rules of Distinction:
1. **Present Perfect (have/has + past participle)**:
   - Connects the past to the present moment.
   - Used with **unfinished time**: *today, this week, recently, ever, so far*.
   - Used with **for** (period: *for five years*) and **since** (starting point: *since 2021*).
2. **Past Simple**:
   - Strictly for **completed past time**: *yesterday, in 2019, three weeks ago, last century*.
   - Never say: *'I have seen him yesterday.'* (Say: *'I saw him yesterday.'*)""",
        "examples": [
            {"text": "Researchers have investigated renewable solar materials for over a decade.", "notes": "Ongoing inquiry spanning past into present."},
            {"text": "The laboratory was inaugurated in 2018.", "notes": "Specific completed historical point requires past simple."}
        ],
        "guided_exercises": [
            {"id": "b1_ge_1", "prompt": "She has lived in Sydney _____ (for / since) three years.", "answer": "for", "explanation": "'Three years' is a duration of time, requiring 'for'."},
            {"id": "b1_ge_2", "prompt": "She has lived in Sydney _____ (for / since) 2023.", "answer": "since", "explanation": "'2023' is a specific starting point in the past, requiring 'since'."}
        ],
        "interactive_practice": [
            {
                "id": "b1_ip_1",
                "question": "Which sentence contains a grammatical error?",
                "options": [
                    "I have visited London several times.",
                    "I have visited London two months ago.",
                    "I visited London two months ago.",
                    "I have lived in London since 2020."
                ],
                "correct_index": 1,
                "explanation": "'Two months ago' is a finished time marker and cannot accompany the Present Perfect 'have visited'."
            }
        ],
        "assessment": [
            {
                "id": "b1_as_1",
                "question": "Select the correct sentence:",
                "options": [
                    "The company has released three new software patches last month.",
                    "The company released three new software patches last month.",
                    "The company was release three new software patches last month.",
                    "The company has been released three new software patches last month."
                ],
                "correct_index": 1,
                "explanation": "'Last month' denotes finished time; the Past Simple 'released' is required."
            }
        ]
    },
    {
        "id": "curric_b1_vocab_workplace_education",
        "cefr_level": "B1",
        "module_type": "vocabulary",
        "title": "Workplace Dynamics, Careers & Higher Education",
        "order_index": 2,
        "objectives": [
            "Learn academic and workplace terminology: 'vocational', 'curriculum', 'probationary', 'remuneration'.",
            "Discuss professional credentials, responsibilities, and tertiary education comfortably.",
            "Form word families (e.g. compete -> competitive -> competition)."
        ],
        "explanation_markdown": """### Career & Education Lexis
Education and employment are central themes across IELTS Speaking Part 3 and Academic Writing Task 2.

#### Key Academic Terminology:
- **Tertiary education**: University or college-level higher education.
- **Vocational training**: Practical technical education aimed at specific skilled trades.
- **Curriculum**: The comprehensive academic courses offered by an educational institution.
- **Remuneration**: Financial compensation or salary paid for work performed.""",
        "examples": [
            {"text": "Investing in tertiary education equips graduates with specialized technical competencies.", "notes": "Band 7+ formulation for educational essays."}
        ],
        "guided_exercises": [
            {"id": "b1_v_ge_1", "prompt": "Practical, hands-on training for trades is known as _____ (vocational / theoretical) education.", "answer": "vocational", "explanation": "'Vocational' denotes practical training for technical careers."}
        ],
        "interactive_practice": [
            {
                "id": "b1_v_ip_1",
                "question": "Which term describes formal university-level education following secondary school?",
                "options": ["Primary education", "Secondary education", "Tertiary education", "Elementary education"],
                "correct_index": 2,
                "explanation": "'Tertiary education' is the formal academic designation for university study."
            }
        ],
        "assessment": [
            {
                "id": "b1_v_as_1",
                "question": "Choose the correct collocation: 'Universities must regularly update their academic _____ to reflect technological change.'",
                "options": ["curriculum", "commute", "fare", "repetition"],
                "correct_index": 0,
                "explanation": "'Academic curriculum' is the precise academic collocation."
            }
        ]
    },
    {
        "id": "curric_b1_write_cohesion_linkers",
        "cefr_level": "B1",
        "module_type": "writing",
        "title": "Paragraph Architecture & Cohesive Discourse Linkers",
        "order_index": 3,
        "objectives": [
            "Construct clear topic sentences that state the main controlling idea.",
            "Employ varied cohesive devices (addition, contrast, cause-and-effect) correctly.",
            "Punctuate sentence linkers with proper comma conventions."
        ],
        "explanation_markdown": """### Paragraph Cohesion & Signposting
Coherence and Cohesion accounts for 25% of your IELTS Writing score.

#### Categories of Discourse Connectors:
- **Contrast**: *However, Nevertheless, In contrast, On the other hand* (Followed by comma when initiating a sentence).
- **Cause & Consequence**: *Consequently, Therefore, As a result, Thus*.
- **Addition**: *Furthermore, Moreover, In addition, Additionally*.
- **Exemplification**: *For instance, To illustrate, Specifically*.""",
        "examples": [
            {"text": "Renewable energy infrastructure requires substantial capital investment. Consequently, government subsidies are vital.", "notes": "'Consequently' indicates the logical cause-and-effect outcome."}
        ],
        "guided_exercises": [
            {"id": "b1_w_ge_1", "prompt": "Electric vehicles produce zero tailpipe emissions. _____, (However / Furthermore) their production requires scarce battery minerals.", "answer": "However", "explanation": "Contrasting advantage with a drawback requires 'However'."}
        ],
        "interactive_practice": [
            {
                "id": "b1_w_ip_1",
                "question": "Which connector logically introduces a consequence?",
                "options": ["In addition", "Therefore", "Whereas", "Despite"],
                "correct_index": 1,
                "explanation": "'Therefore' signals a direct logical consequence."
            }
        ],
        "assessment": [
            {
                "id": "b1_w_as_1",
                "question": "Select the properly punctuated cohesive sentence:",
                "options": [
                    "Furthermore strict penalties deter corporate polluters.",
                    "Furthermore, strict penalties deter corporate polluters.",
                    "Furthermore; strict penalties deter corporate polluters.",
                    "Furthermore: strict penalties deter corporate polluters."
                ],
                "correct_index": 1,
                "explanation": "Sentence-initial conjunctive adverbs like 'Furthermore' must be followed by a comma."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # CEFR B2 — UPPER INTERMEDIATE
    # -------------------------------------------------------------------------
    {
        "id": "curric_b2_gram_conditionals",
        "cefr_level": "B2",
        "module_type": "grammar",
        "title": "Hypothetical Conditionals & Mixed Forms in Academic Arguments",
        "order_index": 1,
        "objectives": [
            "Construct Second, Third, and Mixed Conditionals with accurate clause structures.",
            "Formulate policy proposals using hypothetical subjunctive frames ('If governments were to...').",
            "Eliminate redundant 'would' in conditional if-clauses."
        ],
        "explanation_markdown": """### Advanced Conditional Architecture
Conditionals showcase Band 7+ Grammatical Range by expressing probability, nuance, and hypothetical outcomes.

#### Structural Paradigms:
1. **Second Conditional (Unreal Present/Future)**:
   - *If + Past Simple, would + base verb*
   - Formal subjunctive: *If the government **were** to enact stricter zoning laws, urban sprawl **would diminish**.*
2. **Third Conditional (Unreal Past)**:
   - *If + had + past participle, would have + past participle*
   - *If authorities **had intervened** earlier, the economic crisis **would have been averted**.*
3. **Mixed Conditional (Past Action -> Present Result)**:
   - *If + had + past participle, would + base verb*
   - *If municipal councils **had modernized** transit decades ago, our city **would not face** gridlock today.*""",
        "examples": [
            {"text": "If municipal councils were to invest in light rail, inner-city pollution would decline substantially.", "notes": "Formal hypothetical proposal for IELTS Task 2."}
        ],
        "guided_exercises": [
            {"id": "b2_ge_1", "prompt": "If scientists _____ (not / develop) mRNA technology, vaccine production would have been severely delayed.", "answer": "had not developed", "explanation": "Third conditional unreal past requires 'had not developed'."}
        ],
        "interactive_practice": [
            {
                "id": "b2_ip_1",
                "question": "Which sentence demonstrates a correct mixed conditional?",
                "options": [
                    "If she had studied medicine, she would be a doctor today.",
                    "If she studied medicine, she would be a doctor today.",
                    "If she would have studied medicine, she had been a doctor today.",
                    "If she has studied medicine, she will be a doctor today."
                ],
                "correct_index": 0,
                "explanation": "Past condition ('had studied') yielding present ongoing status ('would be a doctor today')."
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
        ]
    },
    {
        "id": "curric_b2_vocab_academic_word_list",
        "cefr_level": "B2",
        "module_type": "vocabulary",
        "title": "Academic Word List (AWL) Sublist 1 Mastery",
        "order_index": 2,
        "objectives": [
            "Master essential AWL Sublist 1 terms: *analyze, approach, concept, constituent, derive, establish*.",
            "Use precise academic synonyms to replace colloquial expressions.",
            "Form correct collocations with abstract academic nouns."
        ],
        "explanation_markdown": """### Academic Word List (AWL)
The Academic Word List comprises 570 word families most frequently appearing in scholarly texts.

#### High-Yield Sublist 1 Verbs & Nouns:
- **Analyze (v.)**: To examine methodically and in detail. (*Empirical data was analyzed to test the hypothesis.*)
- **Derive (v.)**: To obtain something from a specified origin. (*Pharmaceutical compounds derived from rare flora.*)
- **Establish (v.)**: To prove or demonstrate conclusively. (*Studies have established a clear correlation.*)
- **Constituent (n.)**: An essential component part of an aggregate whole.""",
        "examples": [
            {"text": "Statistical analysis establishes a definitive correlation between dietary habits and cardiovascular wellness.", "notes": "Band 8 AWL usage in research reporting."}
        ],
        "guided_exercises": [
            {"id": "b2_v_ge_1", "prompt": "Scholars continue to _____ (analyze / look at) the socioeconomic implications of automation.", "answer": "analyze", "explanation": "'Analyze' replaces the informal phrasal verb 'look at' with academic precision."}
        ],
        "interactive_practice": [
            {
                "id": "b2_v_ip_1",
                "question": "Which word is the most academically appropriate synonym for 'get' in: 'The researchers _____ their conclusions from rigorous field data.'",
                "options": ["got", "derived", "grabbed", "received"],
                "correct_index": 1,
                "explanation": "'Derived' signifies formally deducing or extracting findings from scientific evidence."
            }
        ],
        "assessment": [
            {
                "id": "b2_v_as_1",
                "question": "Choose the optimal academic collocation: 'Recent sociological surveys have _____ a clear link between screen time and sleep quality.'",
                "options": ["established", "built", "fixed", "settled"],
                "correct_index": 0,
                "explanation": "'Establish a link / correlation' is an essential academic collocation."
            }
        ]
    },
    {
        "id": "curric_b2_write_peel_paragraph_technique",
        "cefr_level": "B2",
        "module_type": "writing",
        "title": "PEEL Paragraph Architecture for IELTS Writing Task 2",
        "order_index": 3,
        "objectives": [
            "Structure body paragraphs using Point, Explanation, Evidence, and Link (PEEL).",
            "Develop arguments deeply rather than merely listing superficial points.",
            "Connect paragraph conclusions back to the overarching thesis statement."
        ],
        "explanation_markdown": """### The PEEL Methodology
The PEEL method ensures every paragraph meets the Task Response criteria for Band 7+ (clear central topic, fully extended and supported ideas).

#### The 4 Stages:
1. **P — Point**: State the central claim clearly in a strong topic sentence.
2. **E — Explanation**: Explain why and how this point operates in reality.
3. **E — Evidence / Example**: Provide concrete empirical, historical, or logical evidence.
4. **L — Link**: Synthesize the point and link directly back to the question or overall essay thesis.""",
        "examples": [
            {"text": "P: Investing in renewable infrastructure accelerates economic diversification. E: By developing wind and solar installations, developing nations diminish reliance on volatile fossil imports. E: For instance, Uruguay transitioned to 98% renewable grid electricity within a single decade. L: Hence, sustainable transition safeguards fiscal stability.", "notes": "Complete, seamless PEEL progression."}
        ],
        "guided_exercises": [
            {"id": "b2_w_ge_1", "prompt": "In the PEEL acronym, what does the second 'E' represent? (Answer: Evidence or Example)", "answer": "Evidence", "explanation": "'Evidence' or 'Example' provides concrete factual grounding for the preceding explanation."}
        ],
        "interactive_practice": [
            {
                "id": "b2_w_ip_1",
                "question": "What is the primary function of the 'Link' sentence in a PEEL paragraph?",
                "options": [
                    "To introduce a completely new, unrelated argument.",
                    "To summarize the evidence and tie the argument back to the essay's core question or thesis.",
                    "To write out a list of citations and authors.",
                    "To ask the examiner a rhetorical question."
                ],
                "correct_index": 1,
                "explanation": "The link sentence unites the paragraph's specific reasoning back to the macro thesis."
            }
        ],
        "assessment": [
            {
                "id": "b2_w_as_1",
                "question": "Which of the following serves best as a clear Topic Sentence (Point)?",
                "options": [
                    "There are many things about technology that are both good and bad.",
                    "Primarily, ubiquitous smartphone integration has compromised workplace productivity by fragmenting employee concentration.",
                    "For example, a study showed that people look at phones 100 times.",
                    "In conclusion, phones are very widespread in modern offices."
                ],
                "correct_index": 1,
                "explanation": "Option 2 is an assertive, analytical topic sentence introducing a clear controlling idea."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # CEFR C1 — ADVANCED
    # -------------------------------------------------------------------------
    {
        "id": "curric_c1_gram_inversion",
        "cefr_level": "C1",
        "module_type": "grammar",
        "title": "Negative & Restrictive Adverbial Inversion",
        "order_index": 1,
        "objectives": [
            "Deploy negative adverbials ('Seldom', 'Rarely', 'Not only', 'Scarcely') at sentence onset.",
            "Invert subject and auxiliary verb accurately according to question word order.",
            "Apply inversion purposefully for dramatic emphasis and elevated academic register."
        ],
        "explanation_markdown": """### Grammatical Inversion (Band 8+ Descriptor Indicator)
Inverting sentence order after restrictive or negative adverbials demonstrates sophisticated grammatical command.

#### Formula:
**Negative Adverbial + Auxiliary Verb + Subject + Main Verb**

#### Core Patterns:
- **Not only... but also**: *Not only **does** automation **increase** productivity, but it also reduces workplace injuries.*
- **Seldom / Rarely**: *Seldom **have** economists **witnessed** such rapid capital reallocation.*
- **Under no circumstances**: *Under no circumstances **should** ethical oversight **be compromised**.*
- **Only when / Only after**: *Only when governments coordinate fiscal policies **will** global inflation stabilize.*""",
        "examples": [
            {"text": "Rarely do modern educational systems cultivate autonomous critical thinking alongside rote examination skills.", "notes": "Band 8.5 inverted rhetorical opening."}
        ],
        "guided_exercises": [
            {"id": "c1_ge_1", "prompt": "Seldom _____ (have / do / are) climatologists recorded such rapid glacial retreat.", "answer": "have", "explanation": "Perfect aspect inversion: 'Seldom have [subject] recorded'."}
        ],
        "interactive_practice": [
            {
                "id": "c1_ip_1",
                "question": "Select the correctly structured inversion sentence:",
                "options": [
                    "Not only automation lowers manufacturing costs, but it creates new engineering sectors.",
                    "Not only does automation lower manufacturing costs, but it also creates new engineering sectors.",
                    "Not only lowers automation manufacturing costs, but it creates sectors.",
                    "Not only automation does lower manufacturing costs, but it also creates new sectors."
                ],
                "correct_index": 1,
                "explanation": "Inversion requires auxiliary 'does' immediately following 'Not only', before the subject 'automation'."
            }
        ],
        "assessment": [
            {
                "id": "c1_as_1",
                "question": "Rewrite using inversion: 'We rarely see such exemplary academic scholarship.'",
                "options": [
                    "Rarely we see such exemplary academic scholarship.",
                    "Rarely do we see such exemplary academic scholarship.",
                    "Rarely are we see such exemplary academic scholarship.",
                    "Rarely did we seen such exemplary academic scholarship."
                ],
                "correct_index": 1,
                "explanation": "'Rarely' + auxiliary 'do' + subject 'we' + base verb 'see'."
            }
        ]
    },
    {
        "id": "curric_c1_vocab_academic_collocations",
        "cefr_level": "C1",
        "module_type": "vocabulary",
        "title": "Nuanced Academic Collocations & Collocational Chains",
        "order_index": 2,
        "objectives": [
            "Use natural collocational pairings: *mitigate risk, exert influence, exacerbate disparities, foster innovation*.",
            "Avoid literal translations and awkward unidiomatic phrasings.",
            "Vary sentence registers between analytical reporting and critical appraisal."
        ],
        "explanation_markdown": """### Advanced Collocational Precision
At Band 8 and 9, candidates do not merely know difficult words; they use words in their precise, natural lexical habitats.

#### High-Yield Academic Pairings:
- **Exacerbate disparities**: To make existing inequalities significantly worse.
- **Mitigate deleterious effects**: To reduce harmful outcomes.
- **Foster interdisciplinary collaboration**: To actively nurture cooperation between fields.
- **Incur substantial expenditure**: To encounter or take on heavy costs.""",
        "examples": [
            {"text": "Failure to regulate algorithmic hiring platforms risks exacerbating existing socioeconomic disparities.", "notes": "Band 8.5 lexical precision."}
        ],
        "guided_exercises": [
            {"id": "c1_v_ge_1", "prompt": "Government subsidies are designed to _____ (mitigate / heal) the economic shock of inflation.", "answer": "mitigate", "explanation": "'Mitigate' collocates with impact, shock, and risk."}
        ],
        "interactive_practice": [
            {
                "id": "c1_v_ip_1",
                "question": "Which verb naturally collocates with 'influence' in: 'Social media algorithms _____ a profound influence over adolescent behavior.'",
                "options": ["make", "exert", "do", "execute"],
                "correct_index": 1,
                "explanation": "'Exert influence' is the standard academic and stylistic collocation."
            }
        ],
        "assessment": [
            {
                "id": "c1_v_as_1",
                "question": "Choose the optimal collocation: 'Inadequate urban drainage systems will inevitably _____ the severity of monsoon flooding.'",
                "options": ["exacerbate", "enlarge", "multiply", "broaden"],
                "correct_index": 0,
                "explanation": "'Exacerbate severity' is the precise academic collocation for worsening a negative condition."
            }
        ]
    },
    {
        "id": "curric_c1_speak_discourse_markers",
        "cefr_level": "C1",
        "module_type": "speaking",
        "title": "Spoken Fluency Discourse Markers & Epistemic Stance",
        "order_index": 3,
        "objectives": [
            "Deploy sophisticated spoken markers (*'From an economic standpoint'*, *'Broadly speaking'*, *'To be perfectly candid'*).",
            "Demonstrate natural hesitation markers and self-correction without losing coherence.",
            "Qualify generalizations with epistemic modality (*'tends to suggest'*, *'in all likelihood'*)."
        ],
        "explanation_markdown": """### Spoken Coherence & Epistemic Stance
In IELTS Speaking Part 3, Band 8 candidates maintain effortless fluency while conveying nuanced viewpoints.

#### Advanced Spoken Signposts:
- **Perspective framing**: *'From an environmental standpoint...' / 'In terms of fiscal policy...'*
- **Hedging & Stance**: *'I would argue that, in all likelihood,...' / 'There is an argument to be made that...'*
- **Concession before rebuttal**: *'While I readily acknowledge the merits of that position, one cannot overlook...' *""",
        "examples": [
            {"text": "Well, from a sociological vantage point, urbanization is something of a double-edged sword.", "notes": "Sophisticated framing paired with an idiomatic concept."}
        ],
        "guided_exercises": [
            {"id": "c1_sp_ge_1", "prompt": "Complete the framing phrase: 'From a technological _____ (point / standpoint), AI accelerates diagnostic accuracy.'", "answer": "standpoint", "explanation": "'From a [domain] standpoint' frames analytical perspectives."}
        ],
        "interactive_practice": [
            {
                "id": "c1_sp_ip_1",
                "question": "Which phrase provides the most natural, sophisticated transition to concede a counter-argument before offering your own critique?",
                "options": [
                    "I hate this opinion, so I think...",
                    "While that argument undoubtedly holds merit, it fails to account for...",
                    "People say this and it is wrong because...",
                    "On the other side of the coin, no."
                ],
                "correct_index": 1,
                "explanation": "Respectful academic concession followed by critical extension demonstrates C1 spoken mastery."
            }
        ],
        "assessment": [
            {
                "id": "c1_sp_as_1",
                "question": "In speaking, which expression best prevents an unverified over-generalization?",
                "options": [
                    "Everyone in the world always does this.",
                    "The empirical evidence tends to indicate that this pattern is predominant.",
                    "This is 100% definitely true without any question.",
                    "Nobody can disagree with this fact."
                ],
                "correct_index": 1,
                "explanation": "'Tends to indicate' constitutes academic hedging, a hallmark of Band 8+ fluency."
            }
        ]
    },

    # -------------------------------------------------------------------------
    # CEFR C2 — PROFICIENCY
    # -------------------------------------------------------------------------
    {
        "id": "curric_c2_gram_cleft_sentences",
        "cefr_level": "C2",
        "module_type": "grammar",
        "title": "Cleft Sentences & Discourse Topicalization",
        "order_index": 1,
        "objectives": [
            "Formulate it-clefts and wh-clefts (pseudo-clefts) to emphasize precise arguments.",
            "Topicalize key discourse entities to control reader focus in scholarly prose.",
            "Distinguish stylistic emphasis from grammatical redundancy."
        ],
        "explanation_markdown": """### Cleft Sentences & Structural Foregrounding
Cleft sentences split a single proposition across two clauses to place emphatic focus on a particular constituent.

#### 1. It-Clefts:
- **Formula**: *It + be + focused element + that/who-clause*
- *Standard*: The lack of infrastructure hindered growth.
- *It-Cleft*: *It was **the chronic lack of infrastructure** that hindered growth.*

#### 2. Wh- / Pseudo-Clefts:
- **Formula**: *What + clause + be + focused element*
- *Standard*: We require international legislative consensus.
- *Wh-Cleft*: *What the international community urgently requires **is robust legislative consensus**.*""",
        "examples": [
            {"text": "What is particularly striking about these findings is the sheer velocity of oceanic temperature elevation.", "notes": "Wh-cleft structuring emphasizing analytical significance."}
        ],
        "guided_exercises": [
            {"id": "c2_ge_1", "prompt": "Transform to an it-cleft: 'Human negligence caused the industrial disaster.' -> 'It was human negligence _____ caused the industrial disaster.'", "answer": "that", "explanation": "'It was [focused element] that...' is the standard it-cleft formula."}
        ],
        "interactive_practice": [
            {
                "id": "c2_ip_1",
                "question": "Which sentence demonstrates an authentic pseudo-cleft (wh-cleft) construction?",
                "options": [
                    "What policy makers must recognize is that economic growth cannot occur in ecological isolation.",
                    "Policy makers must recognize what economic growth is.",
                    "It is policy makers that recognize economic growth.",
                    "Why policy makers recognize growth is because of ecology."
                ],
                "correct_index": 0,
                "explanation": "'What [clause] is [focused proposition]' forms a classic wh-cleft."
            }
        ],
        "assessment": [
            {
                "id": "c2_as_1",
                "question": "Choose the correctly framed it-cleft targeting causation:",
                "options": [
                    "It was precisely because public transit was privatized that fares skyrocketed.",
                    "It was precisely because public transit was privatized which fares skyrocketed.",
                    "What was precisely because public transit privatized that fares skyrocketed.",
                    "It is because public transit was privatized why fares skyrocketed."
                ],
                "correct_index": 0,
                "explanation": "'It was [prepositional cause] that [consequence]' is the precise grammatical formulation."
            }
        ]
    },
    {
        "id": "curric_c2_vocab_idiomatic_register",
        "cefr_level": "C2",
        "module_type": "vocabulary",
        "title": "Stylistic Register & Idiomatic Sophistication",
        "order_index": 2,
        "objectives": [
            "Master refined idiomatic concepts: *quintessential, sea change, watershed moment, double-edged sword*.",
            "Harmonize tone and stylistic register across sophisticated essays and critiques.",
            "Differentiate high-register academic metaphors from informal clichés."
        ],
        "explanation_markdown": """### Band 9 Stylistic Mastery
At the C2 Proficiency tier, language becomes artful, economical, and compellingly nuanced.

#### Elevated Idiomatic Expressions:
- **A watershed moment**: An event marking a decisive turning point in historical trajectory.
- **A sea change**: A profound, sweeping transformation in public attitude or policy.
- **A double-edged sword**: A phenomenon carrying both substantial benefits and latent perils.
- **The quintessential example**: The purest, most archetypal manifestation of a phenomenon.""",
        "examples": [
            {"text": "The advent of generative artificial intelligence represents a watershed moment in digital pedagogy.", "notes": "Eloquent, precise conceptualization."}
        ],
        "guided_exercises": [
            {"id": "c2_v_ge_1", "prompt": "A decisive historical turning point is metaphorically described as a _____ (watershed / waterfall) moment.", "answer": "watershed", "explanation": "'A watershed moment' is the standard idiomatic term."}
        ],
        "interactive_practice": [
            {
                "id": "c2_v_ip_1",
                "question": "Which idiomatic term describes a profound and comprehensive transformation?",
                "options": ["A lake change", "A sea change", "A river change", "An ocean shift"],
                "correct_index": 1,
                "explanation": "'A sea change' (originating in Shakespeare's The Tempest) denotes an irreversible radical transformation."
            }
        ],
        "assessment": [
            {
                "id": "c2_v_as_1",
                "question": "Select the sentence with impeccable C2 stylistic register:",
                "options": [
                    "The new law was super good and changed lots of stuff.",
                    "The landmark legislation represented a watershed moment that catalyzed a sea change in consumer privacy protections.",
                    "The law was really cool and made privacy great again.",
                    "Everyone knows the law was the best thing ever done."
                ],
                "correct_index": 1,
                "explanation": "Exemplifies elevated academic and stylistic register with natural high-level idiomatic precision."
            }
        ]
    },
    {
        "id": "curric_c2_read_implicit_author_stance",
        "cefr_level": "C2",
        "module_type": "reading",
        "title": "Deconstructing Irony, Hedging & Implicit Author Stance",
        "order_index": 3,
        "objectives": [
            "Detect subtle authorial tone, irony, skepticism, and implicit concession in complex texts.",
            "Deconstruct layered epistemic hedging in scientific peer-reviewed discourse.",
            "Master True/False/Not Given and Yes/No/Not Given questions at the highest tier of difficulty."
        ],
        "explanation_markdown": """### Deconstructing Implicit Stance
Band 8.5+ reading passages feature writers who do not announce their bias directly. Instead, they signal skepticism or endorsement through:
1. **Reporting Verbs**: *'claims', 'purports', 'alleges'* signal doubt; *'establishes', 'demonstrates', 'substantiates'* signal acceptance.
2. **Scare Quotes**: *The so-called 'breakthrough' was short-lived.*
3. **Subjunctive & Concessive Adverbials**: *'Plausible as this conjecture may seem at first blush, subsequent empirical scrutiny renders it untenable.'*""",
        "examples": [
            {"text": "Text: 'While proponents herald the initiative as revolutionary, the corroborating telemetry remains suspiciously sparse.' Stance: Skeptical.", "notes": "'Proponents herald' vs. 'suspiciously sparse' communicates clear doubt."}
        ],
        "guided_exercises": [
            {"id": "c2_r_ge_1", "prompt": "If a researcher says a theory 'purports to explain consciousness', does the researcher fully endorse the theory? (Yes / No)", "answer": "No", "explanation": "'Purports to' implies an unproven claim that the author regards with skepticism."}
        ],
        "interactive_practice": [
            {
                "id": "c2_r_ip_1",
                "question": "Author: 'It is arguably premature to dismantle traditional banking frameworks in favor of volatile cryptographic currencies.' What is the author's stance?",
                "options": [
                    "Strongly in favor of immediately adopting cryptographic currency.",
                    "Cautious and advising against rapid abandonment of established banking systems.",
                    "Indifferent and refusing to provide an opinion.",
                    "Believes traditional banking has already failed completely."
                ],
                "correct_index": 1,
                "explanation": "'Premature to dismantle' explicitly advocates caution against hasty replacement."
            }
        ],
        "assessment": [
            {
                "id": "c2_r_as_1",
                "question": "Sentence: 'The minister's much-vaunted environmental reform proved to be little more than rhetorical window-dressing.' The author's tone is:",
                "options": ["Enthusiastic and complimentary", "Skeptical and dismissive", "Objective and statistical", "Confused and uncertain"],
                "correct_index": 1,
                "explanation": "'Much-vaunted' and 'rhetorical window-dressing' convey sharp critique and dismissive skepticism."
            }
        ]
    }
]


class CurriculumEngine:
    """Manages structured CEFR curriculum, lesson progress, interactive exercises, and assessments."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.repo = CurriculumRepository(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)
        self.learner_repo = LearnerRepository(self.db)

    def seed_default_curriculum(self) -> int:
        """Seeds full 54-lesson curriculum from ContentManager or fallback starter lessons."""
        count = 0
        try:
            from .content_manager import ContentManager
            lessons = ContentManager.load_curriculum_lessons()
        except Exception:
            lessons = STARTER_LESSONS

        for lesson in lessons:
            self.repo.upsert_lesson(
                lesson_id=lesson["id"],
                cefr_level=lesson["cefr_level"],
                module_type=lesson["module_type"],
                title=lesson["title"],
                order_index=lesson.get("order_index", 1),
                objectives=lesson.get("objectives", []),
                explanation_markdown=lesson.get("explanation_markdown", ""),
                examples=lesson.get("examples", []),
                guided_exercises=lesson.get("guided_exercises", []),
                interactive_practice=lesson.get("interactive_practice", []),
                assessment=lesson.get("assessment", [])
            )
            count += 1
        return count

    def check_prerequisites(self, learner_id: str, lesson_id: str) -> Dict[str, Any]:
        """
        Verifies whether the learner has completed or mastered all prerequisite lessons.
        Returns: {'unlocked': bool, 'missing_prerequisites': List[Dict]}
        """
        try:
            from .content_manager import ContentManager
            lesson_meta = ContentManager.get_lesson_by_id(lesson_id)
        except Exception:
            lesson_meta = None

        prereqs = lesson_meta.get("prerequisites", []) if lesson_meta else []
        if not prereqs:
            return {"unlocked": True, "missing_prerequisites": []}

        missing = []
        for pid in prereqs:
            prog = self.repo.get_progress(learner_id, pid)
            if not prog or prog.get("status") not in ("completed", "mastered"):
                prereq_lesson = self.repo.get_lesson(pid)
                missing.append({
                    "id": pid,
                    "title": prereq_lesson.get("title", pid) if prereq_lesson else pid,
                    "status": prog.get("status", "not_started") if prog else "not_started"
                })

        return {
            "unlocked": len(missing) == 0,
            "missing_prerequisites": missing
        }

    def recommend_review_lessons(self, learner_id: str) -> List[Dict[str, Any]]:
        """
        Part 8: Recommends review lessons based on recurring mistakes recorded in the Mistake Book.
        Does NOT recommend lessons randomly; strictly performance-driven.
        """
        mistakes = self.mistake_repo.get_mistakes_by_learner(learner_id)
        if not mistakes:
            return []

        # Tally mistake recurrence by skill
        skill_counts = {}
        for m in mistakes:
            s = m.get("skill", "grammar").lower()
            skill_counts[s] = skill_counts.get(s, 0) + m.get("recurrence_count", 1)

        if not skill_counts:
            return []

        # Find most error-prone skill
        priority_skill = max(skill_counts.items(), key=lambda x: x[1])[0]

        # Fetch learner's current CEFR level
        learner = self.learner_repo.get_learner(learner_id)
        current_level = learner.get("cefr_level", "B2") if learner else "B2"

        # Find review lessons matching this skill and level
        matching_lessons = self.list_lessons(cefr_level=current_level, module_type=priority_skill, learner_id=learner_id)
        if not matching_lessons:
            # Fallback to level review lesson
            matching_lessons = self.list_lessons(cefr_level=current_level, module_type="review", learner_id=learner_id)

        recommendations = []
        for l in matching_lessons[:3]:
            recommendations.append({
                "lesson_id": l["id"],
                "title": l["title"],
                "cefr_level": l["cefr_level"],
                "module_type": l["module_type"],
                "reason": f"Targeted remediation for {skill_counts[priority_skill]} recurring mistake(s) in {priority_skill}."
            })

        return recommendations

    def list_lessons(
        self,
        cefr_level: Optional[str] = None,
        module_type: Optional[str] = None,
        learner_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Returns lessons with learner completion progress."""
        lessons = self.repo.list_lessons(cefr_level, module_type)
        if not lessons:
            # Seed default curriculum if empty
            self.seed_default_curriculum()
            lessons = self.repo.list_lessons(cefr_level, module_type)

        if not learner_id:
            return lessons

        # Attach progress for the specified learner
        result = []
        for l in lessons:
            prog = self.repo.get_progress(learner_id, l["id"])
            item = dict(l)
            item["status"] = prog["status"] if prog else "not_started"
            item["score"] = prog["score"] if prog else 0.0
            item["attempts"] = prog["attempts"] if prog else 0
            result.append(item)
        return result

    def get_lesson(self, lesson_id: str, learner_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieves full lesson details and learner progress."""
        lesson = self.repo.get_lesson(lesson_id)
        if not lesson:
            self.seed_default_curriculum()
            lesson = self.repo.get_lesson(lesson_id)
        if not lesson:
            return None

        if learner_id:
            prog = self.repo.get_progress(learner_id, lesson_id)
            lesson["learner_progress"] = prog or {
                "status": "not_started",
                "score": 0.0,
                "attempts": 0
            }
        return lesson

    def evaluate_submission(
        self,
        learner_id: str,
        lesson_id: str,
        answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates learner's answers to interactive practice and assessment quiz.
        Returns immediate feedback, records progress in database, and logs mistakes.
        """
        lesson = self.get_lesson(lesson_id, learner_id)
        if not lesson:
            return {"success": False, "error": f"Lesson {lesson_id} not found"}

        questions = lesson.get("assessment", [])
        if not questions:
            # If no assessment, check interactive_practice
            questions = lesson.get("interactive_practice", [])

        if not questions:
            # Mark complete directly
            self.repo.record_progress(learner_id, lesson_id, 100.0, "completed")
            return {
                "success": True,
                "score": 100.0,
                "status": "completed",
                "total_questions": 0,
                "correct_count": 0,
                "feedback": []
            }

        correct_count = 0
        feedback_list = []

        for q in questions:
            qid = q["id"]
            user_ans = answers.get(qid)
            expected_index = q["correct_index"]
            is_correct = False

            if user_ans is not None:
                try:
                    is_correct = (int(user_ans) == expected_index)
                except (ValueError, TypeError):
                    is_correct = False

            if is_correct:
                correct_count += 1
                feedback_list.append({
                    "question_id": qid,
                    "is_correct": True,
                    "user_answer": user_ans,
                    "correct_answer": expected_index,
                    "explanation": q.get("explanation", "Correct!")
                })
            else:
                feedback_list.append({
                    "question_id": qid,
                    "is_correct": False,
                    "user_answer": user_ans,
                    "correct_answer": expected_index,
                    "explanation": q.get("explanation", "Incorrect.")
                })
                # Log to Mistake Book only if an attempt was actually made
                if user_ans is not None:
                    options = q.get("options", [])
                    correct_text = options[expected_index] if expected_index < len(options) else "Correct Option"
                    user_text = options[int(user_ans)] if (str(user_ans).isdigit() and int(user_ans) < len(options)) else str(user_ans)
                    self.mistake_repo.record_mistake(
                        learner_id=learner_id,
                        skill=lesson.get("module_type", "grammar"),
                        category=lesson.get("title", "Curriculum Lesson"),
                        original_text=user_text,
                        corrected_text=correct_text,
                        explanation=q.get("explanation", "")
                    )

        eval_total = max(1, len(questions))
        score_percent = round((correct_count / eval_total) * 100.0, 1)

        # Enhanced multidimensional mastery calculation
        existing_prog = self.repo.get_progress(learner_id, lesson_id)
        attempts = (existing_prog.get("attempts", 0) + 1) if existing_prog else 1

        # Check prerequisite unlocking and mastery
        prereq_check = self.check_prerequisites(learner_id, lesson_id)
        prereqs_ok = prereq_check.get("unlocked", True)

        # Check recent mistakes in this skill
        recent_mistakes = self.mistake_repo.get_mistakes_by_learner(learner_id)
        unresolved_mistakes = [
            m for m in recent_mistakes
            if m.get("skill", "").lower() == lesson.get("module_type", "").lower()
            and m.get("status", "active") != "mastered"
        ]

        # Mastery requires:
        # 1. Score >= 80%
        # 2. Prerequisites verified
        # 3. Repeated demonstrated performance (>= 2 attempts) OR single attempt >= 80% with 0 unresolved mistakes
        if score_percent >= 80.0 and prereqs_ok:
            if attempts >= 2 or len(unresolved_mistakes) == 0:
                status = "mastered"
            else:
                status = "completed"
        elif score_percent >= 60.0:
            status = "completed"
        else:
            status = "needs_review"

        self.repo.record_progress(learner_id, lesson_id, score_percent, status)

        return {
            "success": True,
            "lesson_id": lesson_id,
            "cefr_level": lesson.get("cefr_level"),
            "score": score_percent,
            "status": status,
            "total_questions": len(questions),
            "correct_count": correct_count,
            "attempts": attempts,
            "mastery_evidence": {
                "attempts": attempts,
                "score_threshold_met": score_percent >= 80.0,
                "prerequisites_satisfied": prereqs_ok,
                "retention_verified": status == "mastered",
                "unresolved_mistakes_count": len(unresolved_mistakes)
            },
            "feedback": feedback_list
        }
