"""
Grammar Engine for IELTS by GAMA.
Covers 24 foundational English grammar categories, diagnoses common errors,
and formats formative feedback following the 'Teach Through Correction' paradigm:
ORIGINAL -> CORRECTION -> WHY -> BETTER ALTERNATIVE -> PRACTICE EXERCISE.
Includes interactive Grammar Fill-Up (Cloze) drills and sentence architecture drills.
"""

import re
from typing import Dict, Any, List, Optional


class GrammarEngine:
    """Diagnoses grammatical errors and teaches underlying linguistic mechanics."""

    # 24 core grammatical syllabus areas
    TOPICS = [
        "Parts of Speech", "Articles", "Tenses", "Subject-Verb Agreement",
        "Pronouns", "Prepositions", "Modal Verbs", "Conditionals",
        "Passive Voice", "Reported Speech", "Relative Clauses", "Gerunds & Infinitives",
        "Comparatives & Superlatives", "Question Formation", "Word Order", "Determiners & Quantifiers",
        "Adverbial Clauses", "Complex Sentences", "Compound Sentences", "Punctuation",
        "Parallel Structure", "Inversion", "Subjunctive & Unreal Past", "Cohesive Linkers"
    ]

    # Heuristic diagnostic patterns across all 24 grammatical categories
    ERROR_RULES = [
        {
            "pattern": r"\b(i|we|they|you)\s+am\s+agree\b",
            "category": "Subject-Verb Agreement",
            "correction_sub": r"\1 agree",
            "why": "'Agree' is an action verb in English and does not use the auxiliary 'am' in the simple present tense.",
            "better_alternative": "I strongly concur with this perspective.",
            "exercise": "Fill in the blank: 'Many economists _____ (agree / are agree) with this forecast.' (Answer: agree)"
        },
        {
            "pattern": r"\ba\s+information\b",
            "category": "Articles",
            "correction_sub": "information (or 'a piece of information')",
            "why": "'Information' is an uncountable noun and cannot be preceded by the indefinite article 'a'.",
            "better_alternative": "a crucial piece of evidence / empirical data",
            "exercise": "Correct this phrase: 'He gave me a good advice.' -> 'He gave me _____ (good advice / a good advice)' (Answer: good advice)"
        },
        {
            "pattern": r"\b(each|every)\s+of\s+the\s+students\s+are\b",
            "category": "Subject-Verb Agreement",
            "correction_sub": r"\1 of the students is",
            "why": "'Each' and 'every' take a singular verb when acting as the head subject.",
            "better_alternative": "Every participant exhibits...",
            "exercise": "Choose the correct verb: 'Each of the experiments _____ (was / were) conclusive.' (Answer: was)"
        },
        {
            "pattern": r"\bmore\s+easier\b",
            "category": "Comparatives & Superlatives",
            "correction_sub": "easier",
            "why": "Two comparative markers ('more' and '-er') cannot be applied to the same adjective.",
            "better_alternative": "considerably more straightforward",
            "exercise": "Correct: 'This method is more faster.' -> 'This method is _____.' (Answer: faster)"
        },
        {
            "pattern": r"\bdiscuss\s+about\b",
            "category": "Prepositions",
            "correction_sub": "discuss",
            "why": "'Discuss' is a transitive verb that takes a direct object without the preposition 'about'.",
            "better_alternative": "deliberate on / explore the nuances of",
            "exercise": "Correct: 'We need to discuss about the budget.' -> 'We need to discuss _____.' (Answer: the budget)"
        },
        {
            "pattern": r"\bdespite\s+of\b",
            "category": "Prepositions",
            "correction_sub": "despite (or 'in spite of')",
            "why": "'Despite' is a preposition used without 'of'. 'In spite of' requires 'of'.",
            "better_alternative": "notwithstanding / despite the prevailing challenges",
            "exercise": "Choose: '_____ (Despite / In spite) of the rainfall, the match continued.' (Answer: In spite)"
        },
        {
            "pattern": r"\bresponsible\s+of\b",
            "category": "Prepositions",
            "correction_sub": "responsible for",
            "why": "The adjective 'responsible' takes the dependent preposition 'for' when indicating duty or cause.",
            "better_alternative": "held accountable for / tasked with overseeing",
            "exercise": "Fill in the preposition: 'Governments are responsible _____ public health.' (Answer: for)"
        },
        {
            "pattern": r"\bdid\s+not\s+(went|saw|ate|wrote|took)\b",
            "category": "Tenses",
            "correction_sub": "did not go/see/eat/write/take",
            "why": "The auxiliary 'did not' must always be paired with the base (bare infinitive) form of the verb.",
            "better_alternative": "failed to observe / did not undertake",
            "exercise": "Correct: 'She did not went.' -> 'She did not _____.' (Answer: go)"
        },
        {
            "pattern": r"\bhave\s+(saw|went|did|took)\b",
            "category": "Tenses",
            "correction_sub": "have seen/gone/done/taken",
            "why": "Present Perfect requires 'have/has' + the past participle, not the past simple form.",
            "better_alternative": "have witnessed / have participated in",
            "exercise": "Fill in the past participle: 'Scientists have _____ (see / saw / seen) unprecedented warming.' (Answer: seen)"
        },
        {
            "pattern": r"\bsince\s+(\d+|\w+)\s+(years|months|days|weeks|hours)\b",
            "category": "Tenses",
            "correction_sub": r"for \1 \2",
            "why": "Use 'for' with a duration of time and 'since' with a specific starting point in the past.",
            "better_alternative": "over the preceding decade / for a duration of three years",
            "exercise": "Choose: 'He has worked here _____ (for / since) five years.' (Answer: for)"
        },
        {
            "pattern": r"\bbetween\s+you\s+and\s+i\b",
            "category": "Pronouns",
            "correction_sub": "between you and me",
            "why": "'Between' is a preposition and requires object pronouns ('me', 'him', 'them').",
            "better_alternative": "confidentially / between ourselves",
            "exercise": "Choose: 'Between you and _____ (I / me), the proposal is weak.' (Answer: me)"
        },
        {
            "pattern": r"\blook\s+forward\s+to\s+hear\b",
            "category": "Gerunds & Infinitives",
            "correction_sub": "look forward to hearing",
            "why": "In 'look forward to', 'to' is a preposition, so it must be followed by a gerund (-ing).",
            "better_alternative": "anticipate receiving your correspondence",
            "exercise": "Correct: 'I look forward to _____ (meet / meeting) you.' (Answer: meeting)"
        },
        {
            "pattern": r"\bcapable\s+to\s+(\w+)\b",
            "category": "Gerunds & Infinitives",
            "correction_sub": r"capable of \1ing",
            "why": "The adjective 'capable' takes the preposition 'of' followed by a gerund, not an infinitive with 'to'.",
            "better_alternative": "equipped with the capacity to",
            "exercise": "Correct: 'He is capable to solve this.' -> 'He is capable _____ this.' (Answer: of solving)"
        },
        {
            "pattern": r"\bmuch\s+(people|students|children|countries|problems)\b",
            "category": "Determiners & Quantifiers",
            "correction_sub": r"many \1",
            "why": "'Much' is used with uncountable nouns; countable plural nouns require 'many' or 'a significant number of'.",
            "better_alternative": "a substantial proportion of individuals",
            "exercise": "Choose: '_____ (Much / Many) students commute by train.' (Answer: Many)"
        },
        {
            "pattern": r"\bless\s+(people|students|children|cars|books)\b",
            "category": "Determiners & Quantifiers",
            "correction_sub": r"fewer \1",
            "why": "Use 'fewer' with countable plural nouns and 'less' with singular uncountable nouns.",
            "better_alternative": "a reduced volume of traffic / fewer motorists",
            "exercise": "Choose: 'There are _____ (less / fewer) errors in this draft.' (Answer: fewer)"
        },
        {
            "pattern": r"\bon\s+the\s+other\s+side\b",
            "category": "Cohesive Linkers",
            "correction_sub": "on the other hand (or 'conversely')",
            "why": "The standard English transitional idiom for contrasting viewpoints is 'on the other hand'.",
            "better_alternative": "conversely / in stark contrast",
            "exercise": "Complete: 'On the one hand... on the other _____.' (Answer: hand)"
        },
        {
            "pattern": r"\bthe\s+reason\s+why\s+is\s+because\b",
            "category": "Complex Sentences",
            "correction_sub": "the reason is that",
            "why": "'Reason why... because' is redundant; use 'the reason is that...'.",
            "better_alternative": "this discrepancy stems primarily from the fact that",
            "exercise": "Correct: 'The reason why is because it rained.' -> 'The reason is _____ it rained.' (Answer: that)"
        },
        {
            "pattern": r"\bwhich\s+it\s+(is|was|has|can|will)\b",
            "category": "Relative Clauses",
            "correction_sub": r"which \1",
            "why": "In a relative clause where 'which' is the subject, the pronoun 'it' is an ungrammatical double subject.",
            "better_alternative": "a phenomenon which signifies...",
            "exercise": "Correct: 'The report, which it was published yesterday...' -> 'The report, which _____ published yesterday...' (Answer: was)"
        },
        {
            "pattern": r"\bhe\s+asked\s+me\s+where\s+(was\s+i|did\s+i\s+go)\b",
            "category": "Reported Speech",
            "correction_sub": "where I was / where I went",
            "why": "Indirect questions and reported speech use affirmative statement word order (Subject + Verb), not inverted question order.",
            "better_alternative": "inquired regarding my location",
            "exercise": "Correct: 'She asked what was my name.' -> 'She asked what my name _____.' (Answer: was)"
        },
        {
            "pattern": r"\bif\s+i\s+would\s+have\b",
            "category": "Conditionals",
            "correction_sub": "if I had",
            "why": "Do not put 'would have' inside the conditional if-clause; use the past perfect 'had + past participle'.",
            "better_alternative": "had retrospective analysis been conducted",
            "exercise": "Correct: 'If I would have known...' -> 'If I _____ known...' (Answer: had)"
        },
        {
            "pattern": r"\bit\s+is\s+essential\s+that\s+he\s+(goes|studies|takes)\b",
            "category": "Subjunctive & Unreal Past",
            "correction_sub": "go/study/take",
            "why": "The mandative subjunctive following adjectives like 'essential/vital/crucial' uses the bare base verb for all persons.",
            "better_alternative": "it is imperative that he undergo...",
            "exercise": "Fill in the base form: 'It is vital that she _____ (attend / attends) the briefing.' (Answer: attend)"
        },
        {
            "pattern": r"\b(firstly|secondly|lastly),?\s+and\s+most\s+importantly\b",
            "category": "Punctuation",
            "correction_sub": "first and foremost (or 'principally')",
            "why": "Overloading informal ordinal adverbs weakens academic tone.",
            "better_alternative": "paramount among these factors is...",
            "exercise": "Choose an elevated academic alternative: '_____ (Firstly / Primarily), renewable energy reduces carbon output.' (Answer: Primarily)"
        },
        {
            "pattern": r"\blacks\s+of\b",
            "category": "Parts of Speech",
            "correction_sub": "lacks (verb) / lack of (noun)",
            "why": "The verb 'to lack' is transitive and does not take 'of'. The noun 'lack' is followed by 'of'.",
            "better_alternative": "is deficient in / exhibits an absence of",
            "exercise": "Correct: 'The country lacks of clean water.' -> 'The country lacks _____ clean water.' (Answer: [blank] or 'lacks')"
        },
        {
            "pattern": r"\badvices\b",
            "category": "Articles",
            "correction_sub": "advice (or 'pieces of advice')",
            "why": "'Advice' is strictly uncountable and cannot be made plural with '-s'.",
            "better_alternative": "counsel / strategic guidance",
            "exercise": "Correct: 'He offered three advices.' -> 'He offered three pieces of _____.' (Answer: advice)"
        },
        {
            "pattern": r"\bequipments\b",
            "category": "Articles",
            "correction_sub": "equipment (or 'pieces of equipment')",
            "why": "'Equipment' is an uncountable mass noun in English and never takes an '-s'.",
            "better_alternative": "apparatus / specialized instrumentation",
            "exercise": "Correct: 'Modern laboratory equipments.' -> 'Modern laboratory _____.' (Answer: equipment)"
        }
    ]

    FILL_UP_DRILLS = [
        {
            "id": "fill_cond_1",
            "category": "Conditionals",
            "prompt": "If municipal authorities _____ (invest) in efficient light rail a decade ago, traffic congestion would not be so acute today.",
            "acceptable": ["had invested"],
            "explanation": "Mixed conditional: Past condition ('had invested') producing a present result ('would not be so acute').",
            "band_note": "Mixed conditionals demonstrate Band 8+ Grammatical Range and Accuracy."
        },
        {
            "id": "fill_cond_2",
            "category": "Conditionals",
            "prompt": "If the government were to raise carbon taxes, corporations _____ (seek) cleaner manufacturing alternatives.",
            "acceptable": ["would seek"],
            "explanation": "Second conditional (unreal/hypothetical): 'were to + verb' in the if-clause requires 'would + base verb' in the main clause.",
            "band_note": "Ideal for proposing policy recommendations in IELTS Writing Task 2."
        },
        {
            "id": "fill_cond_3",
            "category": "Conditionals",
            "prompt": "Had the engineers _____ (anticipate) the seismic tremor, the structural reinforcements would have prevented collapse.",
            "acceptable": ["anticipated"],
            "explanation": "Inverted third conditional ('Had + subject + past participle') eliminates 'if' for elevated academic register.",
            "band_note": "Inverted conditionals reflect Band 8.5+ sophisticated sentence structures."
        },
        {
            "id": "fill_pass_1",
            "category": "Passive Voice",
            "prompt": "It is widely _____ (argue) by sociologists that early childhood education bridges socioeconomic divides.",
            "acceptable": ["argued", "contended", "believed"],
            "explanation": "Impersonal passive reporting: 'It is + past participle + that-clause' establishes objective academic tone.",
            "band_note": "Replaces informal 'People think that' with Band 7+ academic objectivity."
        },
        {
            "id": "fill_pass_2",
            "category": "Passive Voice",
            "prompt": "Comprehensive clinical trials must be _____ (carry out) before new vaccines receive regulatory approval.",
            "acceptable": ["carried out", "conducted"],
            "explanation": "Modal passive: 'must be + past participle'. Note 'carried out' is the past participle of the phrasal verb 'carry out'.",
            "band_note": "Modal passives add precision when discussing regulations and mandates."
        },
        {
            "id": "fill_pass_3",
            "category": "Passive Voice",
            "prompt": "The historical artifacts were _____ (preserve) in temperature-controlled glass vaults.",
            "acceptable": ["preserved"],
            "explanation": "Past simple passive: 'were + past participle'.",
            "band_note": "Crucial for describing processes in Academic Writing Task 1."
        },
        {
            "id": "fill_sva_1",
            "category": "Subject-Verb Agreement",
            "prompt": "The rapid expansion of metropolitan rail networks _____ (have / has) reduced average commuting times.",
            "acceptable": ["has"],
            "explanation": "The head subject is 'The rapid expansion' (singular), not the intervening plural noun 'networks'.",
            "band_note": "Classic IELTS distractor: do not let intervening plural nouns mislead your verb concord."
        },
        {
            "id": "fill_sva_2",
            "category": "Subject-Verb Agreement",
            "prompt": "Each of the experimental samples _____ (was / were) preserved at sub-zero temperatures.",
            "acceptable": ["was"],
            "explanation": "'Each of + plural noun' always takes a singular verb in standard formal English.",
            "band_note": "Essential precision rule for both Academic Task 1 and Task 2."
        },
        {
            "id": "fill_sva_3",
            "category": "Subject-Verb Agreement",
            "prompt": "Neither the head physician nor the senior nurses _____ (was / were) aware of the pharmaceutical defect.",
            "acceptable": ["were"],
            "explanation": "Concord with 'neither... nor': the verb agrees with the closer subject ('senior nurses', plural).",
            "band_note": "Proximity agreement with correlative conjunctions tests high-level grammatical mastery."
        },
        {
            "id": "fill_inv_1",
            "category": "Inversion",
            "prompt": "Not only _____ (do / does / did) automated robotics increase production velocity, but they also minimize industrial accidents.",
            "acceptable": ["do"],
            "explanation": "Negative/restrictive adverbial inversion: 'Not only + auxiliary verb (do) + plural subject (robotics) + main verb'.",
            "band_note": "Inversion structures are an explicit descriptor indicator for Band 8+ Grammatical Range."
        },
        {
            "id": "fill_inv_2",
            "category": "Inversion",
            "prompt": "Seldom _____ (have / has / do) researchers witnessed such rapid biodiversity recovery in a protected reserve.",
            "acceptable": ["have"],
            "explanation": "Adverbial inversion with 'Seldom': auxiliary 'have' precedes the plural subject 'researchers'.",
            "band_note": "Dramatic emphasis structure that stands out to examiners in essays."
        },
        {
            "id": "fill_inv_3",
            "category": "Inversion",
            "prompt": "Under no circumstances _____ (should / must / will) confidential participant medical records be disclosed without authorization.",
            "acceptable": ["should", "must"],
            "explanation": "Fronted negative prepositional phrase: 'Under no circumstances + modal auxiliary + subject'.",
            "band_note": "Authoritative legislative phrasing for public policy discussions."
        },
        {
            "id": "fill_rel_1",
            "category": "Relative Clauses",
            "prompt": "_____ (Having / Have / Had) scrutinized the financial telemetry, the board authorized the merger.",
            "acceptable": ["Having"],
            "explanation": "Perfect participle clause ('Having + past participle') indicates an action completed before the main clause verb.",
            "band_note": "Combines two sentences seamlessly without overusing basic connectors like 'and' or 'so'."
        },
        {
            "id": "fill_rel_2",
            "category": "Relative Clauses",
            "prompt": "The statistical discrepancy, _____ (which / that) puzzled economists for months, was attributable to sampling errors.",
            "acceptable": ["which"],
            "explanation": "Non-defining relative clauses set off by commas must use 'which', never 'that'.",
            "band_note": "Punctuation and pronoun precision in non-restrictive relative clauses."
        },
        {
            "id": "fill_prep_1",
            "category": "Prepositions",
            "prompt": "Heavy commercial vehicle emissions exert a profoundly detrimental impact _____ (on / in / at) air quality.",
            "acceptable": ["on", "upon"],
            "explanation": "The noun 'impact' takes the dependent preposition 'on' (or 'upon').",
            "band_note": "Collocational prepositions must be exact to secure Band 7+ Lexical and Grammatical accuracy."
        },
        {
            "id": "fill_prep_2",
            "category": "Prepositions",
            "prompt": "Municipal authorities were held responsible _____ (for / of / about) the delayed infrastructure upgrades.",
            "acceptable": ["for"],
            "explanation": "'Responsible' takes the preposition 'for' when attributing accountability.",
            "band_note": "Frequent mistake: candidates often mistakenly say 'responsible of'."
        },
        {
            "id": "fill_prep_3",
            "category": "Prepositions",
            "prompt": "Corporate leaders must comply _____ (with / to / at) international carbon emission standards.",
            "acceptable": ["with"],
            "explanation": "The verb 'comply' strictly governs the dependent preposition 'with'.",
            "band_note": "Band 7+ regulatory vocabulary collocation."
        },
        {
            "id": "fill_hedge_1",
            "category": "Modal Verbs",
            "prompt": "The empirical findings tend to _____ (suggest / suggests / suggesting) that remote work improves employee retention.",
            "acceptable": ["suggest"],
            "explanation": "'Tend to + base infinitive verb' is an academic hedging device preventing unsubstantiated over-generalization.",
            "band_note": "IELTS examiners penalize sweeping absolutes. Hedging with 'tends to suggest' aligns with Band 8+ academic style."
        },
        {
            "id": "fill_art_1",
            "category": "Articles",
            "prompt": "Professor Vance provided invaluable _____ (advice / advices) regarding methodology design.",
            "acceptable": ["advice"],
            "explanation": "'Advice' is strictly uncountable in English and can never take a plural '-s' or indefinite 'an'.",
            "band_note": "Common error among non-native candidates; examiners penalize 'an advice' or 'advices'."
        },
        {
            "id": "fill_art_2",
            "category": "Articles",
            "prompt": "The laboratory imported state-of-the-art laboratory _____ (equipment / equipments) from Germany.",
            "acceptable": ["equipment"],
            "explanation": "'Equipment' is an uncountable noun that cannot take plural '-s'.",
            "band_note": "Demonstrates grammatical accuracy with mass nouns."
        },
        {
            "id": "fill_tense_1",
            "category": "Tenses",
            "prompt": "Archaeologists _____ (discover) the ancient stone tablets during the 1922 excavation.",
            "acceptable": ["discovered"],
            "explanation": "Specific completed historical date ('in 1922') requires the Past Simple 'discovered', not the Present Perfect.",
            "band_note": "Finished past time markers demand the Past Simple."
        },
        {
            "id": "fill_tense_2",
            "category": "Tenses",
            "prompt": "Over the past three decades, biomedical engineers _____ (develop) highly sophisticated neural prosthetics.",
            "acceptable": ["have developed"],
            "explanation": "Time period connecting past to present ('Over the past three decades') requires the Present Perfect.",
            "band_note": "Essential tense for introducing background trends in IELTS Writing Task 2."
        },
        {
            "id": "fill_cleft_1",
            "category": "Complex Sentences",
            "prompt": "It was the sudden depletion of foreign reserves _____ (that / which / what) triggered currency devaluation.",
            "acceptable": ["that"],
            "explanation": "Standard it-cleft formula: 'It was + focused noun + that + clause'.",
            "band_note": "Emphatic cleft sentences showcase Band 8+ structural range."
        },
        {
            "id": "fill_cleft_2",
            "category": "Complex Sentences",
            "prompt": "What international delegates must realize _____ (is / are) that renewable transition requires substantial capital transfers.",
            "acceptable": ["is"],
            "explanation": "A wh-cleft nominal relative clause ('What international delegates must realize') functions as a singular subject governing 'is'.",
            "band_note": "Advanced discourse topicalization."
        },
        {
            "id": "fill_gerund_1",
            "category": "Gerunds & Infinitives",
            "prompt": "The diplomatic team looks forward to _____ (receive / receiving) the revised treaty proposal.",
            "acceptable": ["receiving"],
            "explanation": "In the phrasal expression 'look forward to', 'to' is a preposition governing a gerund (-ing).",
            "band_note": "Frequent trap in formal letter writing (General Training Task 1)."
        },
        {
            "id": "fill_subj_1",
            "category": "Subjunctive & Unreal Past",
            "prompt": "It is imperative that the government _____ (undertake / undertakes) an immediate independent audit.",
            "acceptable": ["undertake"],
            "explanation": "Mandative subjunctive following 'imperative that' requires the bare base form 'undertake' regardless of subject person.",
            "band_note": "Subjunctive structures demonstrate mastery of formal English syntax."
        },
        {
            "id": "fill_rep_1",
            "category": "Reported Speech",
            "prompt": "The lead investigator stated that the committee _____ (will / would) publish the full dossier the following week.",
            "acceptable": ["would"],
            "explanation": "Backshifting in reported speech: future modal 'will' shifts to 'would' after a past reporting verb ('stated').",
            "band_note": "Tense harmony in reported discourse."
        },
        {
            "id": "fill_det_1",
            "category": "Determiners & Quantifiers",
            "prompt": "Due to automated sorting, significantly _____ (fewer / less) clerical errors occurred this quarter.",
            "acceptable": ["fewer"],
            "explanation": "'Errors' is a countable plural noun, requiring 'fewer' rather than 'less'.",
            "band_note": "Precise usage of countability quantifiers."
        },
        {
            "id": "fill_cohesion_1",
            "category": "Cohesive Linkers",
            "prompt": "Renewable infrastructure demands substantial upfront investment; _____, (however / consequently) it eliminates long-term fuel costs.",
            "acceptable": ["however", "nevertheless"],
            "explanation": "The conjunctive adverb 'however' signals an antithetical contrast between upfront cost and long-term savings.",
            "band_note": "Accurate logical signposting."
        },
        {
            "id": "fill_parall_1",
            "category": "Parallel Structure",
            "prompt": "Effective academic scholarship involves synthesizing data, formulating hypotheses, and _____ (present) transparent conclusions.",
            "acceptable": ["presenting"],
            "explanation": "Parallel structure: all items in a serial coordination must share identical grammatical form (synthesizing, formulating, presenting).",
            "band_note": "Parallelism elevates stylistic cohesion in academic prose."
        }
    ]

    @classmethod
    def get_fill_up_drills(cls, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns cloze fill-up drills filtered by category or all drills."""
        if category:
            return [d for d in cls.FILL_UP_DRILLS if d["category"].lower() == category.lower()]
        return cls.FILL_UP_DRILLS

    @classmethod
    def evaluate_fill_up(cls, drill_id: str, user_answer: str) -> Dict[str, Any]:
        """Validates a learner's fill-in-the-blank answer."""
        drill = next((d for d in cls.FILL_UP_DRILLS if d["id"] == drill_id), None)
        if not drill:
            return {"is_correct": False, "error": f"Drill {drill_id} not found"}

        cleaned_user = user_answer.strip().lower()
        is_correct = any(cleaned_user == acc.lower() for acc in drill["acceptable"])

        return {
            "drill_id": drill_id,
            "category": drill["category"],
            "user_answer": user_answer,
            "is_correct": is_correct,
            "acceptable_answers": drill["acceptable"],
            "explanation": drill["explanation"],
            "band_note": drill.get("band_note", "")
        }

    @classmethod
    def check_sentence(cls, sentence: str) -> List[Dict[str, Any]]:
        """Scans sentence for grammatical errors and returns structured formative feedback."""
        diagnoses = []
        for rule in cls.ERROR_RULES:
            match = re.search(rule["pattern"], sentence, flags=re.IGNORECASE)
            if match:
                matched_str = match.group(0)
                corrected_str = re.sub(rule["pattern"], rule["correction_sub"], matched_str, flags=re.IGNORECASE)
                diagnoses.append({
                    "original": matched_str,
                    "full_sentence": sentence,
                    "category": rule["category"],
                    "correction": corrected_str,
                    "why": rule["why"],
                    "better_alternative": rule["better_alternative"],
                    "practice_exercise": rule["exercise"]
                })
        return diagnoses

    @classmethod
    def format_teach_through_correction(cls, error_dict: Dict[str, Any]) -> str:
        """Renders the prompt-mandated 5-point formative explanation."""
        return (
            f"**ORIGINAL:**\n\"{error_dict['original']}\"\n\n"
            f"**CORRECTION:**\n\"{error_dict['correction']}\"\n\n"
            f"**WHY:**\n{error_dict['why']}\n\n"
            f"**BETTER ALTERNATIVE (IELTS Band 7+):**\n{error_dict['better_alternative']}\n\n"
            f"**PRACTICE EXERCISE:**\n{error_dict['practice_exercise']}"
        )

    @classmethod
    def get_topic_lesson(cls, topic_name: str) -> Dict[str, Any]:
        """Provides curriculum outline and reference explanation for a grammar topic."""
        lessons = {
            "Articles": {
                "title": "Articles: Definite (The), Indefinite (A/An), and Zero Article",
                "rules": [
                    "Use 'a/an' with singular countable nouns mentioned for the first time.",
                    "Use 'the' when both speaker and listener know the specific referent, or with unique entities ('the sun', 'the government').",
                    "Use zero article with plural countable and uncountable nouns used in a general sense ('Water is essential', 'Students need sleep')."
                ],
                "academic_tip": "In IELTS Writing Task 1, always use 'the' with trends and figures: 'The proportion of students...', 'The number of vehicles...'"
            },
            "Subject-Verb Agreement": {
                "title": "Subject-Verb Agreement in Complex Academic Clauses",
                "rules": [
                    "Intervening prepositional phrases do not change the subject number: 'The quality of the research papers is high.'",
                    "Indefinite pronouns ('each', 'everyone', 'neither') take singular verbs.",
                    "Compound subjects joined by 'and' take plural verbs ('Poverty and unemployment contribute...')."
                ],
                "academic_tip": "Check sentences where the noun closest to the verb is plural but the true subject is singular."
            },
            "Conditionals": {
                "title": "Conditionals for Argumentation (Zero, First, Second, Third, Mixed)",
                "rules": [
                    "Zero: 'If temperature rises, ice melts.' (Universal truth)",
                    "First: 'If policies change, society will benefit.' (Real future condition)",
                    "Second: 'If governments banned fossil fuels, emissions would drop.' (Hypothetical present/future)",
                    "Third: 'If the team had verified the samples, errors would have been prevented.' (Unreal past)",
                    "Mixed: 'If authorities had planned earlier, the city would not face gridlock today.' (Past action -> Present result)"
                ],
                "academic_tip": "Using second and third conditionals in IELTS Writing Task 2 demonstrates Grammatical Range for Band 7+."
            },
            "Inversion": {
                "title": "Adverbial Inversion for Band 8+ Rhetorical Precision",
                "rules": [
                    "Front negative or limiting adverbials ('Not only', 'Seldom', 'Rarely', 'Under no circumstances').",
                    "Place the auxiliary verb immediately after the adverbial: 'Not only does automation save time...'",
                    "Never invert the main verb directly unless it is a form of 'be'."
                ],
                "academic_tip": "Use inversion sparingly (1-2 times per essay) to accentuate high-impact arguments without sounding artificial."
            },
            "Passive Voice": {
                "title": "Academic Passive Voice and Impersonal Reporting",
                "rules": [
                    "Form with appropriate tense of 'be' + past participle ('has been archived', 'were investigated').",
                    "Use impersonal reporting structures: 'It is widely contended that...', 'X is believed to have...'",
                    "Omit the agent ('by someone') when the agent is irrelevant, unknown, or obvious."
                ],
                "academic_tip": "Essential for Academic Writing Task 1 process diagrams and Task 2 objective argument development."
            }
        }
        return lessons.get(topic_name, {
            "title": f"Mastery Guide: {topic_name}",
            "rules": [f"Understand the structural function of {topic_name} in formal academic communication."],
            "academic_tip": f"Maintain precision and grammatical accuracy when utilizing {topic_name} under IELTS exam conditions."
        })
