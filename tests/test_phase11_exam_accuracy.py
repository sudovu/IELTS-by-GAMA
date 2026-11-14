# -*- coding: utf-8 -*-
"""
test_phase11_exam_accuracy.py
Independent IELTS Exam Accuracy and Assessment Criteria Verification Suite (Phase 11C).
Audits:
1. Listening: 4 sections, 10 questions/sec (40 total), spelling, word limits, answer concealment.
2. Reading: Academic (3 long analytical texts) & General Training (social/workplace/general),
   all question types, TFNG vs YNNG, completion word limits, evidence mapping.
3. Writing: Academic Task 1 (6 visual formats), GT Task 1 (3 letter registers), Task 2,
   4-criteria scoring (TA/TR, CC, LR, GRA), length penalties.
4. Speaking: 3-part structure, fluency WPM, pronunciation drills, transparent assessment disclosures.
"""

import unittest
from core.listening.listening_engine import ListeningEngine, ListeningAnswerChecker
from core.reading.reading_engine import ReadingEngine
from core.reading.question_types import ReadingQuestionTypes
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.speaking.fluency_tracker import FluencyTracker
from core.speaking.pronunciation_coach import PronunciationCoach
from core.database.db_manager import DatabaseManager


class TestPhase11ExamAccuracy(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.db.init_schema()

    def tearDown(self):
        self.db.close()

    # -------------------------------------------------------------
    # 1. LISTENING AUDIT
    # -------------------------------------------------------------
    def test_listening_mock_structure_and_counts(self):
        """Verifies exactly 4 sections, 10 questions per section, 40 total questions."""
        sections = ListeningEngine.list_sections()
        self.assertEqual(len(sections), 4, "Must have exactly 4 listening sections")

        for idx, sec in enumerate(sections, 1):
            self.assertEqual(sec["section_number"], idx)
            self.assertEqual(sec["question_count"], 10, f"Section {idx} must have 10 questions")

        total = sum(s["question_count"] for s in sections)
        self.assertEqual(total, 40, "Total listening mock must have exactly 40 questions")

    def test_listening_exam_concealment_and_transparency(self):
        """Verifies that exam mode conceals audio scripts and answers, while review reveals them."""
        # Exam mode: transcripts hidden
        exam_mock = ListeningEngine.generate_full_listening_mock(show_transcripts=False)
        self.assertEqual(len(exam_mock["sections"]), 4)
        for sec in exam_mock["sections"]:
            self.assertNotIn("audio_script", sec, "Audio script must be concealed during examination")
            for q in sec["questions"]:
                self.assertNotIn("acceptable", q, "Answers must not leak in questions")

        # Review mode: transcripts revealed
        review_mock = ListeningEngine.generate_full_listening_mock(show_transcripts=True)
        for sec in review_mock["sections"]:
            self.assertIn("audio_script", sec, "Audio script must be provided in review mode")

    def test_listening_answer_validation_and_spelling(self):
        """Verifies exact and normalized answer checking, spelling variants, and word limits."""
        # Case 1: Exact match
        is_ok, msg = ListeningAnswerChecker.check_answer("water filtration", ["water filtration"], max_words=2)
        self.assertTrue(is_ok)

        # Case 2: Case insensitivity and whitespace stripping
        is_ok, msg = ListeningAnswerChecker.check_answer("  Water Filtration  ", ["water filtration"], max_words=2)
        self.assertTrue(is_ok)

        # Case 3: Acceptable alternative
        is_ok, msg = ListeningAnswerChecker.check_answer("filtration system", ["water filtration", "filtration system"], max_words=2)
        self.assertTrue(is_ok)

        # Case 4: Exceeded word limit (max 2 words, user wrote 3)
        is_ok, msg = ListeningAnswerChecker.check_answer("clean water filtration", ["water filtration"], max_words=2)
        self.assertFalse(is_ok)
        self.assertIn("exceeded word count", msg.lower())

    def test_listening_submission_evaluation_and_distractor_analysis(self):
        """Verifies section submission evaluation reveals distractor analysis and band score."""
        eval_res = ListeningEngine.evaluate_submission("sec_1", {1: "Sterling", 2: "wrong answer"})
        self.assertEqual(eval_res["section_id"], "sec_1")
        self.assertGreaterEqual(eval_res["correct_answers"], 1)
        self.assertIn("estimated_band", eval_res)
        self.assertIn("disclaimer", eval_res)

        # Verify distractor analysis is populated
        q1 = eval_res["results"][0]
        self.assertTrue(q1["is_correct"])
        self.assertIn("distractor_analysis", q1)

    # -------------------------------------------------------------
    # 2. READING AUDIT
    # -------------------------------------------------------------
    def test_reading_track_distinctions_and_full_mock(self):
        """Verifies Academic (3 academic passages) vs General Training (workplace/general passages)."""
        acad_mock = ReadingEngine.generate_full_mock(track="Academic")
        self.assertEqual(acad_mock["track"], "Academic")
        self.assertEqual(len(acad_mock["passages"]), 3)
        self.assertEqual(acad_mock["time_limit_minutes"], 60)

        gt_mock = ReadingEngine.generate_full_mock(track="General Training")
        self.assertEqual(gt_mock["track"], "General Training")
        self.assertEqual(len(gt_mock["passages"]), 3)
        self.assertEqual(gt_mock["time_limit_minutes"], 60)

    def test_reading_tfng_vs_ynng_distinction(self):
        """Verifies strict differentiation between fact-based TFNG and opinion-based YNNG."""
        # True/False/Not Given
        res_true = ReadingQuestionTypes.grade_tfng("True", "True", "ev", "exp")
        self.assertTrue(res_true["is_correct"])

        res_false = ReadingQuestionTypes.grade_tfng("Not Given", "False", "ev", "exp")
        self.assertFalse(res_false["is_correct"])

        # Yes/No/Not Given (author's perspective)
        res_yes = ReadingQuestionTypes.grade_ynng("Yes", "Yes", "ev", "exp")
        self.assertTrue(res_yes["is_correct"])

        res_no = ReadingQuestionTypes.grade_ynng("No", "No", "ev", "exp")
        self.assertTrue(res_no["is_correct"])

    def test_reading_question_types_dispatcher(self):
        """Verifies universal dispatcher handles TFNG, YNNG, MCQ, Matching, and Completion."""
        # 1. TFNG
        q_tfng = {"type": "TFNG", "correct": "True", "evidence": "passage ev", "explanation": "exp"}
        self.assertTrue(ReadingQuestionTypes.grade_question(q_tfng, "True")["is_correct"])

        # 2. YNNG
        q_ynng = {"type": "YNNG", "correct": "No", "evidence": "passage ev", "explanation": "exp"}
        self.assertTrue(ReadingQuestionTypes.grade_question(q_ynng, "No")["is_correct"])

        # 3. MCQ
        q_mcq = {"type": "MCQ", "correct": "B", "evidence": "ev", "explanation": "exp", "distractor_analysis": {"A": "Contradicts text"}}
        self.assertTrue(ReadingQuestionTypes.grade_question(q_mcq, "B")["is_correct"])
        self.assertFalse(ReadingQuestionTypes.grade_question(q_mcq, "A")["is_correct"])

        # 4. Matching
        q_match = {"type": "Matching Headings", "correct": "iv", "evidence": "ev", "explanation": "exp"}
        self.assertTrue(ReadingQuestionTypes.grade_question(q_match, "iv")["is_correct"])

        # 5. Completion with max words
        q_comp = {"type": "Sentence Completion", "acceptable": ["solar energy"], "max_words": 2, "evidence": "ev", "explanation": "exp"}
        self.assertTrue(ReadingQuestionTypes.grade_question(q_comp, "solar energy")["is_correct"])
        self.assertFalse(ReadingQuestionTypes.grade_question(q_comp, "renewable solar energy")["is_correct"])

    # -------------------------------------------------------------
    # 3. WRITING AUDIT
    # -------------------------------------------------------------
    def test_writing_all_task_types_and_formats(self):
        """Verifies Academic visual formats (Bar, Line, Pie, Table, Process, Map) and GT letters."""
        prompts = WritingEvaluator.list_prompts()
        self.assertGreaterEqual(len(prompts), 13)

        # Academic Task 1: 6 visual formats
        acad_t1 = [p for p in prompts if p["track"] == "Academic" and p["task_type"] == "task_1"]
        titles_acad = " ".join([p["title"].lower() + " " + p.get("question_type", "").lower() for p in acad_t1])
        for term in ["bar", "line", "pie", "table", "process", "map"]:
            self.assertIn(term, titles_acad, f"Academic Task 1 missing format: {term}")

        # General Training Task 1: 3 registers
        gt_t1 = [p for p in prompts if p["track"] == "General" and p["task_type"] == "task_1"]
        titles_gt = " ".join([p.get("question_type", "").lower() for p in gt_t1])
        for reg in ["formal", "semi-formal", "informal"]:
            self.assertIn(reg, titles_gt, f"General Training Task 1 missing register: {reg}")

        # Task 2 essays
        t2_prompts = [p for p in prompts if p["task_type"] == "task_2"]
        self.assertGreaterEqual(len(t2_prompts), 4)

    def test_writing_criteria_scoring_and_penalties(self):
        """Verifies that all 4 criteria are evaluated, and underlength penalties cap estimated band."""
        # Short essay (< 100 words on Task 2, requirement is 250)
        short_text = "Technology is good. It connects people across the world. However, some people do not like it."
        res_short = WritingEvaluator.evaluate_essay("acad_t2_stem", short_text, db=self.db)
        self.assertLess(res_short["word_count"], 100)
        self.assertLessEqual(res_short["estimated_band"], 5.0, "Short essay must be capped at Band 5.0")

        # Full essay with proper structure
        full_text = (
            "In contemporary society, an increasing number of individuals argue that high school students "
            "should exclusively study science, technology, engineering, and mathematics (STEM), while others "
            "contend that creative arts are equally indispensable. Although technical proficiencies drive economic prosperity, "
            "I firmly believe that both domains are mutually reinforcing and vital for well-rounded development.\n\n"
            "Firstly, STEM disciplines furnish students with analytical capabilities to solve pressing global dilemmas. "
            "For instance, computing and mathematics foster logical problem-solving skills that prepare secondary students "
            "for technological industries. Without rigorous scientific foundations, students may encounter limitations in emerging global labor markets.\n\n"
            "Conversely, arts and humanities cultivate creative discernment, emotional intelligence, and critical expression. "
            "Scientific knowledge without creative inspiration often yields rigid solutions. Artistic pursuits encourage students "
            "to approach scientific challenges from imaginative angles, thereby stimulating innovative design and holistic thinking.\n\n"
            "Furthermore, multidisciplinary education ensures balanced personal development. Exposure to literature, painting, "
            "and music reduces academic burnout and enhances communication abilities, which are paramount when explaining "
            "complex technical projects to broader audiences.\n\n"
            "In conclusion, although STEM education is vital for technological progress, artistic subjects nourish the creative "
            "and expressive capacities required to deploy technology humanely. Therefore, secondary curricula should maintain "
            "an integrated approach rather than prioritizing one field over another."
        )
        res_full = WritingEvaluator.evaluate_essay("acad_t2_stem", full_text, db=self.db)
        for criterion in ["Task Response", "Coherence and Cohesion", "Lexical Resource", "Grammatical Range and Accuracy"]:
            self.assertIn(criterion, res_full["criteria"])
            self.assertGreaterEqual(res_full["criteria"][criterion], 6.0)

    # -------------------------------------------------------------
    # 4. SPEAKING AUDIT
    # -------------------------------------------------------------
    def test_speaking_three_part_structure_and_models(self):
        """Verifies Part 1 (Introduction/Interview), Part 2 (Cue Card), and Part 3 (Discussion)."""
        prompt_set = SpeakingExaminer.get_test_prompts(0)
        self.assertIn("part_1", prompt_set)
        self.assertIn("part_2_cue_card", prompt_set)
        self.assertIn("part_3_discussion", prompt_set)
        self.assertIn("band_9_model", prompt_set["part_2_cue_card"])
        self.assertIn("advantage_strategy_tip", prompt_set)
        self.assertIn("disclaimer", prompt_set)

    def test_speaking_objective_fluency_and_pronunciation(self):
        """Verifies FluencyTracker provides objective metrics and PronunciationCoach provides transparent feedback."""
        speech = "Well, I believe that living in urban environments has um several distinct advantages."
        fluency = FluencyTracker.analyze_fluency(speech, duration_seconds=8.0)
        self.assertIn("words_per_minute", fluency)
        self.assertIn("filler_breakdown", fluency)
        self.assertEqual(fluency["filler_breakdown"].get("um"), 1)

        # Pronunciation check
        drill = PronunciationCoach.evaluate_drill_attempt("minimal_pair", "sheep", "The sheep is in the meadow")
        self.assertTrue(drill["phonemic_match"])
        self.assertIn("disclaimer", drill)


if __name__ == "__main__":
    unittest.main()
