"""
Phase 16 Automated Test Suite:
Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit.
Covers:
1. Role-based access control (Learner, Teacher, Examiner, Admin).
2. Teacher review workflow, criteria assessment, revision history, and draft saving.
3. Blind double-marking, disagreement matrix calculation, and senior examiner reconciliation.
4. Speaking review modality distinction (audio vs transcript) and non-acoustic protection.
5. Human benchmark dataset management, anonymization, consent enforcement, and withdrawal.
6. Calibration engine statistical integrity: honest zero-state when human data is absent.
7. Controlled beta pilot management: cohorts, participant enrollment, feedback, and bug tracking.
"""

import unittest
import json
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.database.migrations import MigrationManager
from core.database.repositories import LearnerRepository
from core.auth.auth_manager import AuthManager
from core.review.review_manager import ReviewManager
from core.review.double_marking import DoubleMarkingManager
from core.benchmark.benchmark_manager import BenchmarkManager
from core.benchmark.calibration_engine import CalibrationEngine
from core.beta.beta_manager import BetaManager
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer


class TestPhase16BetaToolkit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_path = cls.temp_file.name
        cls.temp_file.close()

        cls.db = DatabaseManager(cls.temp_path)
        cls.db.init_schema()
        mig = MigrationManager(cls.db)
        mig.run_migrations()

        cls.auth_mgr = AuthManager(cls.db)
        cls.review_mgr = ReviewManager(cls.db)
        cls.double_marking_mgr = DoubleMarkingManager(cls.db)
        cls.benchmark_mgr = BenchmarkManager(cls.db)
        cls.calibration_engine = CalibrationEngine(cls.db)
        cls.beta_mgr = BetaManager(cls.db)
        cls.learner_repo = LearnerRepository(cls.db)

        # Setup test learner
        cls.learner = cls.learner_repo.create_learner("Test Candidate", target_band=7.0)

        # Authenticate seeded test accounts
        cls.admin_user = cls.auth_mgr.authenticate("admin", "admin_secure_pass123")
        cls.admin_token = cls.auth_mgr.create_session(cls.admin_user["id"])

        cls.teacher_user = cls.auth_mgr.authenticate("teacher_sarah", "teacher_pass123")
        cls.teacher_token = cls.auth_mgr.create_session(cls.teacher_user["id"])

        cls.examiner_1 = cls.auth_mgr.authenticate("examiner_mark", "examiner_pass123")
        cls.examiner_1_token = cls.auth_mgr.create_session(cls.examiner_1["id"])

        cls.examiner_2 = cls.auth_mgr.authenticate("examiner_clara", "examiner_pass123")
        cls.examiner_2_token = cls.auth_mgr.create_session(cls.examiner_2["id"])

        cls.learner_user = cls.auth_mgr.authenticate("learner_alice", "learner_pass123")
        cls.learner_token = cls.auth_mgr.create_session(cls.learner_user["id"])

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "temp_path") and os.path.exists(cls.temp_path):
            try:
                os.unlink(cls.temp_path)
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # 1. PERMISSIONS & RBAC
    # -------------------------------------------------------------------------
    def test_01_rbac_permissions_enforcement(self):
        """Verifies server-side authorization: learners cannot access teacher/examiner areas."""
        # Teacher area
        ok_t, _, _ = self.auth_mgr.authorize_request(self.teacher_token, ["teacher", "admin"])
        self.assertTrue(ok_t)

        ok_l, _, err_l = self.auth_mgr.authorize_request(self.learner_token, ["teacher", "admin"])
        self.assertFalse(ok_l)
        self.assertIn("Forbidden", err_l)

        # Examiner area
        ok_e, _, _ = self.auth_mgr.authorize_request(self.examiner_1_token, ["examiner", "admin"])
        self.assertTrue(ok_e)

        ok_le, _, err_le = self.auth_mgr.authorize_request(self.learner_token, ["examiner", "admin"])
        self.assertFalse(ok_le)
        self.assertIn("Forbidden", err_le)

        # Unauthenticated request
        ok_no, _, err_no = self.auth_mgr.authorize_request(None, ["teacher", "admin"])
        self.assertFalse(ok_no)
        self.assertIn("Authentication required", err_no)

    # -------------------------------------------------------------------------
    # 2. TEACHER REVIEW WORKFLOW & DRAFTS
    # -------------------------------------------------------------------------
    def test_02_teacher_review_workflow_and_revisions(self):
        """Tests teacher review lifecycle: creation, draft saving, criteria evaluation, and revision tracking."""
        assign = self.review_mgr.create_assignment(
            submission_id="sub_w_101",
            submission_type="writing",
            learner_id=self.learner["id"],
            content_json={"task_type": "task_2", "essay_text": "STEM education drives modernization..."},
            assigned_to=self.teacher_user["id"],
            assigned_role="teacher",
            task_type="task_2",
            track="Academic"
        )
        aid = assign["assignment_id"]

        # 1. Save draft
        draft = self.review_mgr.save_evaluation(
            assignment_id=aid,
            reviewer_id=self.teacher_user["id"],
            reviewer_role="teacher",
            overall_band=6.5,
            criteria_scores={"task_achievement": 6.5, "coherence_cohesion": 6.5, "lexical_resource": 6.5, "grammatical_accuracy": 6.5},
            criterion_feedback={"task_achievement": "Draft note: Needs clearer conclusion."},
            status="draft"
        )
        self.assertTrue(draft["success"])
        self.assertEqual(draft["status"], "draft")
        self.assertEqual(draft["revision"], 1)

        # Check assignment status is 'in_progress'
        a_state = self.review_mgr.get_assignment(aid, reviewer_id=self.teacher_user["id"])
        self.assertEqual(a_state["status"], "in_progress")

        # 2. Update to final submission (increments revision)
        final_eval = self.review_mgr.save_evaluation(
            assignment_id=aid,
            reviewer_id=self.teacher_user["id"],
            reviewer_role="teacher",
            overall_band=7.0,
            criteria_scores={"task_achievement": 7.0, "coherence_cohesion": 7.0, "lexical_resource": 6.5, "grammatical_accuracy": 7.5},
            criterion_feedback={"task_achievement": "Final note: Good progression and examples."},
            general_comments="Well-argued response satisfying Band 7 requirements.",
            status="submitted"
        )
        self.assertTrue(final_eval["success"])
        self.assertEqual(final_eval["status"], "submitted")
        self.assertEqual(final_eval["revision"], 2)

        # Assignment is now completed
        a_final = self.review_mgr.get_assignment(aid, reviewer_id=self.teacher_user["id"])
        self.assertEqual(a_final["status"], "completed")

    # -------------------------------------------------------------------------
    # 3. BLIND DOUBLE-MARKING & DISAGREEMENT RECONCILIATION
    # -------------------------------------------------------------------------
    def test_03_blind_double_marking_and_reconciliation(self):
        """Verifies blind review protection, criterion disagreement detection, and reconciliation."""
        dm = self.double_marking_mgr.create_double_marking_pair(
            submission_id="sub_dm_301",
            submission_type="writing",
            learner_id=self.learner["id"],
            content_json={"task_type": "task_1", "essay_text": "The line graph demonstrates industrial emissions..."},
            reviewer_1_id=self.examiner_1["id"],
            reviewer_2_id=self.examiner_2["id"],
            task_type="task_1",
            track="Academic"
        )
        self.assertTrue(dm["success"])

        # Examiner 1 submits Band 6.0
        self.review_mgr.save_evaluation(
            assignment_id=dm["assignment_1_id"],
            reviewer_id=self.examiner_1["id"],
            reviewer_role="examiner",
            overall_band=6.0,
            criteria_scores={"task_achievement": 6.0, "coherence_cohesion": 6.0, "lexical_resource": 6.0, "grammatical_accuracy": 6.0}
        )

        # Blind Check: Examiner 2 cannot see Examiner 1's evaluation before submitting
        blind_view = self.double_marking_mgr.get_double_marked_evaluations(
            submission_id="sub_dm_301",
            requesting_reviewer_id=self.examiner_2["id"],
            user_role="examiner"
        )
        self.assertEqual(len(blind_view["evaluations"]), 0)

        # Examiner 2 submits Band 7.5 (1.5 band difference!)
        self.review_mgr.save_evaluation(
            assignment_id=dm["assignment_2_id"],
            reviewer_id=self.examiner_2["id"],
            reviewer_role="examiner",
            overall_band=7.5,
            criteria_scores={"task_achievement": 7.5, "coherence_cohesion": 7.5, "lexical_resource": 7.0, "grammatical_accuracy": 8.0}
        )

        # Both now visible
        both = self.double_marking_mgr.get_double_marked_evaluations("sub_dm_301", user_role="admin")
        self.assertEqual(len(both["evaluations"]), 2)

        # Calculate disagreement: overall difference = 1.5 bands, exceeds 0.5 threshold
        disag = self.double_marking_mgr.calculate_disagreement(
            both["evaluations"][0], both["evaluations"][1], threshold=0.5
        )
        self.assertEqual(disag["overall_difference"], 1.5)
        self.assertTrue(disag["requires_reconciliation"])
        self.assertGreater(len(disag["alerts"]), 0)

        # Senior Examiner reconciles to agreed consensus Band 6.5
        recon = self.double_marking_mgr.submit_reconciliation(
            submission_id="sub_dm_301",
            reconciler_id=self.admin_user["id"],
            reconciled_band=6.5,
            reconciled_criteria={"task_achievement": 6.5, "coherence_cohesion": 6.5, "lexical_resource": 6.5, "grammatical_accuracy": 6.5},
            comments="Senior examiner review: Overview is present but data comparisons in paragraph 2 are incomplete."
        )
        self.assertTrue(recon["success"])
        self.assertEqual(recon["reconciled_band"], 6.5)

        # Verify that original Examiner 1 and Examiner 2 marks are still preserved
        check_after = self.double_marking_mgr.get_double_marked_evaluations("sub_dm_301", user_role="admin")
        self.assertEqual(len(check_after["evaluations"]), 2)
        self.assertIsNotNone(check_after["reconciled_evaluation"])
        self.assertEqual(check_after["reconciled_evaluation"]["overall_band"], 6.5)

    # -------------------------------------------------------------------------
    # 4. SPEAKING REVIEW MODALITY
    # -------------------------------------------------------------------------
    def test_04_speaking_review_modality_and_pronunciation(self):
        """Verifies that speaking evaluation explicitly records assessment mode (audio vs transcript)."""
        assign = self.review_mgr.create_assignment(
            submission_id="sub_spk_401",
            submission_type="speaking",
            learner_id=self.learner["id"],
            content_json={"transcript": "I like living in my hometown because it is historic..."},
            assigned_to=self.examiner_1["id"],
            assigned_role="examiner",
            task_type="speaking_full"
        )
        aid = assign["assignment_id"]

        eval_spk = self.review_mgr.save_evaluation(
            assignment_id=aid,
            reviewer_id=self.examiner_1["id"],
            reviewer_role="examiner",
            overall_band=6.5,
            criteria_scores={"fluency_coherence": 6.5, "lexical_resource": 7.0, "grammatical_accuracy": 6.5, "pronunciation": 6.0},
            assessment_mode="transcript",
            general_comments="Assessed via transcript only. Pronunciation score is a nominal placeholder."
        )
        self.assertTrue(eval_spk["success"])

        stored = self.review_mgr.get_evaluation(eval_spk["evaluation_id"])
        self.assertEqual(stored["assessment_mode"], "transcript")
        self.assertEqual(stored["criteria_scores"]["pronunciation"], 6.0)

    # -------------------------------------------------------------------------
    # 5. BENCHMARK DATASET & CONSENT COMPLIANCE
    # -------------------------------------------------------------------------
    def test_05_benchmark_dataset_anonymization_and_consent(self):
        """Verifies PII redaction and consent withdrawal for benchmark records."""
        # 1. Deny enrollment without consent
        no_consent = self.benchmark_mgr.enroll_benchmark_submission(
            assessment_type="writing",
            content="Hello world",
            has_consent=False
        )
        self.assertFalse(no_consent["success"])
        self.assertIn("consent is required", no_consent["error"].lower())

        # 2. Enroll with consent and verify PII anonymization
        raw_text = "Dear Mr. Davis, I am writing to you. You can contact me at candidate_test@gama.internal or 555-0199."
        enrolled = self.benchmark_mgr.enroll_benchmark_submission(
            assessment_type="writing",
            content=raw_text,
            task_type="gt_t1_airline_complaint",
            track="General Training",
            has_consent=True
        )
        self.assertTrue(enrolled["success"])
        bid = enrolled["benchmark_id"]

        rec = self.benchmark_mgr.get_benchmark_record(bid)
        self.assertNotIn("candidate_test@gama.internal", rec["anonymized_content"])
        self.assertIn("[EMAIL REDACTED]", rec["anonymized_content"])

        # 3. Withdraw consent
        withdrawn = self.benchmark_mgr.withdraw_consent(bid)
        self.assertTrue(withdrawn["success"])
        rec_after = self.benchmark_mgr.get_benchmark_record(bid)
        self.assertEqual(rec_after["consent_status"], "withdrawn")
        self.assertIn("WITHDRAWN", rec_after["anonymized_content"])

    # -------------------------------------------------------------------------
    # 6. CALIBRATION STATISTICAL INTEGRITY (HONEST ZERO-STATE)
    # -------------------------------------------------------------------------
    def test_06_calibration_engine_honest_zero_state(self):
        """Verifies that calibration analysis returns an honest pending status when N = 0."""
        # Query calibration for speaking (0 enrolled human consensus records)
        calib_res = self.calibration_engine.run_calibration_analysis(assessment_type="speaking")
        self.assertEqual(calib_res["status"], "pending_human_calibration")
        self.assertEqual(calib_res["valid_samples"], 0)
        self.assertIsNone(calib_res["metrics"])
        self.assertIn("Human calibration data not yet available", calib_res["message"])

    # -------------------------------------------------------------------------
    # 7. CONTROLLED BETA MANAGEMENT & FEEDBACK
    # -------------------------------------------------------------------------
    def test_07_beta_cohorts_and_feedback_categories(self):
        """Tests cohort listing, participant enrollment with consent, and 11 feedback categories."""
        cohorts = self.beta_mgr.list_cohorts()
        self.assertGreaterEqual(len(cohorts), 4)

        target_cohort = cohorts[0]["id"]

        # Enroll participant
        enrolled = self.beta_mgr.enroll_participant(
            cohort_id=target_cohort,
            user_id=self.learner_user["id"],
            email=self.learner_user["email"],
            has_consent=True
        )
        self.assertTrue(enrolled["success"])

        # Duplicate enrollment prevented
        dup = self.beta_mgr.enroll_participant(cohort_id=target_cohort, user_id=self.learner_user["id"])
        self.assertFalse(dup["success"])
        self.assertIn("already enrolled", dup["error"].lower())

        # Submit feedback across valid category
        fb = self.beta_mgr.submit_feedback(
            cohort_id=target_cohort,
            category="writing",
            rating=5,
            comments="The dual task weighting and PEEL blueprint are very helpful.",
            participant_id=enrolled["participant_id"]
        )
        self.assertTrue(fb["success"])

        # Invalid category rejected
        bad_fb = self.beta_mgr.submit_feedback(cohort_id=target_cohort, category="invalid_cat", rating=5, comments="test")
        self.assertFalse(bad_fb["success"])

        # Report bug
        bug = self.beta_mgr.report_bug(
            cohort_id=target_cohort,
            title="Audio button label",
            description="Button resets smoothly but could show pause icon.",
            severity="low"
        )
        self.assertTrue(bug["success"])
        self.assertEqual(bug["severity"], "low")

        # Verify analytics compilation
        analytics = self.beta_mgr.get_beta_analytics()
        self.assertGreater(analytics["total_participants"], 0)
        self.assertIn("writing", analytics["ratings_by_category"])


if __name__ == "__main__":
    unittest.main()
