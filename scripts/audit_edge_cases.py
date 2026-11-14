import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database.db_manager import DatabaseManager
from core.exam.exam_manager import ExamManager

db = DatabaseManager('data/ielts_gama.db')
mgr = ExamManager(db)

print("--- SECURITY AUDIT: EDGE CASES ---")

# 1. Invalid session ID
res1 = mgr.submit_exam("invalid_session_123", "default_learner")
print("1. Invalid session ID:", res1)

# 2. Cross-learner submission
sess2 = mgr.start_exam("learner_alice", "Academic", "reading")
sid2 = sess2["session_id"]
res2 = mgr.submit_exam(sid2, "learner_bob")
print("2. Cross-learner submission:", res2)

# 3. Duplicate submission
res3_first = mgr.submit_exam(sid2, "learner_alice", {"read_1": "TRUE"})
res3_dup = mgr.submit_exam(sid2, "learner_alice", {"read_1": "FALSE"})
print("3. First submit success:", res3_first.get("success"), "Duplicate submit:", res3_dup.get("already_submitted"))
# Check if answers were modified by duplicate submit
res3_check = mgr.get_exam_results(sid2, "learner_alice")
saved_q1 = res3_check["results"]["skills"]["reading"]["questions"][0]["user_answer"]
print("   Q1 answer after duplicate submit attempt (should remain 'TRUE'):", saved_q1)

# 4. Autosave after submit
res4 = mgr.autosave_answers(sid2, "learner_alice", {"read_1": "FALSE"})
print("4. Autosave after submission:", res4)

# 5. Malformed answers (e.g. integer or list as answers dict)
sess5 = mgr.start_exam("learner_charlie", "Academic", "reading")
sid5 = sess5["session_id"]
try:
    res5 = mgr.autosave_answers(sid5, "learner_charlie", ["not", "a", "dict"])
    print("5. Malformed answers type:", res5)
except Exception as e:
    print("5. Malformed answers exception:", type(e), e)

# Clean up test sessions
db.execute("DELETE FROM exam_sessions WHERE learner_id IN ('learner_alice', 'learner_bob', 'learner_charlie')")
