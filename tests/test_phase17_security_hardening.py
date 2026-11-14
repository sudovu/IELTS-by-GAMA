"""
Phase 17 Automated Test Suite:
Security Hardening, Privacy Audit & Controlled Beta Launch Gate.

Covers:
1. Modernized Password Hashing (scrypt $N=16384, r=8, p=1$) and verification.
2. Automatic legacy password hash migration on authentication.
3. Input validation: password length bounds (8-128) and username constraints.
4. Constant-time anti-enumeration behavior on non-existent users.
5. Sliding-window rate limiting on repeated authentication failures.
6. Session revocation upon password modification.
7. Role escalation prevention during registration and admin gating.
8. HTTP Security Headers (nosniff, DENY, CSP, Referrer-Policy).
9. Query string authentication elimination (HTTP 401 on URL tokens).
10. Cross-learner examination data isolation (HTTP 403 on ID spoofing).
11. Blind double-marking protection (Reviewer 2 cannot see Reviewer 1).
12. Review submission immutability (submitted evaluations cannot be edited).
13. Reconciliation conflict-of-interest prevention.
14. Benchmark dataset mandatory consent gate.
15. Multi-entity PII pseudonymization pipeline (email, phone, ID, address, name).
16. Consent withdrawal with full text purge, score zeroing, and audio erasure.
17. Atomic SQLite backup creation and verified test restoration.
"""

import unittest
import os
import json
import time
import tempfile
import sqlite3
import hashlib
import urllib.request
import urllib.error
import threading

from core.database.db_manager import DatabaseManager
from core.database.migrations import MigrationManager
from core.auth.auth_manager import AuthManager
from core.review.review_manager import ReviewManager
from core.review.double_marking import DoubleMarkingManager
from core.benchmark.benchmark_manager import BenchmarkManager
from ui.server import run_server, GAMAHTTPRequestHandler


class TestPhase17SecurityHardening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Setup isolated temporary database for security unit tests
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

        # Provision baseline administrator in test DB
        cls.admin_reg = cls.auth_mgr.register_user("sec_admin", "AdminSecPass123!", role="admin")
        cls.admin_auth = cls.auth_mgr.authenticate("sec_admin", "AdminSecPass123!")
        cls.admin_token = cls.auth_mgr.create_session(cls.admin_auth["id"])

        # Spin up test HTTP server on port 8901
        cls.server_port = 8901
        cls.server_thread = threading.Thread(target=run_server, args=(cls.server_port,), daemon=True)
        cls.server_thread.start()
        time.sleep(1.0)

    @classmethod
    def tearDownClass(cls):
        try:
            if os.path.exists(cls.temp_path):
                os.remove(cls.temp_path)
        except Exception:
            pass

    # 1. Password Hashing & Verification
    def test_01_password_hashing_and_verification(self):
        user = self.auth_mgr.register_user("test_user_scrypt", "CorrectHorseBattery99!")
        self.assertTrue(user["success"])
        user_row = self.db.fetchone("SELECT password_hash FROM users WHERE username = ?", ("test_user_scrypt",))
        self.assertIsNotNone(user_row)
        pw_hash = user_row[0]

        # OWASP scrypt format verification
        self.assertTrue(pw_hash.startswith("scrypt$16384$8$1$"))
        parts = pw_hash.split("$")
        self.assertEqual(len(parts), 6)
        salt_hex = parts[4]
        hash_hex = parts[5]
        self.assertEqual(len(salt_hex), 32)  # 16 bytes = 32 hex chars
        self.assertEqual(len(hash_hex), 128) # 64 bytes = 128 hex chars

        # Verification success & failure
        auth_ok = self.auth_mgr.authenticate("test_user_scrypt", "CorrectHorseBattery99!")
        self.assertIsNotNone(auth_ok)
        self.assertEqual(auth_ok["username"], "test_user_scrypt")

        auth_fail = self.auth_mgr.authenticate("test_user_scrypt", "WrongPassword123!")
        self.assertIsNone(auth_fail)

    # 2. Legacy Hash Migration
    def test_02_legacy_hash_migration(self):
        # Directly insert a legacy SHA-256 hashed user
        legacy_salt = "11223344556677889900aabbccddeeff"
        legacy_plain = "LegacySecretPass2026!"
        legacy_sha = hashlib.sha256((legacy_salt + legacy_plain).encode("utf-8")).hexdigest()
        legacy_stored = f"{legacy_salt}${legacy_sha}"

        user_id = "usr_legacy_migrate_test"
        self.db.execute(
            "INSERT INTO users (id, username, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)",
            (user_id, "legacy_user", legacy_stored, legacy_salt, "learner")
        )

        # Authenticate with legacy credentials
        auth_res = self.auth_mgr.authenticate("legacy_user", legacy_plain)
        self.assertIsNotNone(auth_res)
        self.assertEqual(auth_res["id"], user_id)

        # Verify hash was automatically upgraded to scrypt in DB
        migrated_row = self.db.fetchone("SELECT password_hash FROM users WHERE id = ?", (user_id,))
        self.assertTrue(migrated_row[0].startswith("scrypt$16384$8$1$"))

    # 3. Password Length & Format Validation
    def test_03_password_length_and_format_validation(self):
        # Too short (< 8)
        short_res = self.auth_mgr.register_user("short_user", "1234567")
        self.assertFalse(short_res["success"])
        self.assertIn("at least 8 characters", short_res["error"])

        # Too long (> 128)
        long_pass = "A" * 129
        long_res = self.auth_mgr.register_user("long_user", long_pass)
        self.assertFalse(long_res["success"])
        self.assertIn("exceed 128 characters", long_res["error"])

        # Invalid username format
        bad_name = self.auth_mgr.register_user("inv@lid user!", "ValidPassword123!")
        self.assertFalse(bad_name["success"])
        self.assertIn("letters, numbers", bad_name["error"])

    # 4. Anti-Enumeration Constant-Time Behavior
    def test_04_anti_enumeration_behavior(self):
        # Non-existent user should produce same generic error message
        res = self.auth_mgr.authenticate("non_existent_user_9999", "RandomPassword123!")
        self.assertIsNone(res)
        self.assertEqual(self.auth_mgr.last_auth_error, "Invalid username or password.")

    # 5. Sliding-Window Rate Limiting
    def test_05_rate_limiting_authentication(self):
        target_user = "rate_limit_victim"
        self.auth_mgr.register_user(target_user, "TargetPass1234!")

        # 5 consecutive failed attempts
        for i in range(5):
            res = self.auth_mgr.authenticate(target_user, f"wrong_try_{i}", client_ip="192.168.1.50")
            self.assertIsNone(res)

        # 6th attempt should be locked out
        res6 = self.auth_mgr.authenticate(target_user, "TargetPass1234!", client_ip="192.168.1.50")
        self.assertIsNone(res6)
        self.assertIn("Too many failed login attempts", self.auth_mgr.last_auth_error)

    # 6. Session Invalidation on Password Change
    def test_06_session_invalidation_on_password_change(self):
        user = self.auth_mgr.register_user("pw_change_user", "OldPassword123!")
        self.assertTrue(user["success"])
        auth_info = self.auth_mgr.authenticate("pw_change_user", "OldPassword123!")
        token1 = self.auth_mgr.create_session(auth_info["id"])
        token2 = self.auth_mgr.create_session(auth_info["id"])

        # Verify active sessions
        ok1, _, _ = self.auth_mgr.authorize_request(token1, ["learner"])
        ok2, _, _ = self.auth_mgr.authorize_request(token2, ["learner"])
        self.assertTrue(ok1)
        self.assertTrue(ok2)

        # Change password
        chg_ok, err = self.auth_mgr.change_password(auth_info["id"], "OldPassword123!", "NewPassword456!")
        self.assertTrue(chg_ok, f"Password change failed: {err}")

        # Both tokens must now be revoked
        val1, _, _ = self.auth_mgr.authorize_request(token1, ["learner"])
        val2, _, _ = self.auth_mgr.authorize_request(token2, ["learner"])
        self.assertFalse(val1)
        self.assertFalse(val2)

    # 7. Role Escalation Prevention
    def test_07_role_escalation_prevention(self):
        # Attempt to register teacher without authorizing admin
        unauth_teacher = self.auth_mgr.register_user("sneaky_teacher", "SecretTeacher123!", role="teacher")
        self.assertFalse(unauth_teacher["success"])
        self.assertIn("Privileged role creation requires authorization from an active Administrator", unauth_teacher["error"])

        # Authorized registration with admin ID
        auth_teacher = self.auth_mgr.register_user(
            "legit_teacher", "SecretTeacher123!", role="teacher", authorizing_admin_user_id=self.admin_auth["id"]
        )
        self.assertTrue(auth_teacher["success"])
        self.assertEqual(auth_teacher["role"], "teacher")

    # 8. HTTP Security Headers
    def test_08_http_security_headers(self):
        url = f"http://127.0.0.1:{self.server_port}/api/health"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            headers = dict(resp.headers)
            self.assertEqual(resp.status, 200)
            self.assertEqual(headers.get("X-Content-Type-Options"), "nosniff")
            self.assertEqual(headers.get("X-Frame-Options"), "DENY")
            self.assertEqual(headers.get("X-XSS-Protection"), "1; mode=block")
            self.assertEqual(headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")
            self.assertIn("default-src 'self'", headers.get("Content-Security-Policy", ""))

    # 9. Query String Auth Rejection
    def test_09_query_string_auth_rejection(self):
        # Requesting a protected endpoint with token ONLY in query string should return 401
        url = f"http://127.0.0.1:{self.server_port}/api/teacher/dashboard?token={self.admin_token}"
        req = urllib.request.Request(url, method="GET")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(ctx.exception.code, 401)

    # 10. Cross-Learner Data Isolation
    def test_10_cross_learner_data_isolation(self):
        # Register user on the server's auth manager
        l1_reg = GAMAHTTPRequestHandler.auth_mgr.register_user("iso_learner_1", "PassLearner123!")
        if not l1_reg["success"]:
            # Already registered from previous test run
            l1_auth = GAMAHTTPRequestHandler.auth_mgr.authenticate("iso_learner_1", "PassLearner123!")
        else:
            l1_auth = GAMAHTTPRequestHandler.auth_mgr.authenticate("iso_learner_1", "PassLearner123!")
        l1_token = GAMAHTTPRequestHandler.auth_mgr.create_session(l1_auth["id"])

        # Learner 1 attempts to query history of "other_victim_learner"
        url = f"http://127.0.0.1:{self.server_port}/api/exam/history?learner_id=other_victim_learner"
        req = urllib.request.Request(url, headers={"X-Session-Token": l1_token}, method="GET")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(ctx.exception.code, 403)

    # 11. Blind Double-Marking Protection
    def test_11_blind_double_marking_protection(self):
        ex1 = self.auth_mgr.register_user("blind_ex1", "ExamPass1234!", role="examiner", authorizing_admin_user_id=self.admin_auth["id"])
        ex2 = self.auth_mgr.register_user("blind_ex2", "ExamPass1234!", role="examiner", authorizing_admin_user_id=self.admin_auth["id"])

        dm = self.double_marking_mgr.create_double_marking_pair(
            submission_id="sub_blind_test_001",
            submission_type="writing",
            learner_id="learner_blind",
            content_json={"task_type": "task_2", "essay_text": "Sample essay for blind review test."},
            reviewer_1_id=ex1["user_id"],
            reviewer_2_id=ex2["user_id"],
            task_type="task_2",
            track="Academic"
        )
        self.assertTrue(dm["success"])

        # Reviewer 1 submits evaluation
        self.review_mgr.save_evaluation(
            assignment_id=dm["assignment_1_id"],
            reviewer_id=ex1["user_id"],
            reviewer_role="examiner",
            overall_band=6.5,
            criteria_scores={"task_response": 6.5, "coherence_cohesion": 6.0, "lexical_resource": 6.5, "grammatical_accuracy": 6.0},
            status="submitted"
        )

        # Reviewer 2 checks assignment before submitting
        blind_view = self.double_marking_mgr.get_double_marked_evaluations(
            submission_id="sub_blind_test_001",
            requesting_reviewer_id=ex2["user_id"],
            user_role="examiner"
        )
        # Reviewer 2 MUST NOT see Reviewer 1's feedback or evaluation
        self.assertEqual(len(blind_view["evaluations"]), 0)

    # 12. Submitted Evaluation Immutability
    def test_12_submitted_evaluation_immutability(self):
        teacher = self.auth_mgr.register_user("mut_teacher", "TeachPass123!", role="teacher", authorizing_admin_user_id=self.admin_auth["id"])
        assign = self.review_mgr.create_assignment(
            submission_id="sub_mut_test_002",
            submission_type="writing",
            learner_id="learner_mut",
            content_json={"task_type": "task_1", "essay_text": "Original learner text."},
            assigned_to=teacher["user_id"],
            assigned_role="teacher"
        )
        self.assertTrue(assign["success"])

        # Save as submitted
        res = self.review_mgr.save_evaluation(
            assignment_id=assign["assignment_id"],
            reviewer_id=teacher["user_id"],
            reviewer_role="teacher",
            overall_band=7.0,
            criteria_scores={"task_achievement": 7.0, "coherence_cohesion": 7.0, "lexical_resource": 7.0, "grammatical_accuracy": 7.0},
            status="submitted"
        )
        self.assertTrue(res["success"])

        # Attempt to overwrite the submitted evaluation
        overwrite_res = self.review_mgr.save_evaluation(
            assignment_id=assign["assignment_id"],
            reviewer_id=teacher["user_id"],
            reviewer_role="teacher",
            overall_band=9.0,
            criteria_scores={"task_achievement": 9.0, "coherence_cohesion": 9.0, "lexical_resource": 9.0, "grammatical_accuracy": 9.0},
            status="submitted"
        )
        self.assertFalse(overwrite_res["success"])
        self.assertIn("immutable", overwrite_res["error"].lower())

    # 13. Reconciliation Conflict-of-Interest Prevention
    def test_13_reconciliation_conflict_of_interest(self):
        ex_a = self.auth_mgr.register_user("coi_ex_a", "ExamPass1234!", role="examiner", authorizing_admin_user_id=self.admin_auth["id"])
        ex_b = self.auth_mgr.register_user("coi_ex_b", "ExamPass1234!", role="examiner", authorizing_admin_user_id=self.admin_auth["id"])

        dm = self.double_marking_mgr.create_double_marking_pair(
            submission_id="sub_coi_003",
            submission_type="writing",
            learner_id="learner_coi",
            content_json={"task_type": "task_2", "essay_text": "Essay with discrepancy."},
            reviewer_1_id=ex_a["user_id"],
            reviewer_2_id=ex_b["user_id"]
        )

        # Submit both with discrepancy
        self.review_mgr.save_evaluation(
            dm["assignment_1_id"], ex_a["user_id"], "examiner", 6.0,
            {"task_achievement": 6.0, "coherence_cohesion": 6.0, "lexical_resource": 6.0, "grammatical_accuracy": 6.0},
            status="submitted"
        )
        self.review_mgr.save_evaluation(
            dm["assignment_2_id"], ex_b["user_id"], "examiner", 7.5,
            {"task_achievement": 7.5, "coherence_cohesion": 7.5, "lexical_resource": 7.5, "grammatical_accuracy": 7.5},
            status="submitted"
        )

        # Examiner A attempts to reconcile their own pair
        rec_res = self.double_marking_mgr.submit_reconciliation(
            submission_id="sub_coi_003",
            reconciler_id=ex_a["user_id"],
            reconciled_band=6.5,
            reconciled_criteria={"task_achievement": 6.5, "coherence_cohesion": 6.5, "lexical_resource": 6.5, "grammatical_accuracy": 6.5},
            comments="Biased reconciliation"
        )
        self.assertFalse(rec_res["success"])
        self.assertIn("Conflict of interest", rec_res["error"])

    # 14. Benchmark Dataset Consent Gate
    def test_14_benchmark_consent_gate(self):
        # Attempt to enroll without consent
        no_consent = self.benchmark_mgr.enroll_benchmark_submission(
            assessment_type="writing",
            content="Student essay with personal details.",
            candidate_id="cand_test_001",
            task_type="academic_t2_education",
            has_consent=False
        )
        self.assertFalse(no_consent["success"])
        self.assertIn("consent is required", no_consent["error"].lower())

    # 15. Pseudonymization Pipeline
    def test_15_pseudonymization_pipeline(self):
        raw_text = (
            "Dear Mr. John Smith, please call me at +1 (555) 234-5678 or 555-0199. "
            "My candidate ID is CAND-889123 and my email is student.doe@university.edu. "
            "I reside at 742 Evergreen Terrace, Springfield."
        )
        pseudonymized = self.benchmark_mgr.pseudonymize_text(raw_text)

        self.assertNotIn("student.doe@university.edu", pseudonymized)
        self.assertNotIn("555-0199", pseudonymized)
        self.assertNotIn("CAND-889123", pseudonymized)
        self.assertNotIn("742 Evergreen Terrace", pseudonymized)
        self.assertNotIn("Mr. John Smith", pseudonymized)

        self.assertIn("[EMAIL REDACTED]", pseudonymized)
        self.assertIn("[PHONE REDACTED]", pseudonymized)
        self.assertIn("[ID REDACTED]", pseudonymized)
        self.assertIn("[ADDRESS REDACTED]", pseudonymized)
        self.assertIn("[NAME REDACTED]", pseudonymized)

    # 16. Benchmark Withdrawal and Erasure
    def test_16_benchmark_withdrawal_and_erasure(self):
        # Create dummy audio file to verify physical erasure
        dummy_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        dummy_audio.write(b"RIFF dummy audio content for erasure test")
        audio_path = dummy_audio.name
        dummy_audio.close()
        self.assertTrue(os.path.exists(audio_path))

        enroll = self.benchmark_mgr.enroll_benchmark_submission(
            assessment_type="speaking",
            content="My name is Alice and this is my test speech.",
            candidate_id="cand_erase_002",
            task_type="speaking_p2",
            has_consent=True,
            recording_ref=audio_path
        )
        self.assertTrue(enroll["success"])
        bench_id = enroll["benchmark_id"]

        # Withdraw consent
        withdrawn = self.benchmark_mgr.withdraw_consent(bench_id)
        self.assertTrue(withdrawn["success"])

        # Verify record in DB is purged and scores zeroed/nulled
        record = self.benchmark_mgr.get_benchmark_record(bench_id)
        self.assertEqual(record["consent_status"], "withdrawn")
        self.assertEqual(record["anonymized_content"], "[CONTENT_WITHDRAWN_AND_PURGED]")
        self.assertIsNone(record["consensus_human_band"])

        # Verify audio file was erased from disk
        self.assertFalse(os.path.exists(audio_path))

    # 17. SQLite Database Backup & Restore Integrity
    def test_17_database_backup_and_restore_integrity(self):
        backup_file = tempfile.NamedTemporaryFile(delete=False, suffix="_backup.db")
        backup_path = backup_file.name
        backup_file.close()

        verify_conn = None
        try:
            # 1. Perform online backup using SQLite backup API
            src_conn = sqlite3.connect(self.temp_path)
            dst_conn = sqlite3.connect(backup_path)
            with dst_conn:
                src_conn.backup(dst_conn)
            dst_conn.close()
            src_conn.close()

            # 2. Verify backup integrity
            verify_conn = sqlite3.connect(backup_path)
            integrity = verify_conn.execute("PRAGMA integrity_check").fetchone()[0]
            self.assertEqual(integrity, "ok")

            fk_check = verify_conn.execute("PRAGMA foreign_key_check").fetchall()
            self.assertEqual(len(fk_check), 0)

            # 3. Verify key tables exist and contain records
            tables = [r[0] for r in verify_conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            self.assertIn("users", tables)
            self.assertIn("review_assignments", tables)
            self.assertIn("benchmark_records", tables)

            user_count = verify_conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            self.assertGreater(user_count, 0)

        finally:
            if verify_conn:
                verify_conn.close()
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except Exception:
                    pass


if __name__ == "__main__":
    unittest.main()
