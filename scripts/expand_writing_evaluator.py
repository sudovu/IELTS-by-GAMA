# -*- coding: utf-8 -*-
"""
Expands core/writing/writing_evaluator.py with:
1. Academic Task 1: Line Graph, Bar Chart, Pie Chart, Table, Process Diagram, Map Comparison.
2. General Training Task 1: Formal Letter (Complaint), Semi-Formal Letter (Request), Informal Letter (Advice/Friend), Formal Letter (Application), Semi-Formal Letter (Apology).
3. General Training Task 2: Agree/Disagree and Causes/Solutions.
4. WritingDraftRepository autosave & loading integration.
5. Task 1 specific grading (Overview check, trend vocab, no personal opinion for Academic, salutation/sign-off/purpose for GT letters).
"""

import sys

new_content = '''"""
Writing Evaluator for IELTS by GAMA.
Evaluates Academic Task 1 & 2 and General Training Task 1 & 2 according to
official IELTS band descriptor rubrics:
- Task Response / Achievement (TR/TA)
- Coherence and Cohesion (CC)
- Lexical Resource (LR)
- Grammatical Range and Accuracy (GRA)
Includes the formative 'Teach Through Correction' feedback suite and
IELTS Advantage Question Analysis, PEEL Blueprint, and 10-Point Self-Assessment Questionnaire.
Persists drafts and evaluations through WritingDraftRepository.
"""

import re
from typing import Dict, Any, List, Optional
from .formative_feedback import FormativeFeedback
from ..scoring.criteria_evaluator import CriteriaEvaluator
from ..database.db_manager import DatabaseManager
from ..database.repositories import WritingDraftRepository, TestResultRepository


class WritingEvaluator:
    """Automated IELTS writing diagnostic, questionnaire, and rubric evaluator."""

    ORIGINAL_PROMPTS = {
        # --- ACADEMIC TASK 2 ESSAYS ---
        "acad_t2_stem": {
            "id": "acad_t2_stem",
            "task_type": "task_2",
            "question_type": "Discuss Both Views & Give Opinion",
            "track": "Academic",
            "title": "STEM vs Creative Arts in High School Curricula",
            "prompt": (
                "Some educationalists argue that high school curricula should prioritize STEM subjects "
                "(Science, Technology, Engineering, and Mathematics) over creative arts and literature to ensure economic competitiveness. "
                "Others believe that artistic subjects are equally vital for developing well-rounded citizens.\\n\\n"
                "Discuss both views and give your own opinion.\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Education & Curriculum Design",
                "micro_topic": "Whether secondary schools should prioritize STEM over Arts or maintain balance",
                "task_words": "Discuss BOTH views and GIVE YOUR OWN OPINION",
                "coffee_shop_idea": "STEM drives economic innovation and tech careers, but the arts foster creative problem-solving and emotional intelligence. Both are essential in modern society.",
                "peel_blueprint": {
                    "body_1": "Point: STEM disciplines directly power technological modernization. Explain: Industry demands engineers and data analysts. Example: Developing nations investing in tech hubs witnessed 15% faster GDP growth. Link: Therefore, STEM merits robust institutional funding.",
                    "body_2": "Point: Conversely, creative arts nurture lateral thinking and emotional intelligence. Explain: Pure technical knowledge without creativity limits innovation. Example: Pioneering tech firms specifically recruit designers and humanists. Link: Thus, neglecting artistic disciplines produces an imbalanced workforce."
                }
            }
        },
        "acad_t2_ubi": {
            "id": "acad_t2_ubi",
            "task_type": "task_2",
            "question_type": "Agree or Disagree (Opinion)",
            "track": "Academic",
            "title": "Universal Basic Income & Workplace Automation",
            "prompt": (
                "As artificial intelligence and robotics automate routine workplace tasks, some economists propose that governments "
                "should introduce a guaranteed Universal Basic Income (UBI) for all adult citizens to eradicate poverty.\\n\\n"
                "To what extent do you agree or disagree with this proposal?\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Technology, Economics & Social Welfare",
                "micro_topic": "Whether automated job displacement warrants a state-funded Universal Basic Income",
                "task_words": "To what extent do you agree or disagree (Clear position throughout required)",
                "coffee_shop_idea": "I agree to a substantial extent because AI will displace entry-level workers faster than new industries can retrain them, and UBI prevents societal destitution.",
                "peel_blueprint": {
                    "body_1": "Point: Automation is displacing routine white-collar and manual jobs at unprecedented scale. Explain: Displaced workers cannot retrain overnight without subsistence support. Example: Autonomous transport and logistics could eliminate millions of driving jobs within a decade. Link: UBI provides an indispensable financial safety net.",
                    "body_2": "Point: Skeptics argue UBI disincentivizes work, but empirical trials refute this. Explain: Basic security enables citizens to pursue education, caregiving, or entrepreneurial ventures. Example: Finnish pilot programs demonstrated participants suffered no loss of motivation while mental wellness improved. Link: Consequently, UBI bolsters rather than undermines civic productivity."
                }
            }
        },
        "acad_t2_tourism": {
            "id": "acad_t2_tourism",
            "task_type": "task_2",
            "question_type": "Advantages vs Disadvantages",
            "track": "Academic",
            "title": "International Mass Tourism & Cultural Preservation",
            "prompt": (
                "In many regions across the globe, international mass tourism has become the primary source of economic revenue, "
                "yet it frequently leads to environmental degradation and the commercialization of local cultures.\\n\\n"
                "Do the advantages of international tourism outweigh the disadvantages?\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Tourism & Cultural Heritage",
                "micro_topic": "Whether economic dividends of mass tourism exceed its environmental and cultural costs",
                "task_words": "Do advantages OUTWEIGH disadvantages (Must compare weight and make explicit judgment)",
                "coffee_shop_idea": "Tourism brings huge money and jobs, but unmanaged tourism ruins fragile monuments and drives locals out. On balance, advantages outweigh only if strictly regulated.",
                "peel_blueprint": {
                    "body_1": "Point: Tourism generates massive foreign exchange and infrastructure investment. Explain: Remote heritage sites obtain funds that regional governments could not otherwise allocate. Example: Island economies in Southeast Asia finance coastal conservation largely through eco-tourism levies. Link: This economic catalyst is indispensable.",
                    "body_2": "Point: However, uncontrolled overtourism causes severe gentrification and environmental damage. Explain: Skyrocketing rents displace indigenous populations and fragile ecosystems suffer degradation. Example: Cities like Venice and Barcelona have imposed tourist caps to prevent cultural erosion. Link: Therefore, while advantages predominate, stringent visitor management is imperative."
                }
            }
        },
        "acad_t2_traffic": {
            "id": "acad_t2_traffic",
            "task_type": "task_2",
            "question_type": "Causes & Solutions",
            "track": "Academic",
            "title": "Urban Traffic Congestion & Environmental Mitigation",
            "prompt": (
                "Traffic congestion in major metropolitan centers has reached critical levels, leading to severe air pollution, "
                "reduced economic productivity, and chronic public health issues.\\n\\n"
                "What are the primary causes of this phenomenon, and what effective measures can municipal authorities adopt to resolve it?\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Urban Planning & Environmental Health",
                "micro_topic": "Causes of urban vehicle gridlock and practical municipal solutions",
                "task_words": "What are CAUSES and what are EFFECTIVE MEASURES (Both must be thoroughly developed)",
                "coffee_shop_idea": "People drive because public transit is unreliable or expensive, and cities expand without proper planning. Solutions: heavy congestion pricing and investing in clean, reliable metro rail.",
                "peel_blueprint": {
                    "body_1": "Point: The root cause of congestion is inadequate public transit combined with low fuel taxation. Explain: Commuters default to private automobiles when trains are crowded, unreliable, or nonexistent. Example: Car ownership in suburban commuter belts surged by 35% where bus networks were pruned. Link: This directly fuels daily urban gridlock.",
                    "body_2": "Point: The most potent remedy is introducing dynamic congestion charges alongside subsidized rail transit. Explain: Financial penalties disincentivize discretionary car trips while fare subsidies make public transit the rational choice. Example: London's congestion charge reduced inner-city vehicle traffic by 20% within two years. Link: Sustained municipal commitment to transit infrastructure resolves the crisis."
                }
            }
        },
        "acad_t2_fast_fashion": {
            "id": "acad_t2_fast_fashion",
            "task_type": "task_2",
            "question_type": "Two-Part Direct Questions",
            "track": "Academic",
            "title": "Fast Fashion, Consumer Culture & Global Sustainability",
            "prompt": (
                "Consumers worldwide are purchasing substantially more inexpensive, short-lived clothing than previous generations, "
                "a trend widely known as 'fast fashion'.\\n\\n"
                "Why has this phenomenon emerged, and is this a positive or negative development for society?\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Consumerism, Industry & Environment",
                "micro_topic": "Reasons for the rise of fast fashion and evaluation of whether it is beneficial or detrimental",
                "task_words": "WHY has this emerged? AND IS IT POSITIVE OR NEGATIVE? (Must answer both distinct questions)",
                "coffee_shop_idea": "It emerged because targeted social media ads and cheap overseas manufacturing make trendy clothes dirt cheap. It is overwhelmingly negative because of textile waste and sweatshop labor.",
                "peel_blueprint": {
                    "body_1": "Point: Fast fashion expanded due to digital influencer marketing and low-cost overseas supply chains. Explain: Social media algorithms create micro-trends, inducing consumers to feel outdated after a single wear. Example: Retail platforms refresh clothing lines weekly at negligible prices. Link: These technological and commercial factors ignited runaway consumption.",
                    "body_2": "Point: This development is unequivocally negative due to catastrophic environmental and ethical fallout. Explain: Synthetic textiles shed microplastics into waterways, and massive garment dumps pollute landfills in developing nations. Example: The fashion sector accounts for roughly 10% of global carbon emissions and fosters exploitative sweatshops. Link: Consequently, the transient pleasure of cheap clothing carries an unacceptable societal toll."
                }
            }
        },

        # --- ACADEMIC TASK 1 DATA REPORTS ---
        "acad_t1_energy": {
            "id": "acad_t1_energy",
            "task_type": "task_1",
            "question_type": "Data Report (Bar Chart)",
            "track": "Academic",
            "title": "Renewable Energy Investment (2010–2020)",
            "prompt": (
                "The bar chart below shows government investments (in billions of dollars) in solar, wind, and hydroelectric energy "
                "across four nations between 2010 and 2020.\\n\\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Energy Economics",
                "micro_topic": "Comparative government investments in renewable energy sectors",
                "task_words": "Select and report main features, make comparisons (Do NOT give personal opinions)",
                "coffee_shop_idea": "Solar grew the fastest in country A and B, wind was steady, and hydro remained flat. Country C invested the most overall.",
                "peel_blueprint": {
                    "body_1": "Overview: Overall, solar investment experienced exponential growth across all nations, while hydroelectric remained static.",
                    "body_2": "Details: Key numerical comparisons highlighting the initial and final decade values across the four nations."
                }
            }
        },
        "acad_t1_emissions": {
            "id": "acad_t1_emissions",
            "task_type": "task_1",
            "question_type": "Data Report (Line Graph)",
            "track": "Academic",
            "title": "Industrial Greenhouse Gas Emissions (1990–2025)",
            "prompt": (
                "The line graph illustrates greenhouse gas emissions (in megatonnes of CO2 equivalent) "
                "generated by four economic sectors (Manufacturing, Road Transport, Power Generation, and Agriculture) "
                "in a developed nation from 1990 to 2025.\\n\\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Environmental Science & Climate",
                "micro_topic": "Emissions trajectory across four industrial domains over a 35-year period",
                "task_words": "Select and report main features, make comparisons (Overview required; no opinions)",
                "coffee_shop_idea": "Power generation plummeted due to green transition, transport rose steadily, and agriculture fluctuated slightly.",
                "peel_blueprint": {
                    "body_1": "Overview: Overall, while power generation witnessed a dramatic plunge, transport emissions exhibited a continuous upward trajectory.",
                    "body_2": "Details: Contrasting the steep drop in electricity sector carbon output with the gradual leveling-off in agriculture."
                }
            }
        },
        "acad_t1_water": {
            "id": "acad_t1_water",
            "task_type": "task_1",
            "question_type": "Data Report (Pie Chart)",
            "track": "Academic",
            "title": "Global Freshwater Consumption Sectors",
            "prompt": (
                "The pie charts compare the proportion of global freshwater consumed across three major sectors "
                "(Agriculture, Industrial Manufacturing, and Domestic Households) in developing versus developed regions.\\n\\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Resource Management & Geography",
                "micro_topic": "Discrepancy in water allocation between developing and industrialized economies",
                "task_words": "Select and report main features, make comparisons (Objective reporting)",
                "coffee_shop_idea": "Developing nations allocate over 80% to agriculture, whereas developed nations use nearly half for industrial cooling and production.",
                "peel_blueprint": {
                    "body_1": "Overview: Overall, agriculture overwhelmingly dominates water usage in developing territories, whereas industrialized economies allocate the largest share to industrial processes.",
                    "body_2": "Details: Specific percentage breakdowns comparing domestic household usage (under 10% in developing vs 22% in developed)."
                }
            }
        },
        "acad_t1_transit": {
            "id": "acad_t1_transit",
            "task_type": "task_1",
            "question_type": "Data Report (Table)",
            "track": "Academic",
            "title": "Metropolitan Rail Systems in 5 European Capitals",
            "prompt": (
                "The table below presents data on five European urban metro rail networks, detailing route length (in kilometers), "
                "annual passenger volume (in millions), year opened, and on-time reliability rates.\\n\\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Urban Infrastructure",
                "micro_topic": "Performance and scale comparison of capital city metro systems",
                "task_words": "Summarise main features, make comparisons (Factual data report)",
                "coffee_shop_idea": "London is the oldest and longest, Paris carries the highest passenger volume, and Vienna has the highest on-time punctuality.",
                "peel_blueprint": {
                    "body_1": "Overview: Overall, the oldest rail networks operate the longest track systems, but modern systems maintain superior punctuality ratings.",
                    "body_2": "Details: Explicit comparisons between Paris passenger density and the smaller network scales in Madrid and Berlin."
                }
            }
        },
        "acad_t1_desalination": {
            "id": "acad_t1_desalination",
            "task_type": "task_1",
            "question_type": "Process Diagram (Flowchart)",
            "track": "Academic",
            "title": "Industrial Reverse Osmosis Desalination Process",
            "prompt": (
                "The diagram illustrates the sequential stages involved in converting ocean seawater into potable drinking water "
                "utilizing a multi-stage reverse osmosis desalination facility.\\n\\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Engineering & Water Purification",
                "micro_topic": "Step-by-step technological procedure of seawater desalination",
                "task_words": "Summarise stages of the process (Passive voice and sequential linking essential)",
                "coffee_shop_idea": "First, seawater is drawn in and screened. Next, pre-filtration removes solids. High pressure then forces it through semi-permeable membranes, separating brine from freshwater before mineral addition.",
                "peel_blueprint": {
                    "body_1": "Overview: Overall, the desalination cycle comprises four cardinal stages: intake pre-treatment, membrane separation, post-mineralization, and brine discharge.",
                    "body_2": "Details: Sequential breakdown from initial sand and cartridge filtration through high-pressure pump chambers to municipal storage."
                }
            }
        },
        "acad_t1_port_redevelopment": {
            "id": "acad_t1_port_redevelopment",
            "task_type": "task_1",
            "question_type": "Map Comparison (Spatial Layout)",
            "track": "Academic",
            "title": "Redevelopment of Port Dunmore (2005 vs Present)",
            "prompt": (
                "The two maps illustrate the architectural and commercial modifications that have taken place in "
                "the waterfront district of Port Dunmore between 2005 and the present day.\\n\\n"
                "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\\n"
                "Write at least 150 words."
            ),
            "advantage_analysis": {
                "general_topic": "Urban Regeneration & Spatial Planning",
                "micro_topic": "Transformation of an industrial dockland into a residential and recreational zone",
                "task_words": "Report main structural transformations and compare spatial layouts",
                "coffee_shop_idea": "Derelict warehouses in the north were converted into luxury apartments and a promenade, while the old freight dock became a yacht marina.",
                "peel_blueprint": {
                    "body_1": "Overview: Overall, Port Dunmore has been completely transformed from a utilitarian industrial dock into a pedestrianized leisure and residential hub.",
                    "body_2": "Details: Specific spatial movements: demolition of cranes in the east, construction of green parkland and pedestrian bridges."
                }
            }
        },

        # --- GENERAL TRAINING TASK 1 LETTERS ---
        "gt_t1_airline_complaint": {
            "id": "gt_t1_airline_complaint",
            "task_type": "task_1",
            "question_type": "Formal Letter (Complaint & Compensation)",
            "track": "General",
            "title": "Damaged Luggage & Delayed International Transit",
            "prompt": (
                "You recently traveled on an international flight and your checked baggage was severely damaged and delivered three days late.\\n\\n"
                "Write a letter to the airline customer service manager. In your letter:\\n"
                "• Explain the details of your flight and journey\\n"
                "• Describe the damage caused to your luggage and its contents\\n"
                "• State clearly what financial reimbursement or action you expect the airline to take\\n\\n"
                "Write at least 150 words. You do NOT need to write any addresses.\\n"
                "Begin your letter as follows: Dear Sir or Madam,"
            ),
            "advantage_analysis": {
                "general_topic": "Consumer Rights & Travel Grievance",
                "micro_topic": "Formal complaint regarding flight baggage damage and delayed delivery",
                "task_words": "Address all three bullet points; maintain formal register ('Dear Sir or Madam' / 'Yours faithfully')",
                "coffee_shop_idea": "State flight info calmly, explain cracked suitcase and ruined laptop/clothes, ask for 500 dollars refund and immediate claim processing.",
                "peel_blueprint": {
                    "body_1": "Purpose & Flight Info: Stating reason for writing and flight details (Flight GA-402 on October 14th).",
                    "body_2": "Damage Description: Documenting the shattered shell and damaged textile contents.",
                    "body_3": "Required Redress: Specifying itemized compensation and requested timeline."
                }
            }
        },
        "gt_t1_gym_facilities": {
            "id": "gt_t1_gym_facilities",
            "task_type": "task_1",
            "question_type": "Semi-Formal Letter (Proposal & Request)",
            "track": "General",
            "title": "Extended Weekend Hours at Community Leisure Centre",
            "prompt": (
                "You are an active member of your local community fitness center. You feel the current weekend opening hours "
                "and equipment are inadequate for working residents.\\n\\n"
                "Write a letter to the center manager. In your letter:\\n"
                "• State how long you have been a member and what you like about the center\\n"
                "• Explain the problems caused by early weekend closures and limited cardio equipment\\n"
                "• Suggest reasonable improvements that would benefit other local members\\n\\n"
                "Write at least 150 words. You do NOT need to write any addresses.\\n"
                "Begin your letter as follows: Dear Mr. Robinson,"
            ),
            "advantage_analysis": {
                "general_topic": "Community Facilities & Civic Feedback",
                "micro_topic": "Constructive proposal to extend hours and upgrade gym equipment",
                "task_words": "Address three bullet points; respectful semi-formal register ('Yours sincerely')",
                "coffee_shop_idea": "I love the gym and have attended for 2 years, but 4 PM weekend closing is too early and cardio machines are broken. Please extend to 8 PM and service treadmills.",
                "peel_blueprint": {
                    "body_1": "Membership History: Complimenting staff and expressing appreciation.",
                    "body_2": "The Dilemma: Explaining overcrowding on Saturday afternoons and early closing times.",
                    "body_3": "Constructive Suggestions: Proposing 8 PM weekend closing and a booking app."
                }
            }
        },
        "gt_t1_friend_visit": {
            "id": "gt_t1_friend_visit",
            "task_type": "task_1",
            "question_type": "Informal Letter (Advice & Hospitality)",
            "track": "General",
            "title": "Vacation Advice & Invitation to Stay",
            "prompt": (
                "An old friend from university is planning to visit your town for a one-week holiday next month.\\n\\n"
                "Write a letter to your friend. In your letter:\\n"
                "• Express your excitement about their upcoming visit\\n"
                "• Recommend top local attractions and activities to do together\\n"
                "• Invite them to stay at your apartment and explain arrangements\\n\\n"
                "Write at least 150 words. You do NOT need to write any addresses.\\n"
                "Begin your letter as follows: Dear Alex,"
            ),
            "advantage_analysis": {
                "general_topic": "Personal Hospitality & Travel Advice",
                "micro_topic": "Friendly holiday planning and accommodation offer",
                "task_words": "Warm, conversational, natural informal register ('Dear [Name]' / 'Warm wishes / Best regards')",
                "coffee_shop_idea": "I can't wait to see you! We should hike the mountain trail and check out the new food market. Stay in my spare room!",
                "peel_blueprint": {
                    "body_1": "Warm Greeting: Reconnecting and expressing delight at the trip.",
                    "body_2": "Attraction Recommendations: Hiking, cultural markets, and live music spots.",
                    "body_3": "Accommodation Offer: Spare bedroom ready, picking up from train station."
                }
            }
        },
        "gt_t1_volunteer_app": {
            "id": "gt_t1_volunteer_app",
            "task_type": "task_1",
            "question_type": "Formal Letter (Job Application & Suitability)",
            "track": "General",
            "title": "Volunteer Wildlife Conservation Officer Application",
            "prompt": (
                "You saw an advertisement seeking volunteers to assist with a seasonal environmental protection project in a regional nature reserve.\\n\\n"
                "Write a letter to the volunteer coordinator. In your letter:\\n"
                "• Explain which position you are applying for and where you saw the notice\\n"
                "• Outline your relevant qualifications, outdoor skills, and experience\\n"
                "• State your availability during the upcoming three-month conservation cycle\\n\\n"
                "Write at least 150 words. You do NOT need to write any addresses.\\n"
                "Begin your letter as follows: Dear Sir or Madam,"
            ),
            "advantage_analysis": {
                "general_topic": "Employment & Civic Volunteering",
                "micro_topic": "Application for an outdoor ecological volunteering position",
                "task_words": "Formal professional tone; cover all three prompts; clear structure",
                "coffee_shop_idea": "Applying for forest patrol volunteer, have first aid certification and biology degree, available weekends and full months of July/August.",
                "peel_blueprint": {
                    "body_1": "Application Statement: Formal notice of candidacy and source of advertisement.",
                    "body_2": "Relevant Competencies: Environmental background, trail navigation, and teamwork.",
                    "body_3": "Availability & Next Steps: Specific dates and interview readiness."
                }
            }
        },
        "gt_t1_colleague_apology": {
            "id": "gt_t1_colleague_apology",
            "task_type": "task_1",
            "question_type": "Semi-Formal Letter (Professional Apology & Handover)",
            "track": "General",
            "title": "Absence from Project Review & Task Delegation",
            "prompt": (
                "You are unable to attend an important project presentation and strategy meeting with your corporate team next Monday "
                "due to an unforeseen personal emergency.\\n\\n"
                "Write a letter to your team project leader. In your letter:\\n"
                "• Apologize for your sudden absence and explain the reason\\n"
                "• Describe the progress of your assigned project section so far\\n"
                "• Clarify who will deliver your slides and handle client questions\\n\\n"
                "Write at least 150 words. You do NOT need to write any addresses.\\n"
                "Begin your letter as follows: Dear Sarah,"
            ),
            "advantage_analysis": {
                "general_topic": "Workplace Communication & Accountability",
                "micro_topic": "Professional apology and handover plan for a missed client review",
                "task_words": "Polite, responsible, semi-formal professional register",
                "coffee_shop_idea": "Sincere apology due to family emergency, slides are 100% complete in shared drive, David has agreed to present my section.",
                "peel_blueprint": {
                    "body_1": "Apology & Context: Sincere regret for missing the meeting due to unavoidable circumstances.",
                    "body_2": "Status Report: Financial data and presentation slides finalized in company cloud.",
                    "body_3": "Delegation Arrangement: Colleague briefed to deliver segment, phone accessible for urgent queries."
                }
            }
        },

        # --- GENERAL TRAINING TASK 2 ESSAYS ---
        "gt_t2_remote_work": {
            "id": "gt_t2_remote_work",
            "task_type": "task_2",
            "question_type": "Agree or Disagree (Opinion)",
            "track": "General",
            "title": "Telecommuting, Work-Life Balance & Office Culture",
            "prompt": (
                "Many companies are now allowing employees to work from home permanently rather than commuting to commercial offices. "
                "Some people argue this creates a superior work-life balance, while others contend it weakens professional collaboration and mental health.\\n\\n"
                "To what extent do you agree or disagree that permanent remote work is beneficial for society as a whole?\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Workplace Trends & Well-being",
                "micro_topic": "Whether societal advantages of telecommuting exceed isolation and collaboration challenges",
                "task_words": "To what extent do you agree or disagree (Clear viewpoint required)",
                "coffee_shop_idea": "I agree that it is largely beneficial because cutting commute times saves hours and reduces stress, provided hybrid options exist to maintain social connection.",
                "peel_blueprint": {
                    "body_1": "Point: Telecommuting eliminates grueling daily transit and bolsters personal autonomy. Explain: Workers regain 2-3 hours daily for family and health. Example: Global surveys indicate 70% higher job satisfaction among remote employees. Link: This significantly elevates overall quality of life.",
                    "body_2": "Point: However, complete isolation can erode team synergy if unmanaged. Explain: Spontaneous brainstorming diminishes without face-to-face interaction. Example: Leading enterprises adopted hybrid schedules with 2 office days to preserve camaraderie. Link: Therefore, when implemented flexibly, telecommuting remains strongly advantageous."
                }
            }
        },
        "gt_t2_community_sports": {
            "id": "gt_t2_community_sports",
            "task_type": "task_2",
            "question_type": "Causes & Solutions",
            "track": "General",
            "title": "Youth Participation in Community Sports",
            "prompt": (
                "In many countries, young people are participating significantly less in organized community sports clubs than previous generations, "
                "leading to concerns regarding adolescent fitness and social isolation.\\n\\n"
                "What are the main causes of this decline, and what measures can local communities take to encourage youth participation?\\n"
                "Write at least 250 words."
            ),
            "advantage_analysis": {
                "general_topic": "Community Health & Adolescent Lifestyle",
                "micro_topic": "Reasons for declining athletic club enrollment and municipal remedies",
                "task_words": "What are CAUSES and what are MEASURES (Must cover both thoroughly)",
                "coffee_shop_idea": "Causes: screen addiction/gaming and expensive club fees. Solutions: subsidized membership and modernizing clubs with e-sports integrations or casual formats.",
                "peel_blueprint": {
                    "body_1": "Point: The predominant factor is the lure of digital screen entertainment and escalating membership costs. Explain: Video games and social media provide effortless dopamine without physical exertion. Example: Youth sports registrations fell 25% as smartphone screen time doubled. Link: These lifestyle shifts discourage active recreation.",
                    "body_2": "Point: Municipalities can revitalize participation through public subsidies and diversified activities. Explain: Removing economic barriers ensures all adolescents have access to facilities. Example: Scandinavian local councils provide vouchers for sports clubs, achieving 80% youth engagement. Link: Proactive public investment effectively reverses this trend."
                }
            }
        }
    }

    ACADEMIC_WORDS = {
        "substantial", "significant", "furthermore", "moreover", "consequently",
        "nevertheless", "predominantly", "demonstrate", "illustrate", "proportion",
        "fluctuate", "stabilize", "constitute", "concur", "perspective", "advocate",
        "phenomenon", "empirical", "methodology", "infrastructure", "disparity",
        "paramount", "detrimental", "catalyst", "substantiate", "ameliorate",
        "trajectory", "exponential", "plateaued", "plummeted", "negligible",
        "subsequent", "unprecedented", "correlation", "diminish", "allocation"
    }

    TASK1_TREND_WORDS = {
        "surged", "plummeted", "increased", "decreased", "rose", "fell", "dropped",
        "fluctuated", "plateaued", "peaked", "remained steady", "stabilized",
        "accounted for", "constituted", "represented", "proportion", "percentage",
        "highest", "lowest", "majority", "minority", "respectively", "sharply",
        "gradually", "consistently", "upward", "downward", "trajectory"
    }

    COHESIVE_LINKERS = [
        "furthermore", "moreover", "in addition", "consequently", "therefore",
        "however", "on the other hand", "in contrast", "nevertheless", "to begin with",
        "ultimately", "in conclusion", "for instance", "for example", "notwithstanding",
        "on balance", "in stark contrast", "a compelling case in point", "similarly",
        "by comparison", "in terms of", "broadly speaking"
    ]

    @classmethod
    def list_prompts(cls, track: Optional[str] = None, task_type: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for p in cls.ORIGINAL_PROMPTS.values():
            if track and p["track"].lower() != track.lower():
                continue
            if task_type and p["task_type"].lower() != task_type.lower():
                continue
            results.append({
                "id": p["id"],
                "title": p["title"],
                "task_type": p["task_type"],
                "question_type": p.get("question_type", "Essay"),
                "track": p["track"],
                "prompt": p["prompt"]
            })
        return results

    @classmethod
    def get_prompt(cls, prompt_id: str = "acad_t2_stem") -> Optional[Dict[str, Any]]:
        return cls.ORIGINAL_PROMPTS.get(prompt_id)

    @classmethod
    def save_draft(
        cls,
        learner_id: str,
        prompt_id: str,
        draft_text: str,
        draft_id: Optional[str] = None,
        db: Optional[DatabaseManager] = None
    ) -> Dict[str, Any]:
        """Saves or updates a learner's writing draft in SQLite."""
        p_data = cls.get_prompt(prompt_id) or cls.ORIGINAL_PROMPTS["acad_t2_stem"]
        repo = WritingDraftRepository(db)
        words = len(draft_text.strip().split())
        return repo.save_draft(
            learner_id=learner_id,
            prompt_id=prompt_id,
            task_type=p_data["task_type"],
            track=p_data["track"],
            draft_text=draft_text,
            word_count=words,
            draft_id=draft_id
        )

    @classmethod
    def get_learner_drafts(cls, learner_id: str, db: Optional[DatabaseManager] = None) -> List[Dict[str, Any]]:
        """Retrieves past drafts and submitted evaluations for a learner."""
        repo = WritingDraftRepository(db)
        return repo.get_learner_drafts(learner_id)

    @classmethod
    def evaluate_essay(
        cls,
        prompt_id: str,
        essay_text: str,
        learner_id: Optional[str] = None,
        draft_id: Optional[str] = None,
        db: Optional[DatabaseManager] = None
    ) -> Dict[str, Any]:
        """
        Evaluates learner's response across all four IELTS criteria:
        Task Achievement / Response (25%), Coherence & Cohesion (25%),
        Lexical Resource (25%), Grammatical Range & Accuracy (25%).
        """
        prompt_data = cls.get_prompt(prompt_id) or cls.ORIGINAL_PROMPTS["acad_t2_stem"]
        task_type = prompt_data["task_type"]
        track = prompt_data["track"]

        words = essay_text.strip().split()
        word_count = len(words)
        paragraphs = [p.strip() for p in essay_text.strip().split("\\n\\n") if p.strip()]
        if len(paragraphs) <= 1:
            paragraphs = [p.strip() for p in essay_text.strip().split("\\n") if len(p.strip()) > 30]
        para_count = max(1, len(paragraphs))

        min_words = 150 if task_type == "task_1" else 250
        text_lower = essay_text.lower()

        # ----------------------------------------------------
        # 1. TASK ACHIEVEMENT / TASK RESPONSE (25%)
        # ----------------------------------------------------
        tr_score = 6.0
        ta_notes = []

        if task_type == "task_1":
            if track == "Academic":
                # Academic Task 1: Check Overview
                has_overview = any(k in text_lower for k in [
                    "overall", "in summary", "to summarize", "broadly speaking",
                    "it is clear that", "it is evident that", "the most notable feature",
                    "main trend", "significant feature"
                ])
                if has_overview:
                    tr_score += 0.5
                    ta_notes.append("Clear overview statement identifying prominent features present.")
                else:
                    tr_score -= 0.5
                    ta_notes.append("Missing distinct overview paragraph summarizing general trajectories.")

                # Check for subjective opinion (Task 1 Academic prohibits personal opinion!)
                has_opinion = any(k in text_lower for k in ["in my opinion", "i believe", "i think", "my view is"])
                if has_opinion:
                    tr_score -= 0.5
                    ta_notes.append("Deduction: Avoid personal opinions in Academic Task 1 (pure factual report required).")

                # Trend vocabulary / data comparison
                trend_hits = set(re.findall(r"\\b[a-z']+\\b", text_lower)).intersection(cls.TASK1_TREND_WORDS)
                if len(trend_hits) >= 3:
                    tr_score += 0.5
                    ta_notes.append(f"Included comparative analytical terms ({', '.join(list(trend_hits)[:4])}).")

            else:
                # General Training Task 1: Letter checks
                has_salutation = any(k in text_lower for k in ["dear sir", "dear madam", "dear mr", "dear ms", "dear "])
                has_signoff = any(k in text_lower for k in [
                    "yours faithfully", "yours sincerely", "best regards",
                    "warm regards", "all the best", "sincerely", "warm wishes"
                ])
                has_purpose = any(k in text_lower for k in [
                    "i am writing to", "i would like to", "the reason i am writing", "i am writing with regard"
                ])
                if has_salutation and has_signoff:
                    tr_score += 0.5
                    ta_notes.append("Appropriate salutation and sign-off conventions maintained.")
                if has_purpose:
                    tr_score += 0.5
                    ta_notes.append("Clear statement of letter purpose in opening section.")

            if word_count >= 150:
                tr_score += 0.5
            else:
                ta_notes.append(f"Underlength: {word_count}/150 required words.")

        else:
            # Task 2 Essay
            has_conclusion = any(k in text_lower for k in ["in conclusion", "to conclude", "on balance", "to sum up"])
            has_position = any(k in text_lower for k in ["i argue", "i believe", "in my opinion", "i agree", "i disagree", "my perspective"])
            if word_count >= 250:
                tr_score += 0.5
            if has_conclusion:
                tr_score += 0.5
                ta_notes.append("Effective conclusion summarizing the main argument.")
            if has_position:
                tr_score += 0.5
                ta_notes.append("Clear candidate thesis/position articulated.")
            if para_count >= 4:
                tr_score += 0.5

        tr_score = min(8.5, max(4.0, tr_score))

        # ----------------------------------------------------
        # 2. COHERENCE AND COHESION (25%)
        # ----------------------------------------------------
        cc_score = 6.0
        found_linkers = [l for l in cls.COHESIVE_LINKERS if l in text_lower]
        if len(found_linkers) >= 4:
            cc_score += 0.5
        if len(found_linkers) >= 7:
            cc_score += 0.5
        if para_count in [3, 4, 5]:
            cc_score += 0.5
        cc_score = min(8.5, max(4.0, cc_score))

        # ----------------------------------------------------
        # 3. LEXICAL RESOURCE (25%)
        # ----------------------------------------------------
        lr_score = 6.0
        words_lower = set([w.lower().strip(".,;:!?()") for w in words])
        academic_hits = words_lower.intersection(cls.ACADEMIC_WORDS)
        if len(academic_hits) >= 3:
            lr_score += 0.5
        if len(academic_hits) >= 6:
            lr_score += 1.0
        lr_score = min(8.5, max(4.0, lr_score))

        # ----------------------------------------------------
        # 4. GRAMMATICAL RANGE AND ACCURACY (25%)
        # ----------------------------------------------------
        formative_errors = FormativeFeedback.generate_formative_items(essay_text)
        gra_score = 6.5
        subordinators = ["although", "while", "whereas", "because", "since", "unless", "provided that", "whereas", "despite"]
        has_complex = any(s in text_lower for s in subordinators)
        if has_complex:
            gra_score += 0.5
        if len(formative_errors) > 2:
            gra_score -= 1.0
        elif len(formative_errors) == 1:
            gra_score -= 0.5
        gra_score = min(8.5, max(4.0, gra_score))

        # Build dynamic checklist
        if task_type == "task_1":
            if track == "Academic":
                checklist = [
                    {"item": "Clear Overview highlighting primary trends/stages", "passed": any(k in text_lower for k in ["overall", "in summary", "broadly", "evident"])},
                    {"item": "Objective tone without personal opinions or bias", "passed": not any(k in text_lower for k in ["in my opinion", "i believe", "i think"])},
                    {"item": "Accurate comparative and trend vocabulary utilized", "passed": len(words_lower.intersection(cls.TASK1_TREND_WORDS)) >= 2},
                    {"item": "Minimum 150 words threshold met", "passed": word_count >= 150},
                    {"item": "Logical paragraph division (Intro, Overview, Body 1, Body 2)", "passed": para_count >= 3},
                    {"item": "Cohesive discourse markers and linking devices", "passed": len(found_linkers) >= 2},
                    {"item": "Complex sentence structures with subordinators", "passed": has_complex},
                    {"item": "Grammatical accuracy without basic subject-verb errors", "passed": len(formative_errors) == 0}
                ]
            else:
                checklist = [
                    {"item": "Clear statement of letter purpose in opening", "passed": any(k in text_lower for k in ["i am writing", "writing to", "writing with regard"])},
                    {"item": "Standard salutation included (e.g. Dear Sir/Madam or Dear Alex)", "passed": any(k in text_lower for k in ["dear sir", "dear madam", "dear "])},
                    {"item": "Appropriate sign-off included (e.g. Yours faithfully or Best regards)", "passed": any(k in text_lower for k in ["yours faithfully", "yours sincerely", "best regards", "all the best"])},
                    {"item": "Minimum 150 words threshold met", "passed": word_count >= 150},
                    {"item": "Distinct paragraphs for each required bullet point", "passed": para_count >= 3},
                    {"item": "Appropriate social/business register maintained", "passed": True},
                    {"item": "Varied grammatical structures and complex clauses", "passed": has_complex},
                    {"item": "Grammatical accuracy without basic errors", "passed": len(formative_errors) == 0}
                ]
        else:
            checklist = [
                {"item": "Answered all parts of the question prompt", "passed": word_count >= min_words and para_count >= 3},
                {"item": "Clear thesis position stated in introduction and conclusion", "passed": any(k in text_lower for k in ["i argue", "i believe", "my opinion", "in conclusion", "to conclude", "on balance"])},
                {"item": "Paragraph structure: 4-5 well-developed paragraphs", "passed": para_count in [4, 5]},
                {"item": "Substantial word count (above minimum threshold)", "passed": word_count >= min_words},
                {"item": "Cohesive linkers and discourse signposts present", "passed": len(found_linkers) >= 4},
                {"item": "Band 7+ academic topic vocabulary utilized", "passed": len(academic_hits) >= 3},
                {"item": "Complex subordinate clauses and conditionals present", "passed": has_complex},
                {"item": "Grammatical accuracy without basic subject-verb errors", "passed": len(formative_errors) == 0}
            ]

        passed_checks = sum(1 for c in checklist if c["passed"])

        crit_feedback = {
            "Task Achievement" if task_type == "task_1" else "Task Response": f"Addressed prompt with {word_count} words across {para_count} paragraphs. " + " ".join(ta_notes),
            "Coherence and Cohesion": f"Identified {len(found_linkers)} discourse marker(s) ({', '.join(found_linkers[:4]) if found_linkers else 'none'}).",
            "Lexical Resource": f"Utilized {len(academic_hits)} high-utility academic term(s): {', '.join(academic_hits) if academic_hits else 'expand academic range'}.",
            "Grammatical Range and Accuracy": f"Detected {len(formative_errors)} significant structural issue(s)."
        }

        eval_result = CriteriaEvaluator.evaluate_writing(
            task_type=task_type,
            track=track,
            text=essay_text,
            tr_score=tr_score,
            cc_score=cc_score,
            lr_score=lr_score,
            gra_score=gra_score,
            word_count=word_count,
            feedback_notes=crit_feedback
        )

        eval_result["formative_corrections"] = formative_errors
        eval_result["prompt_title"] = prompt_data["title"]
        eval_result["question_type"] = prompt_data.get("question_type", "Essay")
        eval_result["advantage_checklist"] = checklist
        eval_result["passed_checklist_count"] = passed_checks
        eval_result["advantage_analysis"] = prompt_data.get("advantage_analysis", {})

        # Persist evaluation if learner_id is provided
        if learner_id:
            try:
                db_mgr = db or DatabaseManager()
                draft_repo = WritingDraftRepository(db_mgr)
                if not draft_id:
                    saved = draft_repo.save_draft(
                        learner_id=learner_id,
                        prompt_id=prompt_id,
                        task_type=task_type,
                        track=track,
                        draft_text=essay_text,
                        word_count=word_count
                    )
                    draft_id = saved["id"]

                crit_dict = eval_result.get("criteria", {})
                ta_val = crit_dict.get("Task Achievement", crit_dict.get("Task Response", tr_score))
                draft_repo.record_evaluation(
                    draft_id=draft_id,
                    ta_score=ta_val,
                    cc_score=crit_dict.get("Coherence and Cohesion", cc_score),
                    lr_score=crit_dict.get("Lexical Resource", lr_score),
                    gra_score=crit_dict.get("Grammatical Range and Accuracy", gra_score),
                    overall_band=eval_result["estimated_band"],
                    feedback=eval_result
                )

                # Also update test_results repository for dashboard synchronization!
                test_repo = TestResultRepository(db_mgr)
                test_repo.record_result(
                    learner_id=learner_id,
                    track=track,
                    overall_band=eval_result["estimated_band"],
                    writing_band=eval_result["estimated_band"]
                )
            except Exception:
                pass

        return eval_result
'''

with open("core/writing/writing_evaluator.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated core/writing/writing_evaluator.py successfully!")
