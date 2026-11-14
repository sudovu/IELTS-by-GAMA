# -*- coding: utf-8 -*-
"""
Deep Comprehensive Curriculum Builder for A2, B1, B2, C1, C2 (Phase 13).
Preserves all existing lesson IDs and enriches every lesson with:
- Objectives (3-4)
- Explanations (> 800 chars with formulas, rules, common errors)
- Examples (3+)
- Guided Exercises (3)
- Assessment Questions (3) with full feedback
"""

import json

# -------------------------------------------------------------
# A2 ELEMENTARY (9 Lessons)
# -------------------------------------------------------------
A2_LESSONS = [
    {
        "id": "curric_a2_gram_past_simple",
        "cefr_level": "A2",
        "module_type": "grammar",
        "title": "Past Simple & Regular vs Irregular Verbs",
        "order_index": 1,
        "prerequisites": ["curric_a1_gram_present_simple"],
        "estimated_minutes": 40,
        "objectives": [
            "Formulate affirmative statements using regular (-ed) and high-frequency irregular past verbs",
            "Construct negative statements and questions using auxiliary 'did' and 'did not' + base verb",
            "Differentiate finished past time expressions ('yesterday', 'last year', 'in 2020', 'ago')",
            "Avoid common past tense errors such as double past marking"
        ],
        "explanation_markdown": """### 1. Form & Linguistic Mechanics
The Past Simple describes completed actions or states at a definite time in the past.

#### Structural Formulas:
- **Affirmative Regular:** Subject + Verb + -ed (*walked, worked, visited*).
- **Affirmative Irregular:** Subject + V2 (*went, saw, ate, bought, spoke*).
- **Negative:** Subject + did not (didn't) + Base Verb.
  * Example: *I didn't visit Paris.* (NOT *didn't visited*).
- **Interrogative:** Did + Subject + Base Verb?
  * Example: *Did you see the match yesterday?*

### 2. Regular Verb Spelling Rules
- Verbs ending in -e: add **-d** (*live ➔ lived*).
- Verbs ending in consonant + y: change to **-ied** (*study ➔ studied*).
- Short verbs ending in consonant-vowel-consonant (CVC): double final consonant (*stop ➔ stopped, plan ➔ planned*).

### 3. Common Learner Traps:
1. **Double Marking:** ✗ *We didn't went.* ➔ ✓ *We didn't go.* (The auxiliary 'did' already carries past tense).
2. **Question Inversion:** ✗ *Did you saw him?* ➔ ✓ *Did you see him?*
3. **Confusion with 'was/were':** ✗ *Where did you was?* ➔ ✓ *Where were you?*""",
        "examples": [
            {"text": "We visited the British Museum yesterday afternoon and bought several postcards.", "notes": "Regular past 'visited' and irregular past 'bought' in completed past context."},
            {"text": "The company did not achieve its sales target last quarter.", "notes": "Negative past simple with auxiliary 'did not' + base verb 'achieve'."},
            {"text": "Did the flight arrive on schedule three hours ago?", "notes": "Question formula with 'Did' + subject + base verb 'arrive' + 'ago'."}
        ],
        "guided_exercises": [
            {
                "id": "a2_g_ge_1",
                "prompt": "Complete with past simple: 'Last night, we _____ (see) an excellent documentary.'",
                "answer": "saw",
                "explanation": "'See' is irregular; its past simple form is 'saw'."
            },
            {
                "id": "a2_g_ge_2",
                "prompt": "Correct the error: 'She didn't bought the laptop.'",
                "answer": "She didn't buy the laptop.",
                "explanation": "After 'didn't', the main verb must be in its base infinitive form: 'buy'."
            },
            {
                "id": "a2_g_ge_3",
                "prompt": "Form a past question: '_____ you finish your homework yesterday?' (Do / Did / Was)",
                "answer": "Did",
                "explanation": "Past simple questions for action verbs require auxiliary 'Did'."
            }
        ],
        "assessment": [
            {
                "id": "a2_g_as_1",
                "question": "Which sentence demonstrates grammatically correct past simple negative form?",
                "options": [
                    "They didn't went to the conference last week.",
                    "They didn't go to the conference last week.",
                    "They not went to the conference last week.",
                    "They weren't go to the conference last week."
                ],
                "correct_index": 1,
                "explanation": "'didn't' + base verb 'go' is the correct negative structure."
            },
            {
                "id": "a2_g_as_2",
                "question": "Select the correct past form of the irregular verb 'catch':",
                "options": [
                    "catched",
                    "caught",
                    "cought",
                    "catcht"
                ],
                "correct_index": 1,
                "explanation": "The past simple of 'catch' is irregularly spelled 'caught' /kɔːt/."
            },
            {
                "id": "a2_g_as_3",
                "question": "Choose the correct question format:",
                "options": [
                    "What time did your train arrived?",
                    "What time did your train arrive?",
                    "What time was your train arrived?",
                    "What time does your train arrived yesterday?"
                ],
                "correct_index": 1,
                "explanation": "Wh-word + did + subject + base verb: 'did your train arrive'."
            }
        ]
    },
    {
        "id": "curric_a2_vocab_travel_food",
        "cefr_level": "A2",
        "module_type": "vocabulary",
        "title": "Travel, Food, Dining & Directions",
        "order_index": 2,
        "prerequisites": ["curric_a1_vocab_everyday_essentials"],
        "estimated_minutes": 35,
        "objectives": [
            "Use countable and uncountable food and dining nouns accurately with quantifiers",
            "Distinguish between 'much' (uncountable) and 'many' (countable)",
            "Order food, drinks, and dietary modifications politely in restaurant environments"
        ],
        "explanation_markdown": """### 1. Countable vs Uncountable Nouns
- **Countable Nouns (Can be pluralized, take 'a/an', use 'many/few'):**
  * *apple/apples, meal/meals, restaurant/restaurants, potato/potatoes, suitcase/suitcases.*
- **Uncountable Nouns (Mass, liquid, abstract; no plural, take 'much/little'):**
  * *water, rice, bread, information, luggage, accommodation, luggage, currency.*

### 2. Quantifiers Matrix
- **Affirmative:** *some* (*We bought some bread and some apples.*)
- **Negative & Questions:** *any* (*We don't have any milk. Do you have any sugar?*)
- **Large Quantities:**
  * Countable: *many books, a lot of books.*
  * Uncountable: *much luggage, a lot of luggage.*

### 3. Dining Phrases:
- *Could we have a table for two, please?*
- *I am allergic to nuts. Does this dish contain peanuts?*
- *Could we have the bill, please?*""",
        "examples": [
            {"text": "We did not have much luggage, so we walked to the hotel from the terminal.", "notes": "'Luggage' is uncountable, requiring 'much'."},
            {"text": "Are there any vegetarian options available on the evening menu?", "notes": "'Any' used in questions with plural countable noun."},
            {"text": "Could I please order the grilled salmon with steamed vegetables on the side?", "notes": "Standard polite restaurant ordering formula."}
        ],
        "guided_exercises": [
            {
                "id": "a2_v_ge_1",
                "prompt": "Insert 'much' or 'many': 'There isn't _____ information on the display board.'",
                "answer": "much",
                "explanation": "'Information' is an uncountable noun in English, requiring 'much'."
            },
            {
                "id": "a2_v_ge_2",
                "prompt": "Insert 'some' or 'any': 'Do you have _____ fresh orange juice left?'",
                "answer": "any",
                "explanation": "Standard questions about quantity take 'any'."
            },
            {
                "id": "a2_v_ge_3",
                "prompt": "Correct the error: 'I need to buy two luggages for my holiday.'",
                "answer": "I need to buy two pieces of luggage for my holiday.",
                "explanation": "'Luggage' is uncountable; use partitive 'pieces of luggage'."
            }
        ],
        "assessment": [
            {
                "id": "a2_v_as_1",
                "question": "Which noun in the list is UNCOUNTABLE in English?",
                "options": [
                    "Baggage",
                    "Suitcase",
                    "Bag",
                    "Ticket"
                ],
                "correct_index": 0,
                "explanation": "'Baggage' and 'luggage' are strictly uncountable mass nouns."
            },
            {
                "id": "a2_v_as_2",
                "question": "Choose the correct sentence:",
                "options": [
                    "How many money did you spend on lunch?",
                    "How much money did you spend on lunch?",
                    "How many moneys did you spend on lunch?",
                    "How much moneies did you spend on lunch?"
                ],
                "correct_index": 1,
                "explanation": "'Money' is uncountable, requiring 'How much'."
            },
            {
                "id": "a2_v_as_3",
                "question": "How do you politely ask for the check at a British restaurant?",
                "options": [
                    "Give me the receipt now.",
                    "Could we have the bill, please?",
                    "I want to pay money.",
                    "Bring the invoice."
                ],
                "correct_index": 1,
                "explanation": "'Could we have the bill, please?' is the standard idiomatic formula in the UK."
            }
        ]
    },
    {
        "id": "curric_a2_read_menus",
        "cefr_level": "A2",
        "module_type": "reading",
        "title": "Scanning Menus, Advertisements & Itineraries",
        "order_index": 3,
        "prerequisites": ["curric_a2_vocab_travel_food"],
        "estimated_minutes": 35,
        "objectives": [
            "Scan multi-section menus to identify dietary ingredients and pricing",
            "Extract operational dates, departure times, and luggage restrictions from flight itineraries",
            "Differentiate between inclusions and optional exclusions in travel advertisements"
        ],
        "explanation_markdown": """### Practical Scanning in General Training Reading
In IELTS General Training Section 1, candidates read real-world timetables, notices, and brochures.

#### Text: Highland Day Tour Brochure
```
SCOTTISH HIGHLANDS ONE-DAY COACH EXCURSION
Departure: 08:00 AM from Edinburgh Stance D.
Returns: 19:30 PM.
Price: Adults £55.00 | Children under 12: £35.00.
Included: Luxury coach transport, professional English guide, audio headsets.
Excluded: Admission to Stirling Castle (£16.50), lunch, travel insurance.
Note: Cancellations made 48 hours prior to departure receive a full refund.
```

#### Analytical Reading Rules:
1. **Locating Inclusions vs Exclusions:** Scrutinize 'Included' and 'Excluded' bullet points.
2. **Conditional Eligibility:** Pay close attention to age brackets (*under 12*) and time constraints (*48 hours*).""",
        "examples": [
            {"text": "Stirling Castle admission is not included in the £55 tour fee.", "notes": "Distinguishing base price from optional exclusions."},
            {"text": "A full refund is available if cancelled at least 48 hours before departure.", "notes": "Reading cancellation policy terms."},
            {"text": "The coach tour lasts eleven and a half hours in total.", "notes": "Calculating duration from 08:00 to 19:30."}
        ],
        "guided_exercises": [
            {
                "id": "a2_r_ge_1",
                "prompt": "How much does a ticket cost for a 10-year-old child?",
                "answer": "£35.00",
                "explanation": "Children under 12 qualify for the reduced child rate of £35.00."
            },
            {
                "id": "a2_r_ge_2",
                "prompt": "Is lunch provided free of charge on the tour?",
                "answer": "No",
                "explanation": "The text lists 'lunch' under 'Excluded'."
            },
            {
                "id": "a2_r_ge_3",
                "prompt": "From which station stance does the coach depart?",
                "answer": "Edinburgh Stance D",
                "explanation": "The brochure specifies 'Edinburgh Stance D'."
            }
        ],
        "assessment": [
            {
                "id": "a2_r_as_1",
                "question": "What is the total cost for one adult who also purchases Stirling Castle admission?",
                "options": [
                    "£55.00",
                    "£65.00",
                    "£71.50",
                    "£80.00"
                ],
                "correct_index": 2,
                "explanation": "£55.00 base tour + £16.50 castle entrance = £71.50."
            },
            {
                "id": "a2_r_as_2",
                "question": "To receive a 100% refund upon cancellation, when must the customer notify the company?",
                "options": [
                    "24 hours before departure",
                    "48 hours prior to departure",
                    "On the morning of the tour",
                    "Refunds are never granted"
                ],
                "correct_index": 1,
                "explanation": "The text explicitly states '48 hours prior to departure'."
            },
            {
                "id": "a2_r_as_3",
                "question": "Which service is explicitly INCLUDED in the tour price?",
                "options": [
                    "Travel insurance",
                    "Professional English guide",
                    "Lunch buffet",
                    "Hotel pick-up"
                ],
                "correct_index": 1,
                "explanation": "'Professional English guide' is listed under 'Included'."
            }
        ]
    },
    {
        "id": "curric_a2_listen_directions",
        "cefr_level": "A2",
        "module_type": "listening",
        "title": "Following Spoken Directions & Announcements",
        "order_index": 4,
        "prerequisites": ["curric_a2_vocab_travel_food"],
        "estimated_minutes": 40,
        "objectives": [
            "Follow sequential spatial instructions on a campus or city map",
            "Identify gate changes, delays, and boarding calls in airport public address announcements",
            "Recognize prepositional location phrases ('adjacent to', 'opposite', 'in between')"
        ],
        "explanation_markdown": """### Transcript-Based Listening Strategy: Map Labelling
*(Practice session using authentic IELTS Part 2 style direction scripts.)*

#### Audio Script:
```
GUIDE: Welcome to the University Library orientation. If you look at the floor plan, we are standing 
at the main entrance facing North. Directly in front of you is the Reception Desk. To your immediate 
left is the Computing Suite, where fifty desktop terminals are installed. 
Now, if you walk past the Reception Desk and turn right down the east corridor, you will find 
the Group Study Rooms. They are situated between the Photocopier Room and the Law Collection.
Please note: quiet individual study booths are located on the second floor, accessible via the central staircase.
```

#### Strategic Map Markers:
1. **Starting Point:** Always identify where the speaker begins (*main entrance facing North*).
2. **Direction Shifts:** Note pivot words (*turn right, walk past, opposite*).
3. **Bracketing Phrases:** *Between X and Y* identifies a sandwiched location.""",
        "examples": [
            {"text": "The Computing Suite is located to the immediate left of the main entrance.", "notes": "Direct spatial relationship from orientation origin."},
            {"text": "The Group Study Rooms are between the Photocopier Room and Law Collection.", "notes": "Location identified using preposition 'between'."},
            {"text": "Quiet study booths are on the second floor.", "notes": "Vertical floor level extraction."}
        ],
        "guided_exercises": [
            {
                "id": "a2_l_ge_1",
                "prompt": "What is directly in front of the visitor at the main entrance?",
                "answer": "Reception Desk",
                "explanation": "The guide states 'Directly in front of you is the Reception Desk'."
            },
            {
                "id": "a2_l_ge_2",
                "prompt": "What facility is located to the immediate left of the entrance?",
                "answer": "Computing Suite",
                "explanation": "The text confirms 'To your immediate left is the Computing Suite'."
            },
            {
                "id": "a2_l_ge_3",
                "prompt": "Where are the Group Study Rooms located?",
                "answer": "between the Photocopier Room and the Law Collection",
                "explanation": "The guide states 'situated between the Photocopier Room and the Law Collection'."
            }
        ],
        "assessment": [
            {
                "id": "a2_l_as_1",
                "question": "How do students reach the quiet individual study booths?",
                "options": [
                    "Through the east corridor",
                    "Via the central staircase to the second floor",
                    "Behind the Computing Suite",
                    "Across from the reception desk"
                ],
                "correct_index": 1,
                "explanation": "The guide states booths are 'on the second floor, accessible via the central staircase'."
            },
            {
                "id": "a2_l_as_2",
                "question": "If a speaker says 'take the second turning on your left', what must you do?",
                "options": [
                    "Turn left at the very first street",
                    "Ignore the first left turn and turn left at the second street",
                    "Turn right twice",
                    "Walk past two streets on your right"
                ],
                "correct_index": 1,
                "explanation": "'Second turning on your left' skips the first left and takes the next left."
            },
            {
                "id": "a2_l_as_3",
                "question": "What does 'adjacent to' mean in spatial directions?",
                "options": [
                    "Across the street",
                    "Directly next to / beside",
                    "Behind the building",
                    "Underneath"
                ],
                "correct_index": 1,
                "explanation": "'Adjacent to' is a formal synonym for 'next to' or 'adjoining'."
            }
        ]
    },
    {
        "id": "curric_a2_write_emails",
        "cefr_level": "A2",
        "module_type": "writing",
        "title": "Informal Letters & Descriptive Emails",
        "order_index": 5,
        "prerequisites": ["curric_a1_write_sentences", "curric_a2_gram_past_simple"],
        "estimated_minutes": 45,
        "objectives": [
            "Structure informal letters and emails with standard openings, bodies, and closings",
            "Deploy coordinating conjunctions ('and', 'but', 'so', 'because') to combine simple clauses",
            "Describe a holiday, event, or personal experience chronologically in 80–120 words"
        ],
        "explanation_markdown": """### 1. Informal Email Structure
- **Salutation:** *Dear Sam,* / *Hi Sarah,*
- **Opening Warm-Up:** *I hope you are doing well. I am writing to tell you about my trip to Scotland.*
- **Body Paragraph 1 (What happened / Past events):** *We arrived in Edinburgh on Friday afternoon. The weather was cold but sunny...*
- **Body Paragraph 2 (Feelings / Highlights):** *The highlight of the weekend was visiting the castle. The view was breathtaking...*
- **Closing Sign-Off:** *Let's catch up soon. Give my best to your family.*
- **Sign-Off:** *Best wishes,* / *All the best,* + [First Name].

### 2. Conjunctions for Clause Combining
- **AND (Addition):** *We rented a car and drove to the coast.*
- **BUT (Contrast):** *The hotel was modest, but the food was delicious.*
- **SO (Result):** *It rained heavily, so we spent the afternoon in the museum.*
- **BECAUSE (Reason):** *We booked early because tickets sell out quickly.*""",
        "examples": [
            {"text": "Dear Alex, I hope you are having a wonderful summer break.", "notes": "Natural informal opening."},
            {"text": "We wanted to climb the mountain, but the fog was too dense, so we returned to the lodge.", "notes": "Effective combination of contrast ('but') and result ('so')."},
            {"text": "Write back soon and let me know your news. All the best, Marcus.", "notes": "Friendly, standard closing and sign-off."}
        ],
        "guided_exercises": [
            {
                "id": "a2_w_ge_1",
                "prompt": "Join the clauses using 'because': 'We stayed indoors. The storm was severe.'",
                "answer": "We stayed indoors because the storm was severe.",
                "explanation": "'Because' introduces the causal explanation."
            },
            {
                "id": "a2_w_ge_2",
                "prompt": "Join using 'so': 'The tickets were expensive. We decided not to go.'",
                "answer": "The tickets were expensive, so we decided not to go.",
                "explanation": "'So' introduces the logical consequence/result."
            },
            {
                "id": "a2_w_ge_3",
                "prompt": "Which closing sign-off is appropriate for a casual email to a close friend? (Yours faithfully / All the best)",
                "answer": "All the best",
                "explanation": "'Yours faithfully' is formal; 'All the best' is friendly and informal."
            }
        ],
        "assessment": [
            {
                "id": "a2_w_as_1",
                "question": "Which sentence demonstrates the correct use of 'so' to indicate result?",
                "options": [
                    "I woke up late so I missed the bus.",
                    "I woke up late because I missed the bus.",
                    "I woke up late but I missed the bus.",
                    "I missed the bus so I woke up late."
                ],
                "correct_index": 0,
                "explanation": "Waking up late caused the result of missing the bus: 'so I missed the bus'."
            },
            {
                "id": "a2_w_as_2",
                "question": "Which salutation is suitable for an email to a friend or classmate?",
                "options": [
                    "To Whom It May Concern,",
                    "Dear Sir/Madam,",
                    "Hi David,",
                    "Respected Sir,"
                ],
                "correct_index": 2,
                "explanation": "'Hi David,' or 'Dear David,' is the standard informal salutation."
            },
            {
                "id": "a2_w_as_3",
                "question": "Choose the correctly joined compound sentence:",
                "options": [
                    "The museum was crowded, but we managed to see the famous paintings.",
                    "The museum was crowded, because we managed to see the famous paintings.",
                    "The museum was crowded so but we saw the paintings.",
                    "The museum was crowded although so we saw the paintings."
                ],
                "correct_index": 0,
                "explanation": "'But' correctly expresses the contrast between being crowded and still seeing the paintings."
            }
        ]
    },
    {
        "id": "curric_a2_speak_past_experiences",
        "cefr_level": "A2",
        "module_type": "speaking",
        "title": "Describing Past Experiences & Holidays",
        "order_index": 6,
        "prerequisites": ["curric_a2_gram_past_simple"],
        "estimated_minutes": 35,
        "objectives": [
            "Narrate a past personal event chronologically using time markers ('First', 'Then', 'After that')",
            "Express personal feelings and reactions about past holidays and celebrations",
            "Answer IELTS Speaking Part 1 questions regarding past hobbies and childhood activities"
        ],
        "explanation_markdown": """### 1. Chronological Sequence Markers
When describing past events, avoid repeating 'and then'. Use varied connectors:
- **Beginning:** *To begin with, / On the first morning, / A couple of years ago...*
- **Continuation:** *Following that, / Later that afternoon, / Afterwards...*
- **Unexpected Event:** *Suddenly, / Out of nowhere, / To our surprise...*
- **Conclusion:** *In the end, / Looking back, it was an unforgettable trip.*

### 2. Expressing Reactions & Evaluative Adjectives
Instead of repeating 'good' or 'bad', use A2/B1 evaluative adjectives:
- *breathtaking scenery, delicious regional cuisine, hospitable locals, exhausting journey, peaceful atmosphere.*""",
        "examples": [
            {"text": "Two summers ago, I travelled to the Lake District with three close friends from university.", "notes": "Clear temporal setting and companions."},
            {"text": "On the second day, we hiked up the peak; the panoramic view from the summit was breathtaking.", "notes": "Sequence marker + descriptive evaluative adjective."},
            {"text": "Although the hike was tiring, we had an unforgettable time together.", "notes": "Concession ('although') with evaluative summary."}
        ],
        "guided_exercises": [
            {
                "id": "a2_sp_ge_1",
                "prompt": "Insert a sequence connector: 'First, we visited the castle. _____, we had lunch in a traditional pub.'",
                "answer": "After that",
                "explanation": "'After that' or 'Then' continues chronological narrative."
            },
            {
                "id": "a2_sp_ge_2",
                "prompt": "Select an evaluative adjective: 'The mountain view was absolutely _____.' (breathtaking / bored)",
                "answer": "breathtaking",
                "explanation": "'Breathtaking' describes magnificent views."
            },
            {
                "id": "a2_sp_ge_3",
                "prompt": "Answer in past simple: 'Did you enjoy your last holiday?' (Yes, I did / Yes, I enjoy)",
                "answer": "Yes, I did",
                "explanation": "Short answer to 'Did you...?' is 'Yes, I did'."
            }
        ],
        "assessment": [
            {
                "id": "a2_sp_as_1",
                "question": "Which response to 'Tell me about a memorable holiday' demonstrates the best chronological structure?",
                "options": [
                    "I went Spain. It was good. I like beach.",
                    "Three years ago, I visited Barcelona. First, we explored the historic gothic quarter, and later we visited the famous cathedral. It was truly memorable.",
                    "Spain is very big country and I want go next year.",
                    "I am going to Barcelona yesterday and swimming."
                ],
                "correct_index": 1,
                "explanation": "Provides past time setting, chronological sequence markers, and evaluative vocabulary."
            },
            {
                "id": "a2_sp_as_2",
                "question": "Which adjective expresses high praise for food during a vacation?",
                "options": [
                    "Exhausting",
                    "Delectable",
                    "Boring",
                    "Crowded"
                ],
                "correct_index": 1,
                "explanation": "'Delectable' or 'delicious' evaluates food positively."
            },
            {
                "id": "a2_sp_as_3",
                "question": "Choose the natural past narrative phrase:",
                "options": [
                    "Looking back, it was an unforgettable experience.",
                    "Look back, it is unforgotten experience.",
                    "I look back and it did forgettable.",
                    "Looking backward, it was no good memory."
                ],
                "correct_index": 0,
                "explanation": "'Looking back, it was an unforgettable experience' is idiomatic and reflective."
            }
        ]
    },
    {
        "id": "curric_a2_pron_past_endings",
        "cefr_level": "A2",
        "module_type": "pronunciation",
        "title": "Regular Past Tense Endings (/t/, /d/, /ɪd/)",
        "order_index": 7,
        "prerequisites": ["curric_a1_pron_alphabet", "curric_a2_gram_past_simple"],
        "estimated_minutes": 40,
        "objectives": [
            "Master the 3 phonetic realizations of regular past '-ed': /t/, /d/, and /ɪd/",
            "Identify when '-ed' adds an extra syllable (/ɪd/ after /t/ and /d/)",
            "Eliminate unnecessary extra syllables when pronouncing voiceless past verbs (e.g. 'walked' is 1 syllable, not 2)"
        ],
        "explanation_markdown": """### The 3 Rules of Past '-ed' Pronunciation
The pronunciation of '-ed' depends strictly on the final sound of the base verb:

#### 1. Pronounced as /ɪd/ (Adds an Extra Syllable):
ONLY after base verbs ending in sound **/t/** or **/d/**:
- *want ➔ wanted* /ˈwɒntɪd/ (2 syllables)
- *need ➔ needed* /ˈniːdɪd/ (2 syllables)
- *decide ➔ decided* /dɪˈsaɪdɪd/ (3 syllables)

#### 2. Pronounced as /t/ (No Extra Syllable):
After voiceless ending sounds (/p/, /k/, /s/, /ʃ/, /tʃ/, /f/):
- *walk ➔ walked* /wɔːkt/ (1 syllable, NOT walk-ed)
- *watch ➔ watched* /wɒtʃt/ (1 syllable)
- *laugh ➔ laughed* /lɑːft/ (1 syllable)

#### 3. Pronounced as /d/ (No Extra Syllable):
After voiced ending sounds (all vowels + /b/, /g/, /v/, /z/, /m/, /n/, /l/, /r/):
- *clean ➔ cleaned* /kliːnd/ (1 syllable)
- *play ➔ played* /pleɪd/ (1 syllable)
- *live ➔ lived* /lɪvd/ (1 syllable)""",
        "examples": [
            {"text": "She decided to study abroad.", "notes": "Verb ending in /d/ takes /ɪd/: /dɪˈsaɪdɪd/ (extra syllable)."},
            {"text": "He walked to the bus stop.", "notes": "Voiceless /k/ takes /t/: /wɔːkt/ (strictly one syllable)."},
            {"text": "They lived in Germany for two years.", "notes": "Voiced /v/ takes /d/: /lɪvd/ (strictly one syllable)."}
        ],
        "guided_exercises": [
            {
                "id": "a2_p_ge_1",
                "prompt": "How is the '-ed' ending pronounced in 'visited'? (/t/ / /d/ / /ɪd/)",
                "answer": "/ɪd/",
                "explanation": "'Visit' ends in sound /t/, requiring the /ɪd/ ending with an extra syllable."
            },
            {
                "id": "a2_p_ge_2",
                "prompt": "How many syllables are there in 'worked'? (1 / 2)",
                "answer": "1",
                "explanation": "'Worked' is pronounced /wɜːkt/, containing only 1 syllable."
            },
            {
                "id": "a2_p_ge_3",
                "prompt": "How is '-ed' pronounced in 'played'? (/t/ / /d/ / /ɪd/)",
                "answer": "/d/",
                "explanation": "'Play' ends in a voiced vowel sound /eɪ/, taking /d/."
            }
        ],
        "assessment": [
            {
                "id": "a2_p_as_1",
                "question": "Which of the following verbs adds an extra syllable when inflected into past simple with '-ed'?",
                "options": [
                    "cooked",
                    "washed",
                    "started",
                    "cleaned"
                ],
                "correct_index": 2,
                "explanation": "'Start' ends in /t/, so 'started' is pronounced /ˈstɑːtɪd/ with 2 syllables."
            },
            {
                "id": "a2_p_as_2",
                "question": "In which word is the '-ed' ending pronounced as voiceless /t/?",
                "options": [
                    "hoped",
                    "opened",
                    "rained",
                    "called"
                ],
                "correct_index": 0,
                "explanation": "'Hope' ends in voiceless /p/, so 'hoped' is pronounced /həʊpt/."
            },
            {
                "id": "a2_p_as_3",
                "question": "Which pair of past tense verbs BOTH have their '-ed' pronounced as /d/?",
                "options": [
                    "looked — visited",
                    "arrived — stayed",
                    "watched — wanted",
                    "stopped — waited"
                ],
                "correct_index": 1,
                "explanation": "Both 'arrive' (/v/) and 'stay' (vowel) end in voiced sounds, taking /d/."
            }
        ]
    },
    {
        "id": "curric_a2_func_shopping",
        "cefr_level": "A2",
        "module_type": "functional",
        "title": "Making Purchases & Transactional Dialogue",
        "order_index": 8,
        "prerequisites": ["curric_a2_vocab_travel_food"],
        "estimated_minutes": 35,
        "objectives": [
            "Handle customer service transactions in retail stores, markets, and travel agencies",
            "Inquire about clothing sizes, fittings, and product availability",
            "Request refunds, exchanges, and payment receipts diplomatically"
        ],
        "explanation_markdown": """### 1. In-Store Customer Inquiries
- **Asking to Try On:** *'Excuse me, could I try this jacket on, please? Where are the fitting rooms?'*
- **Sizes & Stock:** *'Do you happen to have this shirt in a medium / in dark blue?'*
- **Price Check:** *'How much does this cost?'* / *'Is this item on sale?'*

### 2. Payment & Checkout Dialogue
- Cashier: *'Are you paying by cash or card?'*
- Customer: *'Contactless card, please. Could I also have a receipt?'*

### 3. Refunds & Exchanges
- *'I bought this yesterday, but unfortunately it doesn't fit properly. Could I exchange it for a larger size, or get a refund? Here is my receipt.'*""",
        "examples": [
            {"text": "Excuse me, where are the changing rooms located?", "notes": "Standard retail navigation question."},
            {"text": "I would like to return this sweater because the seam is torn. Here is the original receipt.", "notes": "Clear, polite statement of reason for return."},
            {"text": "Do you offer a student discount on software subscriptions?", "notes": "Inquiring about special pricing."}
        ],
        "guided_exercises": [
            {
                "id": "a2_f_ge_1",
                "prompt": "Complete: 'Could I try this _____? Where are the fitting rooms?' (on / in / at)",
                "answer": "on",
                "explanation": "The phrasal verb to test clothing fit is 'try on'."
            },
            {
                "id": "a2_f_ge_2",
                "prompt": "What document must you show to obtain a store refund? (passport / receipt)",
                "answer": "receipt",
                "explanation": "Proof of purchase is confirmed via a 'receipt'."
            },
            {
                "id": "a2_f_ge_3",
                "prompt": "Complete: 'Do you have this shirt _____ a size large?' (at / in / on)",
                "answer": "in",
                "explanation": "Clothing sizes take preposition 'in' (in size large)."
            }
        ],
        "assessment": [
            {
                "id": "a2_f_as_1",
                "question": "How should you ask a shop assistant if an item comes in another color?",
                "options": [
                    "Give me another color now.",
                    "Do you have this in blue, please?",
                    "Change color for me.",
                    "Why this is red?"
                ],
                "correct_index": 1,
                "explanation": "'Do you have this in [color], please?' is the natural polite customer request."
            },
            {
                "id": "a2_f_as_2",
                "question": "What is the meaning of 'fitting room' in a clothing shop?",
                "options": [
                    "The storage room for extra merchandise",
                    "The private booth where customers try on clothes",
                    "The cash register area",
                    "The entrance hallway"
                ],
                "correct_index": 1,
                "explanation": "A fitting room (or changing room) is where customers try on garments."
            },
            {
                "id": "a2_f_as_3",
                "question": "Choose the most polite way to request a cash receipt:",
                "options": [
                    "I demand the paper.",
                    "Could I please have a receipt?",
                    "Make receipt quickly.",
                    "Receipt is required."
                ],
                "correct_index": 1,
                "explanation": "'Could I please have a receipt?' is courteous and formal."
            }
        ]
    },
    {
        "id": "curric_a2_review_milestone",
        "cefr_level": "A2",
        "module_type": "review",
        "title": "A2 Milestone Review & Comprehensive Evaluation",
        "order_index": 9,
        "prerequisites": ["curric_a2_gram_past_simple", "curric_a2_write_emails"],
        "estimated_minutes": 50,
        "objectives": [
            "Synthesize A2 past simple narratives, countability quantifiers, and pronunciation",
            "Demonstrate readiness for intermediate CEFR B1 academic and paragraph training",
            "Verify elimination of double-past marking errors and past-tense mispronunciations"
        ],
        "explanation_markdown": """### A2 Milestone Evaluation Synthesis
Graduation to CEFR B1 requires mastery of:
1. **Past Narrative Competency:** Spontaneous correct use of regular and irregular past verbs.
2. **Clause Linking:** Combining clauses naturally using *and, but, so, because*.
3. **Countability & Quantifiers:** Automatic selection of *much* vs *many*, and *some* vs *any*.
4. **Phonetic Clarity:** Pronouncing '-ed' endings without inserting spurious syllables.

Review the core principles of A2 before starting the milestone assessment.""",
        "examples": [
            {"text": "Last winter, we spent two weeks in Edinburgh and visited several historic landmarks.", "notes": "Synthesis: irregular past 'spent' and regular past 'visited'."},
            {"text": "There wasn't much snow, but the weather was crisp and sunny, so we walked every day.", "notes": "Quantifier 'much' with clause linkers 'but' and 'so'."},
            {"text": "Could you tell me how much this guide book costs?", "notes": "Polite transactional indirect question."}
        ],
        "guided_exercises": [
            {
                "id": "a2_rev_ge_1",
                "prompt": "Find and correct the error: 'We didn't bought many souvenir.'",
                "answer": "We didn't buy many souvenirs.",
                "explanation": "'didn't' requires base verb 'buy'; 'many' requires plural noun 'souvenirs'."
            },
            {
                "id": "a2_rev_ge_2",
                "prompt": "Fill in the blank: 'I was tired, _____ I went to bed early.' (because / so)",
                "answer": "so",
                "explanation": "Going to bed early was the result of being tired, requiring 'so'."
            },
            {
                "id": "a2_rev_ge_3",
                "prompt": "Pronounce 'decided'. How many syllables? (2 / 3)",
                "answer": "3",
                "explanation": "de-cid-ed /dɪˈsaɪdɪd/ has 3 syllables because it ends in /d/."
            }
        ],
        "assessment": [
            {
                "id": "a2_rev_as_1",
                "question": "Which sentence contains ZERO grammatical or lexical errors?",
                "options": [
                    "She didn't went to the market because it was raining heavily.",
                    "She didn't go to the market because it was raining heavily.",
                    "She didn't go to the market so it was raining heavily.",
                    "She wasn't go to the market because it rained heavily."
                ],
                "correct_index": 1,
                "explanation": "'didn't go' (base verb after auxiliary) + 'because' (reason for not going)."
            },
            {
                "id": "a2_rev_as_2",
                "question": "Choose the sentence with correct quantifiers for uncountable nouns:",
                "options": [
                    "We didn't have many luggage on our trip.",
                    "We didn't have much luggage on our trip.",
                    "We didn't have many luggages on our trip.",
                    "We didn't have much suitcases on our trip."
                ],
                "correct_index": 1,
                "explanation": "'Luggage' is uncountable and takes 'much'. 'Suitcase' is countable."
            },
            {
                "id": "a2_rev_as_3",
                "question": "In which sentence is the '-ed' ending pronounced as a separate syllable /ɪd/?",
                "options": [
                    "He painted the fence yesterday.",
                    "He worked all day.",
                    "He watched a film.",
                    "He cleaned his room."
                ],
                "correct_index": 0,
                "explanation": "'Paint' ends in /t/, so 'painted' /ˈpeɪntɪd/ has the /ɪd/ extra syllable."
            }
        ]
    }
]

with open("content/curriculum/a2.json", "w", encoding="utf-8") as f:
    json.dump(A2_LESSONS, f, indent=2, ensure_ascii=False)
print("Saved A2:", len(A2_LESSONS), "lessons.")
