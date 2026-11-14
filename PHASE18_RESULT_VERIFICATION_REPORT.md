# PHASE 18: RESULT VERIFICATION & REPRODUCIBILITY REPORT
**Project:** IELTS by GAMA  
**Current Version:** 1.6.0  
**Focus:** Audit Record Immutability, Result Breakdown, Formula Transparency & Historical Reproducibility  
**Audit Date:** November 15, 2026  
**Auditor:** Assessment Accuracy Lead & Database Auditor  

---

## 1. Executive Summary

This report documents the verification and reproducibility infrastructure implemented in Phase 18. In an autonomous, self-study learning environment, students must be able to verify how practice results were calculated, inspect individual question evidence, and review historical performance without ambiguity or discrepancies.

---

## 2. Result Breakdown Structure

Every completed examination session generates an immutable JSON evaluation record stored in `exam_sessions.results_json`. The record contains:

```json
{
  "session_id": "exam_sess_f0a1b2c3",
  "learner_id": "student_maya",
  "exam_id": "mock_full_acad",
  "track": "Academic",
  "module": "full_mock",
  "submitted_at": "2026-11-15T01:45:00Z",
  "overall_band": 6.5,
  "confidence_range": [6.0, 7.0],
  "raw_mean": 6.38,
  "band_breakdown": {
    "reading": 6.5,
    "listening": 7.0,
    "writing": 6.0,
    "speaking": 6.0
  },
  "skills": {
    "reading": {
      "raw_score": 28,
      "total_questions": 40,
      "accuracy_percent": 70.0,
      "estimated_band": 6.5,
      "confidence_range": [6.0, 7.0],
      "scoring_rule": "Official IELTS Academic Band Table (raw score out of 40)",
      "scoring_rule_version": "1.6.0",
      "answer_key_version": "1.6.0",
      "examiner_verified": false,
      "disclaimer": "Diagnostic practice score calculated automatically.",
      "questions": [
        {
          "question_num": 1,
          "question_id": "read_1",
          "prompt": "Peatlands cover less than 5% of global land area.",
          "user_answer": "True",
          "accepted_answers": ["True", "true", "t"],
          "correct_answer": "True",
          "is_correct": true,
          "is_unanswered": false,
          "marks_awarded": 1,
          "marks_available": 1,
          "evidence": "Paragraph 1 states peatlands cover approximately 3% of global land.",
          "explanation": "3% is strictly less than 5%, confirming factual agreement.",
          "review_topic": "Reading: TFNG"
        }
      ]
    }
  }
}
```

---

## 3. Idempotency & Duplicate Submission Protection

To preserve assessment integrity and prevent tampering:
1. When an examination session is submitted, its status transitions from `'in_progress'` to `'submitted'`.
2. Any subsequent submission attempt for the same session ID is intercepted:
   - The engine returns the existing cached result without altering marks.
   - It returns `"already_submitted": True`.
3. Tested and verified in `test_06_duplicate_submission_protection`.

---

## 4. Historical Reproducibility Verification

1. **Deterministic Grading:** Given the same set of submitted answers, `ExamManager` always produces identical raw scores, percentage, criteria bands, and overall band.
2. **Versioned Rules & Answer Keys:** Both `scoring_rule_version` (`"1.6.0"`) and `answer_key_version` (`"1.6.0"`) are explicitly recorded in the result payload.
3. **Database Permanence:** Past results are persisted in both `exam_sessions` (complete breakdown) and `test_results` (profile analytics). Verified that querying historical sessions restores the exact original scores and explanations.

---

## 5. Official Exam Disclaimer

Every practice test result features the prominent disclaimer:
> *"Practice estimate only. This is not an official IELTS score from Cambridge Assessment, IDP: IELTS Australia, or the British Council. Formative diagnostic score for self-study preparation."*

---

## 6. Conclusion

Result calculation in IELTS by GAMA is 100% transparent, auditable, and reproducible, giving learners complete confidence in their practice scores and clear pathways for targeted improvement.
