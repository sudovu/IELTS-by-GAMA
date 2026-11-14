import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.exam.content_repository import ExamContentRepository

forbidden_keys = {"correct", "correct_index", "acceptable", "evidence", "explanation", "distractor_analysis", "distractor_note", "audio_script"}

def scan_for_leakage(obj, path=""):
    leaks = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            curr_path = f"{path}.{k}" if path else k
            if k in forbidden_keys:
                leaks.append((curr_path, v))
            else:
                leaks.extend(scan_for_leakage(v, curr_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            leaks.extend(scan_for_leakage(item, f"{path}[{i}]"))
    return leaks

print("Scanning all examination packages with conceal_answers=True:")
for exam_info in ExamContentRepository.list_available_exams():
    exam_id = exam_info["id"]
    pkg = ExamContentRepository.get_exam_package(exam_id, conceal_answers=True)
    leaks = scan_for_leakage(pkg)
    print(f"  {exam_id}: {len(leaks)} leaked keys found")
    if leaks:
        for p, val in leaks[:5]:
            print(f"    LEAK: {p} = {val}")
