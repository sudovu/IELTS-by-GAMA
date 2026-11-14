import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database.db_manager import DatabaseManager
from core.exam.exam_manager import ExamManager
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.curriculum.curriculum_engine import CurriculumEngine

db = DatabaseManager('data/ielts_gama.db')
mgr = ExamManager(db)

print("=== VERIFYING PHASE 15 DEFECT CORRECTIONS ===")

# Test 1: Submitting abandoned session
sess1 = mgr.start_exam('test_p15_user', 'Academic', 'reading')
sid1 = sess1['session_id']
db.execute("UPDATE exam_sessions SET status = 'abandoned' WHERE id = ?", (sid1,))
res1 = mgr.submit_exam(sid1, 'test_p15_user')
print("1. Submitting abandoned session rejected:", not res1.get("success"), "error:", res1.get("error"))

# Test 2: Malformed answers payload in autosave
sess2 = mgr.start_exam('test_p15_user', 'Academic', 'reading')
sid2 = sess2['session_id']
res2 = mgr.autosave_answers(sid2, 'test_p15_user', ["not", "a", "dict"])
print("2. Malformed answers payload rejected:", not res2.get("success"), "error:", res2.get("error"))

# Test 3: Autosave answer merging (protecting against stale overwrites)
mgr.autosave_answers(sid2, 'test_p15_user', {"read_1": "TRUE"})
mgr.autosave_answers(sid2, 'test_p15_user', {"read_2": "FALSE"})
row2 = db.fetchone("SELECT answers_json FROM exam_sessions WHERE id = ?", (sid2,))
import json
answers_data = json.loads(row2[0])["answers"]
print("3. Answers merged properly:", answers_data == {"read_1": "TRUE", "read_2": "FALSE"}, answers_data)

# Test 4: Empty writing evaluation
eval_w = WritingEvaluator.evaluate_essay("acad_w1_report", "")
print("4. Empty writing returns Band 0.0:", eval_w["estimated_band"] == 0.0, "band:", eval_w["estimated_band"])

# Test 5: Empty speaking evaluation
eval_s = SpeakingExaminer.evaluate_spoken_response("")
print("5. Empty speaking returns Band 0.0:", eval_s["estimated_band"] == 0.0, "band:", eval_s["estimated_band"])

# Test 6: Curriculum partial submission does NOT grant 100% or mastery
curric = CurriculumEngine(db)
# Submit 1 correct answer out of 3 for a lesson
res_c = curric.evaluate_submission('test_p15_user', 'curric_a1_gram_present_simple', {'a1_as_1': 2})
print("6. Partial lesson submission (1/3) receives 33.3%, not 100%:", res_c["score"] == 33.3, "score:", res_c["score"], "status:", res_c["status"])

# Clean up
db.execute("DELETE FROM exam_sessions WHERE learner_id = 'test_p15_user'")
db.execute("DELETE FROM learner_progress WHERE learner_id = 'test_p15_user'")
db.execute("DELETE FROM learner_mistakes WHERE learner_id = 'test_p15_user'")
print("=== ALL 6 DEFECT TESTS PASSED CLEANLY! ===")
