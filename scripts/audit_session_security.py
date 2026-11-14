import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database.db_manager import DatabaseManager
from core.exam.exam_manager import ExamManager

db = DatabaseManager('data/ielts_gama.db')
mgr = ExamManager(db)

# Test 1: Abandoned session submission
sess = mgr.start_exam('test_learner_sec', 'Academic', 'reading')
sid = sess['session_id']
db.execute("UPDATE exam_sessions SET status = 'abandoned' WHERE id = ?", (sid,))
res = mgr.submit_exam(sid, 'test_learner_sec')
row = db.fetchone("SELECT status FROM exam_sessions WHERE id = ?", (sid,))
print("Test 1 - Submit abandoned session:")
print("  API returned success:", res.get("success"), "error:", res.get("error"))
print("  DB status now:", row[0] if row else None)

# Clean up
db.execute("DELETE FROM exam_sessions WHERE learner_id = 'test_learner_sec'")
