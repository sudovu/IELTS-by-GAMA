"""
build_curriculum_content.py
Constructs the full 54-lesson structured CEFR curriculum across all 6 levels (A1 to C2)
and all 9 modules (Grammar, Vocabulary, Reading, Listening, Writing, Speaking,
Pronunciation, Functional English, Review & Assessment).
Saves to content/curriculum/a1.json through c2.json.
"""

import os
import json

CURRICULUM_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "curriculum")
os.makedirs(CURRICULUM_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# A1 — BEGINNER (9 Modules)
# -----------------------------------------------------------------------------
A1_LESSONS = [
    {
        "id": "curric_a1_gram_present_simple",
        "cefr_level": "A1",
        "module_type": "grammar",
        "title": "Present Simple & Subject-Verb Concord",
        "order_index": 1,
        "prerequisites": [],
        "estimated_minutes": 25,
        "objectives": [
            "Understand when to use the Present Simple for habits, routines, and universal truths.",
            "Master third-person singular inflection ('-s' / '-es').",
            "Formulate accurate negative sentences using 'do not' and 'does not'."
        ],
        "form_and_structure": "Subject + Base Verb (I/you/we/they) OR Base Verb + -s/-es (he/she/it). Negative: Subject + do/does not + base verb.",
        "usage_rationale": "Used to describe habitual actions, unchanging facts, routines, and scheduled states.",
        "positive_examples": [
            "I walk to the university campus every morning.",
            "She studies English for forty minutes daily."
        ],
        "negative_examples": [
            "They do not attend evening lectures.",
            "He does not live in central London."
        ],
        "common_mistakes": [
            "Incorrect: 'He don't like coffee.' -> Correct: 'He doesn't like coffee.'",
            "Incorrect: 'She lives in London and study law.' -> Correct: 'She lives in London and studies law.'"
        ],
        "confused_structures": [
            "Present Simple vs Present Continuous: 'I work here' (permanent) vs 'I am working here this week' (temporary)."
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
        "independent_practice": [
            {"id": "a1_ind_1", "prompt": "Write two sentences describing your morning routine using base verbs and third-person singular verbs."}
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
        ],
        "review_questions": [
            "When do we add -es instead of -s to a verb in the third-person singular?",
            "What is the auxiliary verb used for forming negative sentences with 'they'?"
        ]
    },
    {
        "id": "curric_a1_vocab_everyday_essentials",
        "cefr_level": "A1",
        "module_type": "vocabulary",
        "title": "Everyday Essentials: Numbers, Family & Time",
        "order_index": 2,
        "prerequisites": [],
        "estimated_minutes": 20,
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
                "question": "Complete the sentence: 'We usually travel on vacation _____ July.'",
                "options": ["at", "on", "in", "by"],
                "correct_index": 2,
                "explanation": "Months without specific dates take 'in'."
            }
        ]
    },
    {
        "id": "curric_a1_read_short_notices",
        "cefr_level": "A1",
        "module_type": "reading",
        "title": "Reading Practical Signs, Menus & Public Notices",
        "order_index": 3,
        "prerequisites": ["curric_a1_vocab_everyday_essentials"],
        "estimated_minutes": 25,
        "objectives": [
            "Extract specific key information from short everyday announcements and signs.",
            "Recognize common warning and instruction words (Exit, Push, Do Not Enter, Cash Only).",
            "Locate opening hours and prices in directory listings."
        ],
        "explanation_markdown": """### Reading Practical Short Texts
At A1, reading focuses on practical survival information:
1. **Instruction Signs**: *Push / Pull*, *No Parking*, *Emergency Exit*.
2. **Opening Hours**: *Mon–Fri: 09:00–18:00*, *Closed on Public Holidays*.
3. **Prices and Quantities**: *£3.50 per person*, *Special student discount available*.""",
        "examples": [
            {"text": "NOTICE: Library will close at 5:00 PM today for maintenance.", "notes": "Information specifies time (5:00 PM) and reason (maintenance)."}
        ],
        "guided_exercises": [
            {"id": "a1_r_ge_1", "prompt": "If a shop sign states 'Open: 9 AM - 6 PM Daily', can you enter at 7 PM? (Yes/No)", "answer": "No", "explanation": "The shop closes at 6 PM."}
        ],
        "interactive_practice": [
            {
                "id": "a1_r_ip_1",
                "question": "What does a sign saying 'Staff Only' mean?",
                "options": [
                    "Anyone may enter freely.",
                    "Only employees who work there may enter.",
                    "Children must be accompanied by an adult.",
                    "The room is open during staff hours only."
                ],
                "correct_index": 1,
                "explanation": "'Staff Only' restricts access solely to employees."
            }
        ],
        "assessment": [
            {
                "id": "a1_r_as_1",
                "question": "A clinic sign reads: 'Appointments required. No walk-ins.' What should a patient do?",
                "options": [
                    "Wait in the waiting room without booking.",
                    "Call or book online in advance before visiting.",
                    "Enter only on weekends.",
                    "Pay double if arriving early."
                ],
                "correct_index": 1,
                "explanation": "'No walk-ins' means patients cannot be seen without prior scheduled booking."
            }
        ]
    },
    {
        "id": "curric_a1_list_basic_instructions",
        "cefr_level": "A1",
        "module_type": "listening",
        "title": "Listening to Daily Instructions & Numbers",
        "order_index": 4,
        "prerequisites": ["curric_a1_vocab_everyday_essentials"],
        "estimated_minutes": 20,
        "objectives": [
            "Identify spoken numbers, telephone numbers, and street names in slow speech.",
            "Recognize basic classroom and service instructions ('Please sit down', 'Sign here').",
            "Distinguish between similar-sounding digits (e.g. 15 vs 50)."
        ],
        "explanation_markdown": """### Listening for Factual Details
Listening at A1 requires focused attention on:
1. **Numbers**: Listen for syllable stress (fif-TEEN vs FIF-ty).
2. **Spelling Names**: Recognizing letters when speakers spell aloud (*S-M-I-T-H*).
3. **Common Directions**: *Turn left*, *Go upstairs*, *Room 12*.""",
        "examples": [
            {"text": "RECEPTIONIST: 'Your room is on the second floor, number 214.'", "notes": "Key details: second floor, room 214."}
        ],
        "guided_exercises": [
            {"id": "a1_l_ge_1", "prompt": "If a speaker says: 'Call me on zero-seven-two-four', what are the digits?", "answer": "0724", "explanation": "'Zero-seven-two-four' corresponds to 0724."}
        ],
        "interactive_practice": [
            {
                "id": "a1_l_ip_1",
                "question": "In English, which syllable is stressed in 'thirteen'?",
                "options": ["First syllable (THIR-teen)", "Second syllable (thir-TEEN)", "Equal stress", "Neither"],
                "correct_index": 1,
                "explanation": "Teen numbers (13–19) have primary stress on the final syllable '-teen' in isolation."
            }
        ],
        "assessment": [
            {
                "id": "a1_l_as_1",
                "question": "The clerk says: 'The bus leaves at ten to four.' What time is the departure?",
                "options": ["4:10", "3:50", "10:04", "4:50"],
                "correct_index": 1,
                "explanation": "'Ten to four' means 10 minutes before 4:00, which is 3:50."
            }
        ]
    },
    {
        "id": "curric_a1_write_sentence_mechanics",
        "cefr_level": "A1",
        "module_type": "writing",
        "title": "Sentence Mechanics: Capitalization & Simple Sentences",
        "order_index": 5,
        "prerequisites": ["curric_a1_gram_present_simple"],
        "estimated_minutes": 25,
        "objectives": [
            "Apply mandatory capitalization rules (start of sentences, 'I', days, months, proper names).",
            "Construct simple S-V-O (Subject-Verb-Object) sentences with correct end punctuation.",
            "Write basic biographical descriptions (name, age, country, occupation)."
        ],
        "explanation_markdown": """### Writing Clear Basic Sentences
Every complete English sentence requires:
1. A **Subject** (who or what is performing the action).
2. A **Finite Verb** (the action or state).
3. Proper **Punctuation**: Capital letter at the start, full stop (.) or question mark (?) at the end.

#### Capital Letter Checklist:
- The personal pronoun **I** is ALWAYS capitalized.
- Names of people, cities, and countries (*Anna, Tokyo, Spain*).
- Days of the week and months (*Friday, August*).""",
        "examples": [
            {"text": "Maria lives in Madrid and she speaks Spanish.", "notes": "Proper nouns (Maria, Madrid, Spanish) capitalized."}
        ],
        "guided_exercises": [
            {"id": "a1_w_ge_1", "prompt": "Correct the capitalization: 'my friend lives in london with his brother.'", "answer": "My friend lives in London with his brother.", "explanation": "'My' starts the sentence and 'London' is a proper noun city."}
        ],
        "interactive_practice": [
            {
                "id": "a1_w_ip_1",
                "question": "Which sentence has correct punctuation and capitalization?",
                "options": [
                    "i go to school on mondays.",
                    "I go to school on Mondays.",
                    "I go to school on mondays",
                    "i Go to school on Mondays."
                ],
                "correct_index": 1,
                "explanation": "Capital 'I', capital 'Mondays', and ending period '.'."
            }
        ],
        "assessment": [
            {
                "id": "a1_w_as_1",
                "question": "Identify the grammatically complete simple sentence:",
                "options": [
                    "In the university library every afternoon.",
                    "Studies English diligently every day.",
                    "Elena studies English in the library.",
                    "Because Elena studies English every day."
                ],
                "correct_index": 2,
                "explanation": "'Elena studies English in the library' contains subject, verb, object, and place."
            }
        ]
    },
    {
        "id": "curric_a1_speak_introductions",
        "cefr_level": "A1",
        "module_type": "speaking",
        "title": "Self-Introductions & Personal Information",
        "order_index": 6,
        "prerequisites": [],
        "estimated_minutes": 20,
        "objectives": [
            "Introduce oneself clearly stating name, origin, occupation, and studies.",
            "Ask and answer simple personal identity questions comfortably.",
            "Pronounce basic contraction forms ('I'm', 'He's', 'They're') naturally."
        ],
        "explanation_markdown": """### Structuring a Self-Introduction
A fluent self-introduction follows a clear three-step pattern:
1. **Name & Greeting**: *Hello, my name is David / I'm David.*
2. **Origin**: *I come from Valencia, Spain / I am from Valencia.*
3. **Current Occupation or Studies**: *Currently, I am a university student majoring in economics.*""",
        "examples": [
            {"text": "Good morning. My name is Carlos, and I am from Bogota, Colombia.", "notes": "Clear, professional opening."}
        ],
        "guided_exercises": [
            {"id": "a1_s_ge_1", "prompt": "Form the question for the answer: 'I am 22 years old.'", "answer": "How old are you?", "explanation": "Asking age uses 'How old are you?'."}
        ],
        "interactive_practice": [
            {
                "id": "a1_s_ip_1",
                "question": "Which is the most natural reply to 'Where do you come from?'",
                "options": [
                    "I am coming yesterday.",
                    "I come from Osaka, Japan.",
                    "I am live here.",
                    "My country is Osaka."
                ],
                "correct_index": 1,
                "explanation": "'I come from [Place]' is the standard natural response."
            }
        ],
        "assessment": [
            {
                "id": "a1_s_as_1",
                "question": "What is the polite response when meeting someone for the first time?",
                "options": [
                    "See you tomorrow.",
                    "Pleased to meet you.",
                    "How are you doing yesterday?",
                    "Excuse me for everything."
                ],
                "correct_index": 1,
                "explanation": "'Pleased to meet you' or 'Nice to meet you' is standard etiquette."
            }
        ]
    },
    {
        "id": "curric_a1_pron_alphabet_phonemes",
        "cefr_level": "A1",
        "module_type": "pronunciation",
        "title": "English Alphabet Sounds & Short Vowels",
        "order_index": 7,
        "prerequisites": [],
        "estimated_minutes": 20,
        "objectives": [
            "Master the pronunciation of the 26 English letters and their core phonemic values.",
            "Distinguish between short vowel phonemes: /æ/ (cat), /e/ (bed), /ɪ/ (sit), /ɒ/ (hot), /ʌ/ (cup).",
            "Avoid adding trailing vowel sounds to word-final consonants."
        ],
        "explanation_markdown": """### Short Vowels in English
English vowels can be short or long. Mastering short vowels prevents miscommunication:
- **/æ/**: *cat, bat, map* (open jaw, spread lips)
- **/e/**: *bed, pen, red* (relaxed mid vowel)
- **/ɪ/**: *sit, pin, hit* (short, high, lax vowel)
- **/ɒ/**: *hot, stop, clock* (rounded, back vowel)
- **/ʌ/**: *cup, sun, bus* (central, short neutral sound)""",
        "examples": [
            {"text": "bat (/bæt/) vs bet (/bet/) vs bit (/bɪt/)", "notes": "Notice how mouth opening changes."}
        ],
        "guided_exercises": [
            {"id": "a1_p_ge_1", "prompt": "Which vowel phoneme is in 'cup': /æ/ or /ʌ/?", "answer": "/ʌ/", "explanation": "'cup' has the short central vowel /ʌ/."}
        ],
        "interactive_practice": [
            {
                "id": "a1_p_ip_1",
                "question": "Which word contains the /æ/ short vowel sound?",
                "options": ["hate", "hat", "heat", "hot"],
                "correct_index": 1,
                "explanation": "'hat' has the /æ/ sound; 'hate' has diphthong /eɪ/."
            }
        ],
        "assessment": [
            {
                "id": "a1_p_as_1",
                "question": "Identify the pair of words that rhyme:",
                "options": ["pen / pin", "cat / hat", "hot / hut", "bed / bad"],
                "correct_index": 1,
                "explanation": "'cat' and 'hat' share the identical rime /æt/."
            }
        ]
    },
    {
        "id": "curric_a1_func_social_transactions",
        "cefr_level": "A1",
        "module_type": "functional",
        "title": "Functional English: Ordering, Requesting & Shopping",
        "order_index": 8,
        "prerequisites": ["curric_a1_vocab_everyday_essentials"],
        "estimated_minutes": 25,
        "objectives": [
            "Use polite formulaic requests ('Can I have...', 'Could you please...').",
            "Order food and beverages in a cafe or canteen confidently.",
            "Inquire about prices ('How much is this?') and understand payment totals."
        ],
        "explanation_markdown": """### Polite Requests in Everyday Situations
In English-speaking environments, direct commands are softened with politeness markers:
- Instead of *'Give me water'*, say: **'Could I please have a glass of water?'**
- In a cafe: **'I would like a medium coffee, please.'** / **'Can I get a cappuccino to go?'**
- Asking cost: **'How much does this cost?'** / **'How much is that in total?'**""",
        "examples": [
            {"text": "CUSTOMER: 'Could I have the bill, please?' WAITER: 'Certainly, right away.'", "notes": "Polite formulaic exchange."}
        ],
        "guided_exercises": [
            {"id": "a1_func_ge_1", "prompt": "Fill in the polite modal: '_____ I have a receipt, please?' (Can / Am)", "answer": "Can", "explanation": "'Can I have...' is a standard polite request."}
        ],
        "interactive_practice": [
            {
                "id": "a1_func_ip_1",
                "question": "What is the most polite way to ask for a coffee?",
                "options": [
                    "Give me one coffee now.",
                    "I want coffee.",
                    "Could I please have a black coffee?",
                    "Coffee is needed by me."
                ],
                "correct_index": 2,
                "explanation": "'Could I please have...' expresses the polite standard in service interactions."
            }
        ],
        "assessment": [
            {
                "id": "a1_func_as_1",
                "question": "If an item costs $4.75 and you hand the cashier a $5 note, your change is:",
                "options": ["$0.15", "$0.25", "$0.35", "$1.25"],
                "correct_index": 1,
                "explanation": "$5.00 - $4.75 = $0.25 (twenty-five cents)."
            }
        ]
    },
    {
        "id": "curric_a1_rev_mastery_checkpoint",
        "cefr_level": "A1",
        "module_type": "review",
        "title": "A1 Level Review & Comprehensive Mastery Assessment",
        "order_index": 9,
        "prerequisites": ["curric_a1_gram_present_simple", "curric_a1_write_sentence_mechanics"],
        "estimated_minutes": 30,
        "objectives": [
            "Synthesize A1 grammar, vocabulary, reading, and functional communication.",
            "Demonstrate mastery of present simple subject concord and sentence mechanics.",
            "Confirm readiness for CEFR A2 Elementary curriculum."
        ],
        "explanation_markdown": """### A1 Milestone Review
Congratulations on completing the A1 foundational curriculum.
Review your core competencies:
1. **Grammar**: Present simple affirmative, negative, and interrogative structures.
2. **Vocabulary**: Numbers, time prepositions (at/on/in), family, and everyday objects.
3. **Reading & Listening**: Grasping factual times, notices, and instructions.
4. **Writing**: Proper capitalization, periods, and complete simple sentences.""",
        "examples": [
            {"text": "Summary checklist: I can introduce myself, ask for prices, read notices, and write basic sentences.", "notes": "A1 CEFR descriptor achieved."}
        ],
        "guided_exercises": [
            {"id": "a1_rev_ge_1", "prompt": "Identify the error: 'On 8 o'clock, he arrive at work.'", "answer": "At 8 o'clock, he arrives at work.", "explanation": "Time requires 'At' and third-person singular requires 'arrives'."}
        ],
        "interactive_practice": [
            {
                "id": "a1_rev_ip_1",
                "question": "Which sentence is completely error-free?",
                "options": [
                    "She don't live in Madrid on sundays.",
                    "She doesn't live in Madrid on Sundays.",
                    "She does not lives in Madrid on sundays.",
                    "She not lives in madrid on Sundays."
                ],
                "correct_index": 1,
                "explanation": "'doesn't live' has correct concord, and 'Madrid' and 'Sundays' are capitalized."
            }
        ],
        "assessment": [
            {
                "id": "a1_rev_as_1",
                "question": "Select the correct sentence to complete the conversation: 'What time does the train leave?'",
                "options": [
                    "It leave at 3:15 PM.",
                    "It leaves at 3:15 PM.",
                    "It is leave in 3:15 PM.",
                    "It leaves on 3:15 PM."
                ],
                "correct_index": 1,
                "explanation": "'It' requires 'leaves', and clock time takes 'at'."
            },
            {
                "id": "a1_rev_as_2",
                "question": "What is the plural of 'child'?",
                "options": ["childs", "children", "childrens", "childes"],
                "correct_index": 1,
                "explanation": "'child' has the irregular plural 'children'."
            }
        ]
    }
]

with open(os.path.join(CURRICULUM_DIR, "a1.json"), "w", encoding="utf-8") as f:
    json.dump(A1_LESSONS, f, indent=2, ensure_ascii=False)
print("Generated a1.json with", len(A1_LESSONS), "lessons.")
