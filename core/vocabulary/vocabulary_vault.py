# -*- coding: utf-8 -*-
"""
Comprehensive Vocabulary Vault & Spaced Repetition Manager for IELTS by GAMA.
Integrates:
- Academic Word List (AWL) across Sublists 1-10
- Rich lexical cards: IPA, definitions, collocations, word families, common pitfalls
- SM-2 Spaced Repetition System (SRS) for retention scheduling
- Full SQLite persistence via VocabularyVaultRepository and SRSRepository
"""

from typing import Dict, Any, List, Optional
import random
from ..database.db_manager import DatabaseManager
from ..database.repositories import VocabularyVaultRepository, SRSRepository, MistakeBookRepository
from ..progress.srs import SpacedRepetitionSystem


class VocabularyVault:
    """Manages the academic lexical database and learner SRS flashcard progression."""

    DEFAULT_VAULT_WORDS = [
        {
            "word": "substantial",
            "pos": "adjective",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "suhb-STAN-shuhl",
            "ipa": "/səbˈstæn.ʃəl/",
            "simple_definition": "Large in amount, size, or importance.",
            "advanced_definition": "Of considerable importance, volume, or consequence in quantitative or qualitative analysis.",
            "example_sentences": [
                "There was a substantial increase in government expenditure on renewable energy between 2010 and 2020.",
                "The research team gathered substantial empirical evidence to corroborate their initial hypothesis."
            ],
            "synonyms": ["considerable", "significant", "sizeable", "momentous"],
            "antonyms": ["negligible", "slight", "trivial", "insubstantial"],
            "word_family": {
                "noun": "substance",
                "verb": "substantiate",
                "adjective": "substantial",
                "adverb": "substantially",
                "negative": "insubstantial"
            },
            "collocations": ["substantial increase", "substantial evidence", "substantial proportion", "substantial difference"],
            "common_mistakes": ["Do not confuse with 'substantive' (which means dealing with matters of real basis or law)."],
            "academic_usage": "High-yield descriptor for Writing Task 1 trend magnitudes and Task 2 evidence presentation."
        },
        {
            "word": "fluctuate",
            "pos": "verb",
            "cefr_level": "B2",
            "band_tier": "Band 7.0-8.0",
            "pronunciation": "FLUK-choo-ayt",
            "ipa": "/ˈflʌk.tʃu.eɪt/",
            "simple_definition": "To rise and fall irregularly in number or amount.",
            "advanced_definition": "To undergo continuous change, variation, or shift in value or intensity around an equilibrium point.",
            "example_sentences": [
                "Crude oil prices fluctuated wildly between 60 and 95 dollars per barrel throughout the fiscal year.",
                "Candidate approval ratings fluctuated following the televised parliamentary debates."
            ],
            "synonyms": ["oscillate", "vary", "waver", "alternate"],
            "antonyms": ["stabilize", "plateau", "remain steady"],
            "word_family": {
                "noun": "fluctuation",
                "verb": "fluctuate",
                "adjective": "fluctuating",
                "adverb": "fluctuatingly"
            },
            "collocations": ["fluctuate wildly", "fluctuate between X and Y", "fluctuate over time", "seasonal fluctuation"],
            "common_mistakes": ["Use 'between X and Y' rather than 'from X to Y' when describing continuous non-linear oscillation."],
            "academic_usage": "Cardinal verb for Academic Writing Task 1 time-series line graphs and volatile economic charts."
        },
        {
            "word": "ameliorate",
            "pos": "verb",
            "cefr_level": "C2",
            "band_tier": "Band 8.0-9.0",
            "pronunciation": "uh-MEE-lee-uh-rayt",
            "ipa": "/əˈmiː.li.ə.reɪt/",
            "simple_definition": "To make something bad or difficult better.",
            "advanced_definition": "To improve or mitigate a deleterious, suboptimal, or oppressive condition.",
            "example_sentences": [
                "Subsidized public transport networks can ameliorate severe urban traffic congestion and lower emissions.",
                "Targeted social welfare interventions helped ameliorate child malnutrition in rural districts."
            ],
            "synonyms": ["alleviate", "mitigate", "enhance", "remedy"],
            "antonyms": ["exacerbate", "worsen", "aggravate"],
            "word_family": {
                "noun": "amelioration",
                "verb": "ameliorate",
                "adjective": "ameliorative"
            },
            "collocations": ["ameliorate conditions", "ameliorate the effects", "ameliorate poverty", "substantially ameliorate"],
            "common_mistakes": ["Do not use for already positive things; you ameliorate a dilemma, hardship, or symptom, not success."],
            "academic_usage": "Sophisticated Band 8.5 solution-verb in Task 2 essays on social policy, environmental mitigation, and economics."
        },
        {
            "word": "detrimental",
            "pos": "adjective",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "deh-truh-MEN-tuhl",
            "ipa": "/ˌdɛt.rɪˈmɛn.təl/",
            "simple_definition": "Causing damage or harm.",
            "advanced_definition": "Producing harm, impairment, or disadvantageous effects upon an organism, system, or society.",
            "example_sentences": [
                "Sedentary desk lifestyles exert a detrimental impact on long-term cardiovascular health.",
                "Excessive light pollution produces detrimental consequences for nocturnal animal navigation."
            ],
            "synonyms": ["deleterious", "harmful", "damaging", "adverse", "injurious"],
            "antonyms": ["beneficial", "advantageous", "salutary", "constructive"],
            "word_family": {
                "noun": "detriment",
                "adjective": "detrimental",
                "adverb": "detrimentally"
            },
            "collocations": ["detrimental impact on", "detrimental effect", "detrimental consequence", "to the detriment of"],
            "common_mistakes": ["Collocates with preposition 'to' or 'on' ('detrimental to health'), not 'for'."],
            "academic_usage": "Superior academic replacement for the colloquial word 'bad' across Writing Task 2 and Speaking Part 3."
        },
        {
            "word": "catalyst",
            "pos": "noun",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "KAT-uh-list",
            "ipa": "/ˈkæt.ə.lɪst/",
            "simple_definition": "Someone or something that speeds up change.",
            "advanced_definition": "An agent, factor, or event that precipitates or significantly accelerates notable socioeconomic or scientific change.",
            "example_sentences": [
                "The advent of mobile telecommunications served as a major catalyst for micro-enterprise in emerging economies.",
                "Government tax credits acted as a prime catalyst for private investment in solar technology."
            ],
            "synonyms": ["stimulus", "impetus", "spark", "spur", "instigator"],
            "antonyms": ["deterrent", "impediment", "hindrance"],
            "word_family": {
                "noun": "catalyst / catalysis",
                "verb": "catalyze",
                "adjective": "catalytic"
            },
            "collocations": ["act as a catalyst", "prime catalyst", "catalyst for change", "serve as a catalyst"],
            "common_mistakes": ["Always followed by the preposition 'for' ('a catalyst for reform'), never 'of'."],
            "academic_usage": "Ideal for Writing Task 2 and Speaking when discussing causes, technological drivers, and societal transformation."
        },
        {
            "word": "disparity",
            "pos": "noun",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "dih-SPAIR-uh-tee",
            "ipa": "/dɪˈspær.ɪ.ti/",
            "simple_definition": "A noticeable difference, usually unfair.",
            "advanced_definition": "A pronounced inequality, disproportion, or incongruity in treatment, income, or opportunity between demographic groups.",
            "example_sentences": [
                "There remains a marked economic disparity between urban metropolitan enclaves and rural communities.",
                "Educational disparities were exacerbated when students lacked internet access during school closures."
            ],
            "synonyms": ["inequality", "discrepancy", "imbalance", "divergence"],
            "antonyms": ["parity", "equality", "similarity", "congruence"],
            "word_family": {
                "noun": "disparity",
                "adjective": "disparate"
            },
            "collocations": ["income disparity", "regional disparity", "marked disparity", "growing disparity"],
            "common_mistakes": ["Do not pluralize as 'disparities' when speaking of the general abstract concept of inequality."],
            "academic_usage": "Standard academic vocabulary for discussing economic inequality, educational access, and health outcomes."
        },
        {
            "word": "unprecedented",
            "pos": "adjective",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "uhn-PRES-uh-den-tid",
            "ipa": "/ʌnˈprɛs.ɪ.dɛn.tɪd/",
            "simple_definition": "Never having happened or existed before.",
            "advanced_definition": "Lacking any prior historical parallel, benchmark, or antecedent in scale, velocity, or scope.",
            "example_sentences": [
                "The 21st century has witnessed an unprecedented expansion of digital telecommunications networks.",
                "Metropolitan temperatures reached unprecedented heights during the mid-August heatwave."
            ],
            "synonyms": ["unparalleled", "unrivaled", "record-breaking", "groundbreaking"],
            "antonyms": ["precedented", "commonplace", "familiar", "routine"],
            "word_family": {
                "noun": "precedent",
                "adjective": "precedented / unprecedented",
                "adverb": "unprecedentedly"
            },
            "collocations": ["unprecedented scale", "unprecedented growth", "unprecedented challenge", "at an unprecedented rate"],
            "common_mistakes": ["Ensure spelling with a 'c' ('precedent'), not 'pressident'."],
            "academic_usage": "Effective for emphasizing record highs or extraordinary historical shifts in Writing Task 1 and 2."
        },
        {
            "word": "substantiate",
            "pos": "verb",
            "cefr_level": "C2",
            "band_tier": "Band 8.0-9.0",
            "pronunciation": "suhb-STAN-shee-ayt",
            "ipa": "/səbˈstæn.ʃi.eɪt/",
            "simple_definition": "To prove with facts or evidence.",
            "advanced_definition": "To establish the truth, validity, or plausibility of an assertion by providing concrete verifiable evidence.",
            "example_sentences": [
                "Researchers conducted a longitudinal study with 2,000 participants to substantiate their claims.",
                "Without empirical evidence to substantiate the proposal, committee funding was denied."
            ],
            "synonyms": ["corroborate", "validate", "authenticate", "verify"],
            "antonyms": ["refute", "disprove", "debunk", "invalidate"],
            "word_family": {
                "noun": "substantiation",
                "verb": "substantiate",
                "adjective": "substantiated / substantial"
            },
            "collocations": ["substantiate claims", "substantiate hypotheses", "substantiate evidence", "adequately substantiate"],
            "common_mistakes": ["Active verb: 'Evidence substantiates the claim', or passive: 'The claim is substantiated by evidence'."],
            "academic_usage": "Crucial verb for thesis justification and evidence-based argumentation in IELTS Task 2."
        },
        {
            "word": "trajectory",
            "pos": "noun",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "truh-JEK-tuh-ree",
            "ipa": "/trəˈdʒɛk.tər.i/",
            "simple_definition": "The path that something follows over time.",
            "advanced_definition": "The course, curve, or evolutionary pathway charted by a physical body, trend, or socioeconomic metric over time.",
            "example_sentences": [
                "The line graph portrays a steep upward trajectory in electric vehicle sales from 2015 to 2025.",
                "Without strict policy interventions, national carbon emissions will remain on a dangerous trajectory."
            ],
            "synonyms": ["course", "pathway", "trend", "vector", "direction"],
            "antonyms": ["plateau", "stagnation"],
            "word_family": {
                "noun": "trajectory"
            },
            "collocations": ["upward trajectory", "downward trajectory", "growth trajectory", "alter the trajectory"],
            "common_mistakes": ["Collocates with 'upward' or 'downward' ('on an upward trajectory'), not 'rising trajectory'."],
            "academic_usage": "Premier term for Academic Writing Task 1 trends and Task 2 future projections."
        },
        {
            "word": "paramount",
            "pos": "adjective",
            "cefr_level": "C1",
            "band_tier": "Band 7.5-8.5",
            "pronunciation": "PAIR-uh-mownt",
            "ipa": "/ˈpær.ə.maʊnt/",
            "simple_definition": "More important than anything else.",
            "advanced_definition": "Supreme, overriding, or surpassing all other considerations in importance or urgency.",
            "example_sentences": [
                "Ensuring patient confidentiality is of paramount importance in biomedical research ethics.",
                "Child pedestrian safety must remain paramount when designing residential roadways."
            ],
            "synonyms": ["supreme", "cardinal", "preeminent", "indispensable", "vital"],
            "antonyms": ["trivial", "secondary", "negligible", "marginal"],
            "word_family": {
                "adjective": "paramount"
            },
            "collocations": ["of paramount importance", "paramount concern", "paramount duty", "remain paramount"],
            "common_mistakes": ["Most idiomatically used in the phrase 'is of paramount importance' rather than bare 'is paramount'."],
            "academic_usage": "High-impact academic signpost in Writing Task 2 introductions, topic sentences, and conclusions."
        }
    ]

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.repo = VocabularyVaultRepository(self.db)
        self.srs = SpacedRepetitionSystem(self.db)
        self.mistake_repo = MistakeBookRepository(self.db)

    def seed_default_vault(self) -> int:
        """Populates the vocabulary_vault database with curated AWL and high-yield lexical items from themes."""
        count = 0
        # 1. Seed static core words
        for item in self.DEFAULT_VAULT_WORDS:
            self.repo.upsert_word(
                word=item["word"],
                pos=item["pos"],
                cefr_level=item["cefr_level"],
                band_tier=item["band_tier"],
                simple_definition=item["simple_definition"],
                advanced_definition=item["advanced_definition"],
                example_sentences=item["example_sentences"],
                synonyms=item["synonyms"],
                antonyms=item["antonyms"],
                word_family=item["word_family"],
                collocations=item["collocations"],
                common_mistakes=item["common_mistakes"],
                pronunciation=item.get("pronunciation"),
                ipa=item.get("ipa"),
                academic_usage=item.get("academic_usage")
            )
            count += 1

        # 2. Seed themed words from content/vocabulary/themes.json
        try:
            from ..curriculum.content_manager import ContentManager
            themed_count = ContentManager.seed_database_vocabulary(self.db)
            count += themed_count
        except Exception:
            pass

        return count

    def get_word(self, word: str) -> Optional[Dict[str, Any]]:
        """Fetches full lexical details for a given word."""
        return self.repo.get_word(word)

    def search_words(self, query: str = "", cefr_level: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Searches vocabulary vault by text and optional CEFR level."""
        if cefr_level:
            return self.repo.get_by_cefr(cefr_level, limit=limit)
        return self.repo.search_words(query, limit=limit)

    def add_word_to_srs(self, learner_id: str, word: str) -> Dict[str, Any]:
        """Creates an SRS flashcard for the learner from a vault word."""
        word_data = self.get_word(word)
        if not word_data:
            word_data = {
                "word": word,
                "simple_definition": "Target vocabulary term for active recall.",
                "example_sentences": [f"Practice using '{word}' in an IELTS sentence."]
            }

        definition = word_data.get("advanced_definition") or word_data.get("simple_definition", "")
        examples = word_data.get("example_sentences", [""])
        example = examples[0] if examples else ""
        collocations = ", ".join(word_data.get("collocations", [])[:3])
        notes = f"CEFR: {word_data.get('cefr_level', 'B2')} | Collocations: {collocations}"

        return self.srs.add_vocabulary_card(
            learner_id=learner_id,
            word=word_data["word"],
            definition=definition,
            example_sentence=example,
            notes=notes
        )

    def get_due_srs_deck(self, learner_id: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Returns flashcards due for review today according to SM-2 schedule."""
        return self.srs.get_due_deck(learner_id, limit=limit)

    def review_card(self, item_id: str, grade: int) -> Dict[str, Any]:
        """Submits an SM-2 grade (0-5) and schedules next review."""
        return self.srs.review_card(item_id, grade)

    # -------------------------------------------------------------------------
    # INTERACTIVE VOCABULARY EXERCISE GENERATORS
    # -------------------------------------------------------------------------
    def generate_gap_fill_exercise(self, theme: Optional[str] = None, cefr_level: Optional[str] = None) -> Dict[str, Any]:
        """Generates a contextual sentence gap-fill exercise with multiple choice options."""
        from ..curriculum.content_manager import ContentManager
        words = ContentManager.search_all_vocabulary(cefr_level=cefr_level, theme_id=theme)
        if not words:
            words = list(self.DEFAULT_VAULT_WORDS)

        target = random.choice(words)
        target_word = target["word"]
        examples = target.get("example_sentences") or [target.get("contextual_example", "")]
        sentence = examples[0] if examples and examples[0] else f"The {target_word} was carefully evaluated."

        # Mask target word (case-insensitive)
        import re
        masked_sentence = re.sub(rf"\b{re.escape(target_word)}\b", "_____", sentence, flags=re.IGNORECASE)
        if "_____" not in masked_sentence:
            masked_sentence = f"_____: {target.get('simple_definition', target.get('definition', ''))}"

        # Select 3 distractor words from other items
        distractors = [w["word"] for w in words if w["word"] != target_word]
        if len(distractors) < 3:
            distractors = ["variable", "perspective", "dimension", "factor"]
        distractors = random.sample(distractors, 3)

        options = [target_word] + distractors
        random.shuffle(options)
        correct_idx = options.index(target_word)

        return {
            "exercise_type": "gap_fill",
            "prompt": f"Select the most appropriate word to complete the sentence:\n\n\"{masked_sentence}\"",
            "masked_sentence": masked_sentence,
            "target_word": target_word,
            "options": options,
            "correct_index": correct_idx,
            "explanation": f"'{target_word}' ({target.get('pos', 'word')}) means: {target.get('simple_definition', target.get('definition', ''))}.",
            "collocations": target.get("collocations", [])
        }

    def generate_synonym_exercise(self, theme: Optional[str] = None, cefr_level: Optional[str] = None) -> Dict[str, Any]:
        """Generates a synonym matching exercise."""
        from ..curriculum.content_manager import ContentManager
        words = ContentManager.search_all_vocabulary(cefr_level=cefr_level, theme_id=theme)
        words_with_syns = [w for w in words if w.get("synonyms") and len(w["synonyms"]) > 0]
        if not words_with_syns:
            words_with_syns = [w for w in self.DEFAULT_VAULT_WORDS if w.get("synonyms")]

        target = random.choice(words_with_syns)
        target_word = target["word"]
        correct_syn = target["synonyms"][0]

        # Distractor options
        all_other = [w["word"] for w in words if w["word"] != target_word and w["word"] != correct_syn]
        if len(all_other) < 3:
            all_other = ["diminish", "superficial", "unrelated", "rigid"]
        distractors = random.sample(all_other, 3)

        options = [correct_syn] + distractors
        random.shuffle(options)
        correct_idx = options.index(correct_syn)

        return {
            "exercise_type": "synonym_selection",
            "prompt": f"Which word is the closest academic synonym for '{target_word}'?",
            "target_word": target_word,
            "options": options,
            "correct_index": correct_idx,
            "explanation": f"'{correct_syn}' is a direct synonym of '{target_word}' (meaning: {target.get('simple_definition', '')})."
        }

    def generate_collocation_exercise(self, theme: Optional[str] = None, cefr_level: Optional[str] = None) -> Dict[str, Any]:
        """Generates an academic collocation matching exercise."""
        from ..curriculum.content_manager import ContentManager
        words = ContentManager.search_all_vocabulary(cefr_level=cefr_level, theme_id=theme)
        words_with_colloc = [w for w in words if w.get("collocations") and len(w["collocations"]) > 0]
        if not words_with_colloc:
            words_with_colloc = [w for w in self.DEFAULT_VAULT_WORDS if w.get("collocations")]

        target = random.choice(words_with_colloc)
        colloc = random.choice(target["collocations"])
        colloc_parts = colloc.split()

        if len(colloc_parts) >= 2:
            base_word = colloc_parts[0]
            correct_partner = " ".join(colloc_parts[1:])
        else:
            base_word = target["word"]
            correct_partner = "evidence"

        distractors = ["trouble", "mistake", "noise", "weather"]
        options = [correct_partner] + distractors[:3]
        random.shuffle(options)
        correct_idx = options.index(correct_partner)

        return {
            "exercise_type": "collocation_practice",
            "prompt": f"Which word naturally collocates with '{base_word}' in academic English?",
            "base_word": base_word,
            "options": options,
            "correct_index": correct_idx,
            "explanation": f"The natural academic collocation is '{base_word} {correct_partner}'."
        }

    def generate_word_family_exercise(self, theme: Optional[str] = None, cefr_level: Optional[str] = None) -> Dict[str, Any]:
        """Generates a word-family derivation exercise."""
        from ..curriculum.content_manager import ContentManager
        words = ContentManager.search_all_vocabulary(cefr_level=cefr_level, theme_id=theme)
        words_with_wf = [w for w in words if isinstance(w.get("word_family"), dict) and len(w["word_family"]) >= 2]
        if not words_with_wf:
            words_with_wf = [w for w in self.DEFAULT_VAULT_WORDS if isinstance(w.get("word_family"), dict)]

        target = random.choice(words_with_wf)
        wf = target["word_family"]
        target_pos, derived_form = random.choice(list(wf.items()))

        options = [derived_form, target["word"] + "ing", target["word"] + "ness", target["word"] + "ous"]
        options = list(dict.fromkeys(options))[:4]
        if len(options) < 4:
            options += ["unclear", "variation"]
            options = options[:4]
        random.shuffle(options)
        correct_idx = options.index(derived_form)

        return {
            "exercise_type": "word_family",
            "prompt": f"What is the {target_pos} form of the root word '{target['word']}'?",
            "root_word": target["word"],
            "target_pos": target_pos,
            "options": options,
            "correct_index": correct_idx,
            "explanation": f"The {target_pos} form of '{target['word']}' is '{derived_form}'."
        }

    def generate_vocab_quiz(self, theme: Optional[str] = None, cefr_level: Optional[str] = None, count: int = 5) -> Dict[str, Any]:
        """Combines multiple exercise types into a structured vocabulary quiz."""
        generators = [
            self.generate_gap_fill_exercise,
            self.generate_synonym_exercise,
            self.generate_collocation_exercise,
            self.generate_word_family_exercise
        ]

        questions = []
        for i in range(count):
            gen = generators[i % len(generators)]
            q = gen(theme=theme, cefr_level=cefr_level)
            q["id"] = f"v_quiz_{i+1}"
            questions.append(q)

        return {
            "quiz_id": f"vocab_quiz_{theme or 'general'}_{cefr_level or 'all'}",
            "theme": theme or "all_themes",
            "cefr_level": cefr_level or "mixed",
            "total_questions": len(questions),
            "questions": questions
        }

    def evaluate_quiz_submission(
        self,
        learner_id: str,
        quiz: Dict[str, Any],
        answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluates quiz answers, updates Mistake Book for errors, and awards progress."""
        correct_count = 0
        feedback = []

        for q in quiz.get("questions", []):
            qid = q["id"]
            user_ans = answers.get(qid)
            expected = q["correct_index"]
            is_correct = False

            try:
                is_correct = (int(user_ans) == expected)
            except (ValueError, TypeError):
                is_correct = False

            if is_correct:
                correct_count += 1
                feedback.append({
                    "question_id": qid,
                    "is_correct": True,
                    "user_answer": user_ans,
                    "correct_answer": expected,
                    "explanation": q.get("explanation", "Correct!")
                })
            else:
                feedback.append({
                    "question_id": qid,
                    "is_correct": False,
                    "user_answer": user_ans,
                    "correct_answer": expected,
                    "explanation": q.get("explanation", "Incorrect.")
                })
                # Log mistake
                opts = q.get("options", [])
                correct_text = opts[expected] if expected < len(opts) else "Correct Option"
                user_text = opts[int(user_ans)] if (user_ans is not None and str(user_ans).isdigit() and int(user_ans) < len(opts)) else "Unanswered"
                self.mistake_repo.record_mistake(
                    learner_id=learner_id,
                    skill="vocabulary",
                    category=q.get("exercise_type", "vocabulary_quiz"),
                    original_text=user_text,
                    corrected_text=correct_text,
                    explanation=q.get("explanation", "")
                )

        total = len(quiz.get("questions", []))
        score_percent = round((correct_count / max(1, total)) * 100.0, 1)

        return {
            "learner_id": learner_id,
            "total_questions": total,
            "correct_count": correct_count,
            "score_percent": score_percent,
            "feedback": feedback
        }
        """Submits an SM-2 grade (0-5) and schedules next review."""
        return self.srs.review_card(item_id, grade)
