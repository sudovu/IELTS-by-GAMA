# PHASE 15 — EXAMINATION SECURITY & TAMPER-RESISTANCE AUDIT

**Project:** IELTS by GAMA  
**Phase:** 15 — Independent Product Verification  
**Auditor Role:** Senior Application Security Engineer & Penetration Tester  
**Testing Methodology:** Black-box & Grey-box API Fuzzing, Boundary Inspection, Cross-Learner Tampering Tests  

---

## 1. Scope of Audit

All examination-related REST API endpoints in `ui/server.py` and `core/exam/exam_manager.py` were audited:

1. `GET  /api/exam/library`
2. `POST /api/exam/start`
3. `GET  /api/exam/session`
4. `POST /api/exam/autosave`
5. `POST /api/exam/submit`
6. `GET  /api/exam/results`
7. `GET  /api/exam/history`

---

## 2. Attack Vectors Tested & Findings

### 2.1 Pre-Submission Answer Key Extraction
- **Objective:** Attempt to extract correct answers, acceptable variants, textual evidence, or distractor notes prior to submitting the exam.
- **Test:** Queried `/api/exam/start`, `/api/exam/session`, and inspect client JSON payloads across all 6 examination packages.
- **Result:** **0 leaked keys found.** Every sensitive key (`correct`, `correct_index`, `acceptable`, `evidence`, `explanation`, `distractor_analysis`, `distractor_note`) is completely stripped by `ExamContentRepository.sanitize_for_client()`.

### 2.2 Cross-Learner Tampering & Access
- **Objective:** Attempt to access, overwrite, or submit another learner's examination session.
- **Test:** Created Session $S_A$ for Learner A (`learner_alice`). Attempted:
  - Autosaving to $S_A$ with `learner_id="learner_bob"`.
  - Submitting $S_A$ with `learner_id="learner_bob"`.
  - Fetching results of $S_A$ with `learner_id="learner_bob"`.
- **Result:** **All attempts rejected with 400/404.**
  - Autosave returned: `{"success": False, "error": "Unauthorized learner session access"}`.
  - Submit returned: `{"success": False, "error": "Unauthorized learner session access"}`.
  - Results returned `None` (404 Not Found).

### 2.3 Submitting an Abandoned Session (Defect Discovered & Fixed)
- **Vulnerability:** When a session was marked `abandoned`, calling `POST /api/exam/submit` previously graded the exam and changed status to `submitted`.
- **Fix:** In `ExamManager.submit_exam()`, added an explicit check:
  ```python
  if sess["status"] != "in_progress":
      if sess["status"] == "submitted":
          return {"success": True, "already_submitted": True, "results": results}
      return {"success": False, "error": f"Cannot submit an exam session with status '{sess['status']}'"}
  ```
- **Verification:** Verified by `test_04_abandoned_session_submission_rejection`. Abandoned submissions are now blocked.

### 2.4 Duplicate Submission Locking
- **Objective:** Submit an exam twice with different answers to see if final results can be altered.
- **Test:** Submitted with `read_1 = "TRUE"`. Received Band 6.5. Immediately sent second submission with `read_1 = "FALSE"`.
- **Result:** Second request returned `{"success": True, "already_submitted": True}`. Answers in database remained locked to initial submission.

### 2.5 Malformed JSON & Unexpected Data Types (Defect Discovered & Fixed)
- **Vulnerability:** Sending `answers: ["not", "a", "dict"]` was saved by `autosave_answers`, causing `submit_exam` to crash with `AttributeError`.
- **Fix:** Enforced `isinstance(answers, dict)` validation in both `autosave_answers` and `submit_exam`.
- **Verification:** Verified by `test_05_malformed_autosave_payload_and_merging`. Invalid payloads are rejected with clear 400 errors.

---

## 3. Security Audit Summary Table

| Endpoint | Tested Vector | Defense Mechanism | Status |
|:---|:---|:---|:---:|
| `/api/exam/library` | Data disclosure | Returns public metadata only (no questions/answers) | **SECURE** |
| `/api/exam/start` | Key leakage | Sanitized pre-submission payload via recursive scrubber | **SECURE** |
| `/api/exam/session` | Cross-learner snooping | Filtered strictly by `learner_id` parameter | **SECURE** |
| `/api/exam/autosave` | Cross-learner tampering | Rejects if `sess.learner_id != request.learner_id` | **SECURE** |
| `/api/exam/autosave` | Payload corruption | Enforces dictionary type check; merges answers monotonically | **SECURE** |
| `/api/exam/submit` | Post-expiry submission | Server validates UTC `started_at`; flags timed-out exams | **SECURE** |
| `/api/exam/submit` | Status manipulation | Rejects submissions of `abandoned` or invalid sessions | **SECURE** |
| `/api/exam/results` | Answer snooping | Hides results until session is officially submitted | **SECURE** |
| `/api/exam/history` | Profile isolation | Scoped strictly to requesting learner ID | **SECURE** |
