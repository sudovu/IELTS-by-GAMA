"""
Comprehensive Assessment Accuracy and Answer Key Audit for Phase 18.
Audits every Reading and Listening question across Academic and General Training.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.exam.content_repository import ExamContentRepository
from core.reading.reading_engine import ReadingEngine
from core.reading.question_types import ReadingQuestionTypes
from core.listening.listening_engine import ListeningEngine
from core.listening.answer_checker import ListeningAnswerChecker
from core.scoring.band_calculator import BandCalculator

def audit_all_assessments():
    issues = []
    total_q_checked = 0

    print("=== 1. AUDITING FULL ACADEMIC MOCK (mock_full_acad) ===")
    acad = ExamContentRepository.get_exam_package("mock_full_acad", conceal_answers=False)
    
    # 1.1 Reading Academic
    r_items = acad["skills"]["reading"]["passages"]
    r_nums = set()
    for p in r_items:
        for q in p["questions"]:
            total_q_checked += 1
            num = q["num"]
            if num in r_nums:
                issues.append(f"Duplicate Academic Reading question number: {num}")
            r_nums.add(num)

            # Check answer key
            if not q.get("correct") and not q.get("acceptable"):
                issues.append(f"Missing answer key in Academic Reading Q{num}")

            # Check MCQ
            if q.get("type") in ("MCQ", "Multiple Choice"):
                opts = q.get("options", [])
                corr = q.get("correct", "")
                if not opts:
                    issues.append(f"MCQ Academic Reading Q{num} has no options")
                if corr not in opts and q.get("correct_index") is None:
                    issues.append(f"MCQ Academic Reading Q{num} correct '{corr}' not in options")

            # Check empty answer handling
            empty_eval = ReadingQuestionTypes.grade_question(q, "")
            if empty_eval["is_correct"]:
                issues.append(f"CRITICAL: Academic Reading Q{num} awarded credit for empty answer!")

            # Check correct answer awards credit
            target_ans = q.get("correct") or q.get("acceptable", [""])[0]
            if isinstance(target_ans, list):
                target_ans = target_ans[0]
            corr_eval = ReadingQuestionTypes.grade_question(q, target_ans)
            if not corr_eval["is_correct"]:
                issues.append(f"CRITICAL: Academic Reading Q{num} failed on official key '{target_ans}'")

    print(f"Academic Reading questions checked: {len(r_nums)} (Expected: 40)")
    if len(r_nums) != 40:
        issues.append(f"Academic Reading has {len(r_nums)} questions instead of 40")

    # 1.2 Listening Academic
    l_secs = acad["skills"]["listening"]["sections"]
    l_nums = set()
    for s in l_secs:
        for q in s["questions"]:
            total_q_checked += 1
            num = q["num"]
            if num in l_nums:
                issues.append(f"Duplicate Listening question number: {num}")
            l_nums.add(num)

            acceptable = q.get("acceptable") or [q.get("correct", "")]
            if not acceptable or not acceptable[0]:
                issues.append(f"Missing answer key in Listening Q{num}")

            # Empty answer check
            is_c, msg = ListeningAnswerChecker.check_answer("", acceptable, max_words=q.get("max_words", 2))
            if is_c:
                issues.append(f"CRITICAL: Listening Q{num} awarded credit for empty answer!")

            # Official answer check
            is_c2, msg2 = ListeningAnswerChecker.check_answer(acceptable[0], acceptable, max_words=q.get("max_words", 2))
            if not is_c2:
                issues.append(f"CRITICAL: Listening Q{num} failed on official key '{acceptable[0]}'")

    print(f"Listening questions checked: {len(l_nums)} (Expected: 40)")
    if len(l_nums) != 40:
        issues.append(f"Listening has {len(l_nums)} questions instead of 40")

    print("\n=== 2. AUDITING FULL GENERAL TRAINING MOCK (mock_full_gt) ===")
    gt = ExamContentRepository.get_exam_package("mock_full_gt", conceal_answers=False)
    
    # 2.1 Reading GT
    gt_r_items = gt["skills"]["reading"].get("passages") or gt["skills"]["reading"].get("sections") or []
    gt_r_nums = set()
    for sec in gt_r_items:
        for q in sec["questions"]:
            total_q_checked += 1
            num = q["num"]
            if num in gt_r_nums:
                issues.append(f"Duplicate GT Reading question number: {num}")
            gt_r_nums.add(num)

            if not q.get("correct") and not q.get("acceptable"):
                issues.append(f"Missing answer key in GT Reading Q{num}")

            # Check MCQ
            if q.get("type") in ("MCQ", "Multiple Choice"):
                opts = q.get("options", [])
                corr = q.get("correct", "")
                if not opts:
                    issues.append(f"MCQ GT Reading Q{num} has no options")
                if corr not in opts and q.get("correct_index") is None:
                    issues.append(f"MCQ GT Reading Q{num} correct '{corr}' not in options")

            # Check empty answer handling
            empty_eval = ReadingQuestionTypes.grade_question(q, "")
            if empty_eval["is_correct"]:
                issues.append(f"CRITICAL: GT Reading Q{num} awarded credit for empty answer!")

            # Check correct answer awards credit
            target_ans = q.get("correct") or q.get("acceptable", [""])[0]
            if isinstance(target_ans, list):
                target_ans = target_ans[0]
            corr_eval = ReadingQuestionTypes.grade_question(q, target_ans)
            if not corr_eval["is_correct"]:
                issues.append(f"CRITICAL: GT Reading Q{num} failed on official key '{target_ans}'")

    print(f"GT Reading questions checked: {len(gt_r_nums)} (Expected: 40)")
    if len(gt_r_nums) != 40:
        issues.append(f"GT Reading has {len(gt_r_nums)} questions instead of 40")

    print(f"\nTotal questions audited: {total_q_checked}")
    print(f"Total defects / discrepancies found: {len(issues)}")
    for iss in issues:
        print("  ❌", iss)

    return len(issues) == 0

if __name__ == "__main__":
    audit_all_assessments()
