"""
Tests for Phase 13: Educational Quality, Curriculum Depth & Assessment Reliability.
Verifies:
1. Depth thresholds across all 54 lessons (length, examples, guided drills, assessments).
2. Prerequisite cycle detection and graph integrity.
3. Themed Vocabulary Academy depth (15 themes, 120 words, rich lexical entries, zero cross-theme duplicates).
4. Scoring confidence intervals, uncertainty bounds, and official disclaimer transparency.
5. Speech recognition modality disclosure and acoustic analysis disclaimer.
6. Honest listening practice categorization (transcript-based strategy vs studio audio).
7. Multidimensional mastery progression in CurriculumEngine.
"""

import unittest
import copy
import json
import tempfile
import os
from core.database.db_manager import DatabaseManager
from core.curriculum.content_manager import ContentManager
from core.curriculum.validator import ContentValidator
from core.curriculum.curriculum_engine import CurriculumEngine
from core.scoring.criteria_evaluator import CriteriaEvaluator
from core.speaking.pronunciation_coach import PronunciationCoach
from core.listening.listening_engine import ListeningEngine


class TestPhase13EducationalQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_path = cls.temp_file.name
        cls.temp_file.close()
        cls.db = DatabaseManager(cls.temp_path)
        cls.db.init_schema()
        cls.curriculum_engine = CurriculumEngine(cls.db)
        cls.curriculum_engine.seed_default_curriculum()
        cls.lessons = ContentManager.load_curriculum_lessons()
        cls.themes = ContentManager.load_vocabulary_themes()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.db.close()
        except Exception:
            pass
        try:
            if os.path.exists(cls.temp_path):
                os.remove(cls.temp_path)
        except Exception:
            pass

    def test_curriculum_depth_and_substance_thresholds(self):
        """Verifies all 54 lessons meet rigorous educational depth thresholds."""
        self.assertEqual(len(self.lessons), 54, "Curriculum must contain exactly 54 structured lessons")

        total_explanation_chars = 0
        total_examples = 0
        total_guided = 0
        total_assessments = 0

        for l in self.lessons:
            lid = l["id"]
            exp = l.get("explanation_markdown", "")
            examples = l.get("examples", [])
            guided = l.get("guided_exercises", [])
            assessments = l.get("assessment", [])

            # Hard minimum thresholds per lesson
            self.assertGreaterEqual(len(exp), ContentValidator.MIN_EXPLANATION_LENGTH,
                                   f"Lesson {lid} explanation too short: {len(exp)} chars")
            self.assertGreaterEqual(len(examples), ContentValidator.MIN_EXAMPLES_PER_LESSON,
                                   f"Lesson {lid} has insufficient examples: {len(examples)}")
            self.assertGreaterEqual(len(guided), ContentValidator.MIN_GUIDED_EXERCISES_PER_LESSON,
                                   f"Lesson {lid} has insufficient guided drills: {len(guided)}")
            self.assertGreaterEqual(len(assessments), ContentValidator.MIN_ASSESSMENT_QUESTIONS_PER_LESSON,
                                   f"Lesson {lid} has insufficient assessment questions: {len(assessments)}")

            # Verify every assessment question has non-empty explanation and valid correct_index
            for q in assessments:
                self.assertIn("question", q)
                self.assertIn("options", q)
                self.assertGreaterEqual(len(q["options"]), 2)
                self.assertIn("correct_index", q)
                self.assertTrue(0 <= q["correct_index"] < len(q["options"]))
                self.assertTrue(bool(q.get("explanation")), f"Assessment question {q.get('id')} lacks explanation")

            total_explanation_chars += len(exp)
            total_examples += len(examples)
            total_guided += len(guided)
            total_assessments += len(assessments)

        avg_exp_chars = total_explanation_chars / len(self.lessons)
        self.assertGreaterEqual(avg_exp_chars, 800.0,
                                f"Average explanation length ({avg_exp_chars:.1f} chars) below 800 chars target")
        self.assertGreaterEqual(total_examples, 162)
        self.assertGreaterEqual(total_guided, 162)
        self.assertGreaterEqual(total_assessments, 162)

    def test_prerequisite_cycle_detection(self):
        """Verifies ContentValidator detects cyclic dependencies in prerequisite chains."""
        # 1. Clean validation on production curriculum
        c_val = ContentValidator.validate_curriculum(self.lessons)
        self.assertEqual(c_val["total_issues_found"], 0)
        self.assertEqual(c_val["quality_score_percent"], 100.0)

        # 2. Inject artificial cycle
        mutated_lessons = copy.deepcopy(self.lessons)
        lesson_map = {l["id"]: l for l in mutated_lessons}
        # Create cycle: A -> B -> A
        if "curric_a1_gram_present_simple" in lesson_map and "curric_a2_gram_past_simple" in lesson_map:
            lesson_map["curric_a1_gram_present_simple"]["prerequisites"] = ["curric_a2_gram_past_simple"]
            lesson_map["curric_a2_gram_past_simple"]["prerequisites"] = ["curric_a1_gram_present_simple"]

            cycle_val = ContentValidator.validate_curriculum(mutated_lessons)
            self.assertGreater(cycle_val["total_issues_found"], 0)
            has_cycle_error = any("circular" in iss.get("issue", "").lower() or "cycle" in iss.get("issue", "").lower()
                                  for iss in cycle_val["issues"])
            self.assertTrue(has_cycle_error, "Validator must explicitly report cyclic/circular prerequisite dependency")

    def test_vocabulary_academy_depth_and_lexical_richness(self):
        """Verifies Themed Vocabulary Academy has 15 themes, 120 words, zero duplicates, and full metadata."""
        v_val = ContentValidator.validate_vocabulary_themes(self.themes)
        self.assertEqual(v_val["total_issues_found"], 0, f"Vocabulary issues: {v_val['issues']}")
        self.assertEqual(v_val["quality_score_percent"], 100.0)

        self.assertEqual(len(self.themes), 15, "Must contain exactly 15 themes")
        all_words = []
        for theme_name, words in self.themes.items():
            self.assertGreaterEqual(len(words), 8, f"Theme '{theme_name}' has fewer than 8 words")
            for w in words:
                all_words.append(w["word"].strip().lower())
                self.assertTrue(bool(w.get("ipa")), f"Word {w['word']} lacks IPA")
                self.assertTrue(bool(w.get("definition")), f"Word {w['word']} lacks definition")
                self.assertGreaterEqual(len(w.get("collocations", [])), 2,
                                        f"Word {w['word']} needs >= 2 collocations")
                self.assertIn("ielts_usefulness", w)
                self.assertIsInstance(w.get("word_family"), dict)

        # Verify zero cross-theme duplicates
        self.assertEqual(len(all_words), len(set(all_words)), "No duplicate words allowed across themes")
        self.assertGreaterEqual(len(all_words), 120)

    def test_criteria_evaluator_confidence_intervals_and_disclaimers(self):
        """Verifies writing evaluation produces calibrated confidence bounds and official disclaimer."""
        sample_essay = (
            "The impact of automation on modern employment is profound and multifaceted. "
            "While technological innovation inevitably replaces routine manufacturing occupations, "
            "it simultaneously creates highly specialized opportunities in programming and systems design. "
            "Governments must proactively facilitate educational reskilling to prevent structural unemployment. "
            "In conclusion, automation is not an insurmountable crisis but a transition demanding decisive policy."
        )
        task_prompt = "Discuss the advantages and disadvantages of automation on modern workforce employment."
        result = CriteriaEvaluator.evaluate_writing(
            task_type="Task 2",
            track="Academic",
            text=sample_essay,
            tr_score=7.0,
            cc_score=7.0,
            lr_score=7.0,
            gra_score=7.0,
            word_count=len(sample_essay.split())
        )

        self.assertIn("confidence_range", result)
        conf = result["confidence_range"]
        self.assertIsInstance(conf, list)
        self.assertEqual(len(conf), 2)
        min_band, max_band = conf[0], conf[1]
        self.assertLessEqual(min_band, result["estimated_band"])
        self.assertGreaterEqual(max_band, result["estimated_band"])

        # Check official disclaimer and uncertainty disclosure
        self.assertIn("official_disclaimer", result)
        self.assertIn("not an official IELTS score", result["official_disclaimer"])
        self.assertIn("assessment_uncertainty_note", result)

    def test_pronunciation_coach_speech_modality_disclosure(self):
        """Verifies pronunciation evaluation discloses speech-to-text transcript modality."""
        result = PronunciationCoach.evaluate_drill_attempt(
            drill_type="syllable_stress",
            target_word="photograph",
            spoken_transcript="photograph"
        )
        self.assertIn("assessment_modality", result)
        self.assertIn("speech_recognition_transcript_matching", result["assessment_modality"])
        self.assertIn("modality_notice", result)
        self.assertIn("spectral or formant", result["modality_notice"].lower())
        self.assertIn("confidence_range", result)
        self.assertIn("disclaimer", result)
        self.assertIn("Not an official IELTS examiner score", result["disclaimer"])

    def test_listening_engine_honest_categorization(self):
        """Verifies listening tests are explicitly labeled as transcript strategy practice."""
        test_session = ListeningEngine.generate_full_listening_mock()
        self.assertIn("transcript_strategy_practice", test_session["activity_type"])
        self.assertIn("speech_synthesis_ready", test_session["audio_asset_status"])
        self.assertIn("instructions", test_session)
        self.assertIn("spoken dialogue scripts", test_session["instructions"].lower())

    def test_human_review_protocol_checklist(self):
        """Verifies the human review protocol defines all 8 required assessment dimensions."""
        checklist = ContentValidator.get_human_review_checklist()
        self.assertIsInstance(checklist, list)
        self.assertEqual(len(checklist), 8)
        areas = [item["area"] for item in checklist]
        self.assertTrue(any("grammar" in a.lower() for a in areas))
        self.assertTrue(any("vocabulary" in a.lower() for a in areas))
        self.assertTrue(any("ielts" in a.lower() for a in areas))
        self.assertTrue(any("cefr" in a.lower() for a in areas))


if __name__ == "__main__":
    unittest.main()
