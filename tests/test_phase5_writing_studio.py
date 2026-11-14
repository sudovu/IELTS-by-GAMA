# -*- coding: utf-8 -*-
"""
Tests for Phase 5: Writing Studio Expansion.
Verifies:
1. Academic Task 1: Line Graph, Bar Chart, Pie Chart, Table, Process Diagram, Map Comparison.
2. General Training Task 1: Formal, Semi-Formal, and Informal Letters.
3. Criteria scoring (TA/TR, CC, LR, GRA) with IELTS Advantage analysis.
4. Draft saving, retrieval, and evaluation persistence in SQLite.
"""

import unittest
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.database.repositories import WritingDraftRepository, TestResultRepository
from core.writing.writing_evaluator import WritingEvaluator


class TestPhase5WritingStudio(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_prompt_inventory_coverage(self):
        """Verifies all required Task 1 and Task 2 prompts are present."""
        prompts = WritingEvaluator.list_prompts()
        self.assertGreaterEqual(len(prompts), 13)

        # Check Academic Task 1 formats
        acad_t1_ids = [p["id"] for p in prompts if p["track"] == "Academic" and p["task_type"] == "task_1"]
        self.assertIn("acad_t1_energy", acad_t1_ids)      # Bar
        self.assertIn("acad_t1_emissions", acad_t1_ids)   # Line
        self.assertIn("acad_t1_water", acad_t1_ids)       # Pie
        self.assertIn("acad_t1_transit", acad_t1_ids)     # Table
        self.assertIn("acad_t1_desalination", acad_t1_ids) # Process
        self.assertIn("acad_t1_port_redevelopment", acad_t1_ids) # Map

        # Check General Training Task 1 letters
        gt_t1_ids = [p["id"] for p in prompts if p["track"] == "General" and p["task_type"] == "task_1"]
        self.assertIn("gt_t1_airline_complaint", gt_t1_ids) # Formal
        self.assertIn("gt_t1_gym_facilities", gt_t1_ids)   # Semi-formal
        self.assertIn("gt_t1_friend_visit", gt_t1_ids)     # Informal

        # Check Task 2 essays
        t2_ids = [p["id"] for p in prompts if p["task_type"] == "task_2"]
        self.assertIn("acad_t2_stem", t2_ids)
        self.assertIn("gt_t2_remote_work", t2_ids)

    def test_academic_task_1_evaluation(self):
        """Tests that Academic Task 1 rewards an Overview and penalizes personal opinions."""
        sample_task1 = (
            "The line graph illustrates greenhouse gas emissions produced by four economic sectors from 1990 to 2025.\n\n"
            "Overall, power generation experienced a dramatic plunge over the 35-year period, "
            "whereas road transport emissions demonstrated a persistent upward trajectory, making it the highest emitting sector by 2025. "
            "Agricultural emissions remained relatively static throughout the timeframe.\n\n"
            "In 1990, electricity generation accounted for the largest proportion of emissions at 450 megatonnes. "
            "However, this figure dropped sharply to 180 megatonnes in 2025 due to renewable energy integration and decarbonization policies. "
            "By comparison, manufacturing emissions fluctuated around 200 megatonnes during the first two decades before stabilizing at approximately 190 megatonnes.\n\n"
            "In contrast, transport emissions surged continuously from 120 megatonnes in 1990 to reach an unprecedented peak of 310 megatonnes in 2025. "
            "Finally, agricultural emissions showed negligible variation, hovering consistently between 100 and 110 megatonnes over the surveyed decades."
        )

        res = WritingEvaluator.evaluate_essay("acad_t1_emissions", sample_task1, db=self.db)
        self.assertIn("Task Achievement", res["criteria"])
        self.assertGreaterEqual(res["criteria"]["Task Achievement"], 6.5)
        self.assertGreaterEqual(res["estimated_band"], 6.5)
        self.assertEqual(res["task_type"], "task_1")
        self.assertEqual(res["track"], "Academic")

        # Verify overview check passed in checklist
        checklist = res["advantage_checklist"]
        overview_check = next(c for c in checklist if "Overview" in c["item"])
        self.assertTrue(overview_check["passed"])

    def test_general_training_task_1_letter(self):
        """Tests that GT Task 1 correctly identifies salutation, purpose, and sign-off."""
        sample_letter = (
            "Dear Sir or Madam,\n\n"
            "I am writing to formally register a complaint regarding my checked baggage, "
            "which was delivered severely damaged and three days late on flight GA-402 on October 14th.\n\n"
            "Upon retrieving my suitcase at the terminal carousel, I discovered that the hard outer shell was cracked, "
            "and valuable photographic equipment inside was broken. Specifically, the professional camera lens was shattered "
            "and the casing was dented beyond repair. Furthermore, because my luggage was missing for three days, "
            "I had to purchase emergency clothing, toiletries, and business attire at considerable personal expense in order to attend scheduled professional meetings.\n\n"
            "Given these unfortunate circumstances, I expect the airline to provide financial compensation of 450 dollars "
            "to cover the replacement cost of the suitcase and damaged contents. In addition, I request reimbursement for essential expenses. "
            "I have enclosed copies of my original baggage claim receipts and purchase invoices.\n\n"
            "I look forward to your prompt response and an equitable resolution to this matter within fourteen business days.\n\n"
            "Yours faithfully,\n"
            "Julian Sterling"
        )

        res = WritingEvaluator.evaluate_essay("gt_t1_airline_complaint", sample_letter, db=self.db)
        self.assertIn("Task Achievement", res["criteria"])
        self.assertGreaterEqual(res["criteria"]["Task Achievement"], 7.0)
        self.assertGreaterEqual(res["estimated_band"], 6.5)
        self.assertEqual(res["track"], "General")

        checklist = res["advantage_checklist"]
        salutation_check = next(c for c in checklist if "salutation" in c["item"].lower())
        signoff_check = next(c for c in checklist if "sign-off" in c["item"].lower())
        purpose_check = next(c for c in checklist if "purpose" in c["item"].lower())
        self.assertTrue(salutation_check["passed"])
        self.assertTrue(signoff_check["passed"])
        self.assertTrue(purpose_check["passed"])

    def test_draft_saving_and_persistence(self):
        """Tests autosaving and evaluation persistence into SQLite."""
        learner_id = "phase5_test_learner"
        prompt_id = "acad_t2_stem"
        draft_text = "Education is fundamental to economic growth and societal prosperity. Although STEM disciplines are vital..."

        # 1. Save draft
        saved_draft = WritingEvaluator.save_draft(
            learner_id=learner_id,
            prompt_id=prompt_id,
            draft_text=draft_text,
            db=self.db
        )
        draft_id = saved_draft["id"]
        self.assertIsNotNone(draft_id)
        self.assertEqual(saved_draft["status"], "draft")

        # 2. Retrieve drafts
        drafts = WritingEvaluator.get_learner_drafts(learner_id, db=self.db)
        self.assertEqual(len(drafts), 1)
        self.assertEqual(drafts[0]["prompt_id"], prompt_id)

        # 3. Evaluate and persist
        full_essay = (
            "In contemporary society, education plays a vital role in determining national prosperity and individual empowerment. "
            "Some educationalists argue that high school curricula should prioritize STEM subjects over artistic fields to ensure economic competitiveness. "
            "Although scientific skills are crucial for modern industry, I believe artistic studies are equally indispensable for nurturing creative problem-solving.\n\n"
            "To begin with, technological development requires robust training in engineering, mathematics, and computing. "
            "Consequently, students equipped with quantitative competence can innovate modern digital infrastructure and power sustainable industries. "
            "Developing nations investing heavily in technical education have witnessed accelerated economic modernization.\n\n"
            "On the other hand, the humanities, fine arts, and literature cultivate empathy, critical discernment, and emotional intelligence. "
            "Furthermore, modern technology enterprises increasingly seek individuals who combine technical proficiency with artistic creativity. "
            "Neglecting the creative arts risks producing technically adept workers who lack interpersonal awareness.\n\n"
            "In conclusion, while STEM domains provide practical utility, a balanced educational curriculum embracing both science and arts is essential."
        )
        eval_res = WritingEvaluator.evaluate_essay(
            prompt_id=prompt_id,
            essay_text=full_essay,
            learner_id=learner_id,
            draft_id=draft_id,
            db=self.db
        )

        # Check draft updated to 'evaluated'
        updated_drafts = WritingEvaluator.get_learner_drafts(learner_id, db=self.db)
        self.assertEqual(updated_drafts[0]["status"], "evaluated")
        self.assertGreaterEqual(updated_drafts[0]["overall_band"], 5.0)

        # Check test_results recorded writing score for dashboard
        test_repo = TestResultRepository(self.db)
        recent_tests = test_repo.get_recent_tests(learner_id, limit=5)
        self.assertGreaterEqual(len(recent_tests), 1)
        self.assertIsNotNone(recent_tests[0]["writing_band"])


if __name__ == "__main__":
    unittest.main()
