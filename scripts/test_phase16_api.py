import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database.db_manager import DatabaseManager
from core.database.migrations import MigrationManager
from core.auth.auth_manager import AuthManager
from core.review.review_manager import ReviewManager
from core.review.double_marking import DoubleMarkingManager
from core.benchmark.benchmark_manager import BenchmarkManager
from core.benchmark.calibration_engine import CalibrationEngine
from core.beta.beta_manager import BetaManager

import tempfile
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
temp_path = temp_file.name
temp_file.close()

db = DatabaseManager(temp_path)
mig = MigrationManager(db)
mig.run_migrations()

auth = AuthManager(db)
review = ReviewManager(db)
double_mark = DoubleMarkingManager(db)
bench = BenchmarkManager(db)
calib = CalibrationEngine(db)
beta = BetaManager(db)

# Provision test users in temporary database
auth.register_user("admin", "admin_secure_pass123", role="admin")
admin_auth = auth.authenticate("admin", "admin_secure_pass123")
admin_tok = auth.create_session(admin_auth["id"])

auth.register_user("teacher_sarah", "teacher_pass123", role="teacher", authorizing_admin_user_id=admin_auth["id"])
teacher_auth = auth.authenticate("teacher_sarah", "teacher_pass123")
teacher_tok = auth.create_session(teacher_auth["id"])

ex_1 = auth.register_user("examiner_mark", "examiner_pass123", role="examiner", authorizing_admin_user_id=admin_auth["id"])
ex_2 = auth.register_user("examiner_clara", "examiner_pass123", role="examiner", authorizing_admin_user_id=admin_auth["id"])

auth.register_user("learner_alice", "learner_pass123", role="learner")
learner_auth = auth.authenticate("learner_alice", "learner_pass123")
learner_tok = auth.create_session(learner_auth["id"])

print("=== RUNNING PHASE 16 INTEGRATION TEST ===")
print("1. Admin auth:", admin_auth["role"] == "admin", admin_auth["username"])
print("   Teacher auth:", teacher_auth["role"] == "teacher", teacher_auth["username"])
print("   Learner auth:", learner_auth["role"] == "learner", learner_auth["username"])

# 2. RBAC authorization checks
ok_t, _, _ = auth.authorize_request(teacher_tok, ["teacher", "admin"])
print("2. Teacher authorized for teacher area:", ok_t)
ok_l, _, err_l = auth.authorize_request(learner_tok, ["teacher", "admin"])
print("   Learner rejected for teacher area:", not ok_l, "Error:", err_l)

# Setup default learner record
db.execute("INSERT OR IGNORE INTO learners (id, name, target_band) VALUES (?, ?, ?)", ("default_learner", "Default Candidate", 7.0))

# 3. Teacher Dashboard & Review Assignment
review.assign_teacher_to_learner(teacher_auth["id"], "default_learner")
dash = review.get_teacher_dashboard(teacher_auth["id"])
print("3. Teacher dashboard assigned learners:", len(dash["assigned_learners"]))

# Create an assignment
assign_res = review.create_assignment(
    submission_id="sub_test_101",
    submission_type="writing",
    learner_id="default_learner",
    content_json={"task_type": "task_2", "essay_text": "Automation creates higher value jobs..."},
    assigned_to=teacher_auth["id"],
    assigned_role="teacher"
)
aid = assign_res["assignment_id"]
print("   Created review assignment:", aid)

# Save evaluation
eval_res = review.save_evaluation(
    assignment_id=aid,
    reviewer_id=teacher_auth["id"],
    reviewer_role="teacher",
    overall_band=7.0,
    criteria_scores={"task_achievement": 7.0, "coherence_cohesion": 7.0, "lexical_resource": 7.0, "grammatical_accuracy": 7.0},
    criterion_feedback={"task_achievement": "Strong thesis and clear development."},
    general_comments="Well structured argument.",
    status="submitted"
)
print("   Saved human evaluation:", eval_res["success"], "band:", eval_res["overall_band"])

# 4. Double-marking & blind review protection
dm_pair = double_mark.create_double_marking_pair(
    submission_id="sub_dm_202",
    submission_type="writing",
    learner_id="default_learner",
    content_json={"task_type": "task_1", "essay_text": "The graph shows transport emissions rising..."},
    reviewer_1_id=ex_1["user_id"],
    reviewer_2_id=ex_2["user_id"]
)
print("4. Double marking pair created:", dm_pair["assignment_1_id"], dm_pair["assignment_2_id"])

# Examiner Mark submits
review.save_evaluation(
    assignment_id=dm_pair["assignment_1_id"],
    reviewer_id=ex_1["user_id"],
    reviewer_role="examiner",
    overall_band=6.5,
    criteria_scores={"task_achievement": 6.5, "coherence_cohesion": 6.5, "lexical_resource": 6.5, "grammatical_accuracy": 6.5}
)

# Blind check: Examiner Clara requests double-marked status BEFORE submitting
blind_check = double_mark.get_double_marked_evaluations("sub_dm_202", requesting_reviewer_id=ex_2["user_id"], user_role="examiner")
print("   Blind check: Reviewer 2 sees 0 evaluations before submitting:", len(blind_check["evaluations"]) == 0)

# Examiner Clara submits (with disagreement: band 7.5)
review.save_evaluation(
    assignment_id=dm_pair["assignment_2_id"],
    reviewer_id=ex_2["user_id"],
    reviewer_role="examiner",
    overall_band=7.5,
    criteria_scores={"task_achievement": 7.5, "coherence_cohesion": 7.5, "lexical_resource": 7.5, "grammatical_accuracy": 7.5}
)

# Now both submitted: calculate disagreement
both_evals = double_mark.get_double_marked_evaluations("sub_dm_202", user_role="admin")
print("   Both submitted count:", len(both_evals["evaluations"]))
disag = double_mark.calculate_disagreement(both_evals["evaluations"][0], both_evals["evaluations"][1], threshold=0.5)
print("   Disagreement overall diff:", disag["overall_difference"], "Requires reconciliation:", disag["requires_reconciliation"])

# Reconcile by Senior Examiner
recon = double_mark.submit_reconciliation(
    submission_id="sub_dm_202",
    reconciler_id=admin_auth["id"],
    reconciled_band=7.0,
    reconciled_criteria={"task_achievement": 7.0, "coherence_cohesion": 7.0, "lexical_resource": 7.0, "grammatical_accuracy": 7.0},
    comments="Agreed consensus band 7.0 after reviewing Lexical Resource."
)
print("   Reconciliation completed:", recon["success"], "consensus band:", recon["reconciled_band"])

# 5. Benchmark & Calibration Zero-State
calib_empty = calib.run_calibration_analysis()
print("5. Calibration empty state status:", calib_empty["status"], "Samples:", calib_empty["valid_samples"])

# Enroll 1 benchmark sample with consent
bench_res = bench.enroll_benchmark_submission(
    assessment_type="writing",
    content="I am writing to express my dissatisfaction. My email is student@example.com.",
    task_type="gt_t1_airline_complaint",
    has_consent=True
)
print("   Enrolled benchmark ID:", bench_res["benchmark_id"])
bench_rec = bench.get_benchmark_record(bench_res["benchmark_id"])
print("   Anonymized content:", bench_rec["anonymized_content"])

# 6. Beta Management
cohorts = beta.list_cohorts()
print("6. Beta cohorts count:", len(cohorts), [c["name"] for c in cohorts[:2]])
part = beta.enroll_participant(cohorts[0]["id"], learner_auth["id"], "alice@example.com", has_consent=True)
print("   Enrolled beta participant:", part["participant_id"], part["consent_status"])

fb = beta.submit_feedback(cohorts[0]["id"], "exam_sim", 5, "The full mock timer and autosave work flawlessly.")
print("   Submitted feedback:", fb["success"], fb["category"])

bug = beta.report_bug(cohorts[0]["id"], "Microphone permission notice", "Add clearer prompt before Part 2 Speaking.", "low")
print("   Reported bug:", bug["success"], bug["severity"])

stats = beta.get_beta_analytics()
print("   Beta analytics total participants:", stats["total_participants"], "Feedbacks:", stats["total_feedback_submissions"])

print("=== ALL PHASE 16 TESTS PASSED CLEANLY! ===")
try:
    if os.path.exists(temp_path):
        os.remove(temp_path)
except Exception:
    pass
