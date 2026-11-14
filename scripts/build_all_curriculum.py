"""
build_all_curriculum.py
Generates the complete 54-lesson structured CEFR curriculum (9 modules per level for A1-C2).
Preserves and integrates the 18 existing starter lesson IDs.
"""

import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRICULUM_DIR = os.path.join(BASE_DIR, "content", "curriculum")
os.makedirs(CURRICULUM_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# A2 — ELEMENTARY (9 Modules)
# -----------------------------------------------------------------------------
A2_LESSONS = [
    {
        "id": "curric_a2_gram_past_simple",
        "cefr_level": "A2",
        "module_type": "grammar",
        "title": "Past Simple & Regular/Irregular Verbs",
        "order_index": 1,
        "prerequisites": ["curric_a1_gram_present_simple"],
        "estimated_minutes": 25,
        "objectives": [
            "Distinguish between regular '-ed' inflections and high-frequency irregular past verbs.",
            "Formulate negative statements and questions using 'did not' and 'did'.",
            "Express completed past historical and biographical events accurately."
        ],
        "form_and_structure": "Regular: Base + -ed (worked, studied). Irregular: V2 form (went, bought, saw). Negative: did not + base verb.",
        "usage_rationale": "Used for actions completed at a specific time in the past.",
        "positive_examples": [
            "She visited the British Museum last Saturday.",
            "They bought their train tickets yesterday morning."
        ],
        "negative_examples": [
            "He did not attend the tutorial yesterday.",
            "We did not see the announcement."
        ],
        "common_mistakes": [
            "Incorrect: 'She didn't went to class.' -> Correct: 'She didn't go to class.' (Auxiliary 'did' already carries past tense).",
            "Incorrect: 'I buyed a new dictionary.' -> Correct: 'I bought a new dictionary.'"
        ],
        "confused_structures": [
            "Past Simple vs Present Perfect: 'I lost my keys yesterday' (finished time) vs 'I have lost my keys' (result now)."
        ],
        "explanation_markdown": """### Past Simple Mechanics
The Past Simple expresses completed events at a definite time in the past (*yesterday, last year, in 2020*).

#### Regular vs Irregular:
- **Regular**: Add *-ed* (*work -> worked, call -> called*).
- **Irregular**: Unique forms must be memorized (*go -> went, take -> took, write -> wrote*).
- **Negatives & Questions**: Auxiliary **did / did not** + base form.""",
        "examples": [
            {"text": "The committee submitted the report yesterday afternoon.", "notes": "Regular past verb with specific time marker."},
            {"text": "Dr. Watson wrote three groundbreaking papers in 2015.", "notes": "Irregular verb 'write' -> 'wrote'."}
        ],
        "guided_exercises": [
            {"id": "a2_ge_1", "prompt": "Yesterday, they _____ (go) to the laboratory early.", "answer": "went", "explanation": "'go' has the irregular past form 'went'."}
        ],
        "interactive_practice": [
            {
                "id": "a2_ip_1",
                "question": "Which sentence correctly forms the negative past simple?",
                "options": [
                    "She didn't arrived on time.",
                    "She didn't arrive on time.",
                    "She wasn't arrive on time.",
                    "She no arrived on time."
                ],
                "correct_index": 1,
                "explanation": "'did not (didn't)' is followed by the base verb 'arrive'."
            }
        ],
        "assessment": [
            {
                "id": "a2_as_1",
                "question": "Select the correct past form: 'He _____ (catch) the express bus.'",
                "options": ["catched", "caught", "cought", "was catch"],
                "correct_index": 1,
                "explanation": "The past simple of 'catch' is irregular: 'caught'."
            }
        ]
    },
    {
        "id": "curric_a2_vocab_travel_transport",
        "cefr_level": "A2",
        "module_type": "vocabulary",
        "title": "Travel, Commuting & Urban Geography",
        "order_index": 2,
        "prerequisites": ["curric_a1_vocab_everyday_essentials"],
        "estimated_minutes": 20,
        "objectives": [
            "Acquire essential terminology for public transportation, routes, and tickets.",
            "Describe commuting routines and directional navigation.",
            "Distinguish between 'trip', 'journey', 'travel', and 'voyage'."
        ],
        "explanation_markdown": """### Travel & Commuter Terminology
- **Commute**: Daily journey between home and work.
- **Fare**: Money paid for a journey on public transit.
- **Platform**: Raised area beside railroad tracks where passengers board.""",
        "examples": [
            {"text": "The daily commute takes forty-five minutes by underground train.", "notes": "Commute refers to the daily routine travel."}
        ],
        "guided_exercises": [
            {"id": "a2_v_ge_1", "prompt": "You wait for the train at _____ number 4. (platform / station)", "answer": "platform", "explanation": "Passengers board at a specific platform."}
        ],
        "interactive_practice": [
            {
                "id": "a2_v_ip_1",
                "question": "Which word is uncountable in standard English?",
                "options": ["trip", "journey", "travel", "flight"],
                "correct_index": 2,
                "explanation": "'travel' is an uncountable noun; 'trip' and 'journey' are countable."
            }
        ],
        "assessment": [
            {
                "id": "a2_v_as_1",
                "question": "A ticket that permits travel to a destination and back is called a:",
                "options": ["single ticket", "return ticket", "platform ticket", "one-way pass"],
                "correct_index": 1,
                "explanation": "A return ticket covers travel to a place and back."
            }
        ]
    },
    {
        "id": "curric_a2_read_scanning_notices",
        "cefr_level": "A2",
        "module_type": "reading",
        "title": "Scanning Notices & Informational Announcements",
        "order_index": 3,
        "prerequisites": ["curric_a1_read_short_notices"],
        "estimated_minutes": 25,
        "objectives": [
            "Employ targeted scanning techniques to locate specific dates, requirements, and regulations.",
            "Identify conditional clauses in public announcements ('If lost, please return...').",
            "Synthesize details from multi-section notices without reading every word."
        ],
        "explanation_markdown": """### The Mechanics of Scanning
Scanning is rapid reading to locate specific keywords, numbers, or terms without reading the entire passage word-for-word.
1. Decide on your keyword (e.g. *fee, Friday, room 4*).
2. Move eyes systematically across headings and bullet points.""",
        "examples": [
            {"text": "CAMPUS NOTICE: Submissions after 5 PM incur a 10% penalty.", "notes": "Scanning quickly finds '5 PM' and '10% penalty'."}
        ],
        "guided_exercises": [
            {"id": "a2_r_ge_1", "prompt": "Scan for the penalty: 'Late returns cost £2 per day.' Penalty amount = £_____", "answer": "2", "explanation": "Targeted scanning identifies £2."}
        ],
        "interactive_practice": [
            {
                "id": "a2_r_ip_1",
                "question": "When scanning a public notice, what should you look at first?",
                "options": [
                    "The final sentence only",
                    "Headings, bold text, and bullet points",
                    "Every preposition in the text",
                    "The word count of each paragraph"
                ],
                "correct_index": 1,
                "explanation": "Headings and bold text provide quick visual orientation."
            }
        ],
        "assessment": [
            {
                "id": "a2_r_as_1",
                "question": "Notice: 'Passes valid on local buses only. Excludes express airport coaches.' Can you use this pass to the airport on an express coach?",
                "options": [
                    "Yes, at all times.",
                    "No, express coaches are excluded.",
                    "Yes, but only on weekends.",
                    "Only with written permission."
                ],
                "correct_index": 1,
                "explanation": "'Excludes' means express coaches are not covered."
            }
        ]
    },
    {
        "id": "curric_a2_list_conversations",
        "cefr_level": "A2",
        "module_type": "listening",
        "title": "Listening to Transactional Dialogues & Schedules",
        "order_index": 4,
        "prerequisites": ["curric_a1_list_basic_instructions"],
        "estimated_minutes": 25,
        "objectives": [
            "Follow transactional conversations in banks, hotels, and transit offices.",
            "Identify corrections and self-repairs in spoken speech ('Actually, make that two').",
            "Record dates, times, and prices accurately."
        ],
        "explanation_markdown": """### Recognizing Spoken Corrections & Distractors
Speakers often correct themselves in real time:
- *'I would like a single room for Thursday... oh wait, Friday night, please.'*
The true answer is **Friday night**; Thursday was a distractor.""",
        "examples": [
            {"text": "SPEAKER: 'The class was scheduled for room 102, but we moved to 204.'", "notes": "Room 102 is the distractor; 204 is the final room."}
        ],
        "guided_exercises": [
            {"id": "a2_l_ge_1", "prompt": "Customer: 'Give me three tickets... actually, make it four.' Final quantity: _____", "answer": "4", "explanation": "'Make it four' updates the requested quantity to 4."}
        ],
        "interactive_practice": [
            {
                "id": "a2_l_ip_1",
                "question": "What word signals that the speaker is correcting what they just said?",
                "options": ["Always", "Actually", "Already", "Almost"],
                "correct_index": 1,
                "explanation": "'Actually' is commonly used to introduce an immediate self-correction."
            }
        ],
        "assessment": [
            {
                "id": "a2_l_as_1",
                "question": "AGENT: 'The flight arrives at 7:15... apologies, the screen shows a delay to 8:30.' Arrival time is:",
                "options": ["7:15", "8:30", "7:45", "8:15"],
                "correct_index": 1,
                "explanation": "The self-correction and screen update confirm 8:30."
            }
        ]
    },
    {
        "id": "curric_a2_write_informal_emails",
        "cefr_level": "A2",
        "module_type": "writing",
        "title": "Writing Short Informal Emails & Messages",
        "order_index": 5,
        "prerequisites": ["curric_a1_write_sentence_mechanics"],
        "estimated_minutes": 25,
        "objectives": [
            "Structure a clear short email with greeting, message body, and sign-off.",
            "Use basic coordinating conjunctions ('and', 'but', 'so', 'because') to combine clauses.",
            "Express invitations, acceptance, and polite apologies."
        ],
        "explanation_markdown": """### Structure of an Informal Email
1. **Greeting**: *Hi Sarah,* / *Dear Mark,*
2. **Opening**: *Thanks for your email. I am writing to ask...*
3. **Core Message**: Clear details combined with *and, but, so, because*.
4. **Closing**: *Hope to see you soon! / Best wishes,*""",
        "examples": [
            {"text": "Hi Alex, I cannot meet you today because I have an exam, but let's meet on Friday.", "notes": "Uses 'because' and 'but' smoothly."}
        ],
        "guided_exercises": [
            {"id": "a2_w_ge_1", "prompt": "Join the sentences with 'so': 'It was raining heavily. We stayed inside.'", "answer": "It was raining heavily so we stayed inside.", "explanation": "'so' shows result."}
        ],
        "interactive_practice": [
            {
                "id": "a2_w_ip_1",
                "question": "Which connector shows contrast between two ideas?",
                "options": ["and", "because", "but", "so"],
                "correct_index": 2,
                "explanation": "'but' introduces a contrast."
            }
        ],
        "assessment": [
            {
                "id": "a2_w_as_1",
                "question": "Which is an appropriate informal sign-off to a friend?",
                "options": [
                    "Yours faithfully,",
                    "I remain your obedient servant,",
                    "Best wishes,",
                    "To whom it may concern,"
                ],
                "correct_index": 2,
                "explanation": "'Best wishes,' is friendly and informal."
            }
        ]
    },
    {
        "id": "curric_a2_speak_narrating_events",
        "cefr_level": "A2",
        "module_type": "speaking",
        "title": "Narrating Past Experiences & Describing Habits",
        "order_index": 6,
        "prerequisites": ["curric_a1_speak_introductions", "curric_a2_gram_past_simple"],
        "estimated_minutes": 25,
        "objectives": [
            "Describe a memorable trip or past event in chronological order.",
            "Use temporal sequence markers ('first', 'then', 'after that', 'finally').",
            "Answer Part 1 style personal history questions with appropriate elaboration."
        ],
        "explanation_markdown": """### Chronological Sequencing in Speech
Keep your listener engaged by organizing past events clearly:
- **First**: *First, we took a taxi to the terminal.*
- **Then / After that**: *After that, we boarded the plane.*
- **Finally**: *Finally, we arrived at our hotel around midnight.*""",
        "examples": [
            {"text": "Last summer, I visited Scotland. First, I stayed in Edinburgh, and then I traveled to the Highlands.", "notes": "Organized past narration."}
        ],
        "guided_exercises": [
            {"id": "a2_s_ge_1", "prompt": "Sequence marker to conclude a story: '_____, we returned home safely.'", "answer": "Finally", "explanation": "'Finally' or 'In the end' concludes a series of events."}
        ],
        "interactive_practice": [
            {
                "id": "a2_s_ip_1",
                "question": "In IELTS Speaking Part 1, if the examiner asks 'Did you enjoy your last vacation?', the best response is:",
                "options": [
                    "Yes.",
                    "Yes, I did. I went to the coast with my family and the weather was excellent.",
                    "No vacation.",
                    "Vacations are generally taken by individuals annually."
                ],
                "correct_index": 1,
                "explanation": "Always elaborate with 2-3 sentences providing details."
            }
        ],
        "assessment": [
            {
                "id": "a2_s_as_1",
                "question": "What is the past tense form of 'fly' in speech?",
                "options": ["flied", "flew", "flown", "flying"],
                "correct_index": 1,
                "explanation": "Past simple of fly is 'flew'."
            }
        ]
    },
    {
        "id": "curric_a2_pron_past_ed_endings",
        "cefr_level": "A2",
        "module_type": "pronunciation",
        "title": "Pronunciation of Regular Past '-ed' Endings",
        "order_index": 7,
        "prerequisites": ["curric_a2_gram_past_simple"],
        "estimated_minutes": 20,
        "objectives": [
            "Master the three phonetic pronunciations of '-ed': /t/, /d/, and /ɪd/.",
            "Pronounce /ɪd/ only after root verbs ending in /t/ or /d/ sounds.",
            "Produce voiceless /t/ after voiceless consonants (/p, k, s, ʃ, tʃ/).",
            "Produce voiced /d/ after vowels and voiced consonants."
        ],
        "explanation_markdown": """### The Three '-ed' Pronunciations
1. **/ɪd/** (adds an extra syllable): ONLY after **t** or **d** (*waited, needed, decided*).
2. **/t/** (no extra syllable): after voiceless sounds /p, k, f, s, ʃ, tʃ/ (*walked -> /wɔːkt/, stopped -> /stɒpt/*).
3. **/d/** (no extra syllable): after voiced sounds and vowels (*played -> /pleɪd/, lived -> /lɪvd/*).""",
        "examples": [
            {"text": "started (/ɪd/) vs cooked (/t/) vs opened (/d/)", "notes": "Notice only 'started' adds an extra syllable."}
        ],
        "guided_exercises": [
            {"id": "a2_p_ge_1", "prompt": "Does 'wanted' have 1 or 2 syllables in pronunciation?", "answer": "2", "explanation": "'wan-ted' adds the /ɪd/ syllable because root ends in /t/."}
        ],
        "interactive_practice": [
            {
                "id": "a2_p_ip_1",
                "question": "In which word is '-ed' pronounced as an extra syllable /ɪd/?",
                "options": ["worked", "visited", "cleaned", "watched"],
                "correct_index": 1,
                "explanation": "'visited' ends in /t/, so '-ed' is pronounced /ɪd/."
            }
        ],
        "assessment": [
            {
                "id": "a2_p_as_1",
                "question": "How is '-ed' pronounced in the word 'laughed' (/lɑːft/)?",
                "options": ["/ɪd/", "/d/", "/t/", "/ed/"],
                "correct_index": 2,
                "explanation": "'laugh' ends in voiceless /f/, so '-ed' is pronounced /t/."
            }
        ]
    },
    {
        "id": "curric_a2_func_asking_directions",
        "cefr_level": "A2",
        "module_type": "functional",
        "title": "Functional English: Asking for & Giving Directions",
        "order_index": 8,
        "prerequisites": ["curric_a2_vocab_travel_transport"],
        "estimated_minutes": 25,
        "objectives": [
            "Ask for locations politely ('Excuse me, could you tell me where the station is?').",
            "Understand spatial prepositions ('opposite', 'next to', 'between', 'around the corner').",
            "Follow directional guidance ('Go straight on', 'Take the second turn on your right')."
        ],
        "explanation_markdown": """### Direction Formulas
- **Polite Inquiries**:
  - *'Excuse me, how do I get to the central library?'*
  - *'Could you tell me where the nearest pharmacy is?'*
- **Giving Directions**:
  - *Go straight ahead for two blocks.*
  - *Turn left at the traffic lights.*
  - *It's on your right, opposite the post office.*""",
        "examples": [
            {"text": "PEDESTRIAN: 'Excuse me, where is the subway?' GUIDE: 'Turn right at the bank; it's next to the cafe.'", "notes": "Functional spatial exchange."}
        ],
        "guided_exercises": [
            {"id": "a2_func_ge_1", "prompt": "If building A is across the street from building B, building A is _____ building B. (opposite / inside)", "answer": "opposite", "explanation": "'opposite' means across from."}
        ],
        "interactive_practice": [
            {
                "id": "a2_func_ip_1",
                "question": "What does 'take the second turning on the left' mean?",
                "options": [
                    "Turn left immediately.",
                    "Pass the first left road, and turn at the second left road.",
                    "Turn right twice.",
                    "Turn left and then stop for two minutes."
                ],
                "correct_index": 1,
                "explanation": "It directs you to bypass the first intersection and turn on the second."
            }
        ],
        "assessment": [
            {
                "id": "a2_func_as_1",
                "question": "Complete the request: 'Excuse me, is there a post office _____ here?'",
                "options": ["near", "nearly", "alongside", "closely"],
                "correct_index": 0,
                "explanation": "'near here' is the idiomatic phrase asking for nearby proximity."
            }
        ]
    },
    {
        "id": "curric_a2_rev_elementary_mastery",
        "cefr_level": "A2",
        "module_type": "review",
        "title": "A2 Level Review & Comprehensive Assessment",
        "order_index": 9,
        "prerequisites": ["curric_a2_gram_past_simple", "curric_a2_write_informal_emails"],
        "estimated_minutes": 30,
        "objectives": [
            "Consolidate A2 past tense inflections, regular and irregular verbs.",
            "Verify reading comprehension and scanning efficiency on announcements.",
            "Confirm readiness for CEFR B1 Intermediate curriculum."
        ],
        "explanation_markdown": """### A2 Milestone Review
Key competencies consolidated at A2:
- **Grammar**: Past Simple regular and irregular verbs, negative questions with 'did'.
- **Vocabulary**: Commuting, directions, urban transport, connectors (*so, because, but*).
- **Phonetics**: Three '-ed' endings (/t/, /d/, /ɪd/).
- **Writing & Speaking**: Informal emails and past event narrations.""",
        "examples": [
            {"text": "A2 Mastery Check: Ability to communicate routine tasks requiring simple and direct exchange of information.", "notes": "Official CEFR A2 descriptor."}
        ],
        "guided_exercises": [
            {"id": "a2_rev_ge_1", "prompt": "Identify the past tense of 'leave': _____", "answer": "left", "explanation": "'leave' -> 'left'."}
        ],
        "interactive_practice": [
            {
                "id": "a2_rev_ip_1",
                "question": "Choose the correctly formed question:",
                "options": [
                    "Where did you went yesterday?",
                    "Where did you go yesterday?",
                    "Where you went yesterday?",
                    "Where was you go yesterday?"
                ],
                "correct_index": 1,
                "explanation": "'did' + subject 'you' + base verb 'go'."
            }
        ],
        "assessment": [
            {
                "id": "a2_rev_as_1",
                "question": "Which sentence is punctuated and inflected accurately?",
                "options": [
                    "We visited Edinburgh last year, and we took many photographs.",
                    "We visit Edinburgh last year, and we taked many photographs.",
                    "We visited edinburgh last year and tooked photographs.",
                    "We were visit Edinburgh last year and take photographs."
                ],
                "correct_index": 0,
                "explanation": "'visited' and 'took' are correct past forms; 'Edinburgh' is capitalized."
            }
        ]
    }
]

with open(os.path.join(CURRICULUM_DIR, "a2.json"), "w", encoding="utf-8") as f:
    json.dump(A2_LESSONS, f, indent=2, ensure_ascii=False)
print("Generated a2.json with", len(A2_LESSONS), "lessons.")
