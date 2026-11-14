# PHASE 16 TEACHER TOOLKIT & SCORING STUDIO REPORT
**Project:** IELTS by GAMA  
**Version:** 1.6.0  
**Phase:** 16 — Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit  
**Date:** November 15, 2026  
**Component:** `core/review/review_manager.py`, `ui/server.py`, `ui/static/`  

---

## 1. Objective & Scope

The Teacher Review Toolkit equips qualified English language instructors and IELTS examiners with a dedicated assessment environment. In previous versions, scoring was purely automated. Phase 16 establishes a human review workflow enabling educators to inspect candidate submissions, apply standardized Cambridge IELTS criteria rubrics, draft iterative feedback, track revision histories, and submit binding human evaluations.

---

## 2. Architectural Design & Implementation

### 2.1 Core Review Manager (`core/review/review_manager.py`)
The `ReviewManager` coordinates all review workflows:
1. **Assignment Lifecycle:**
   - Status transitions: `assigned` → `in_review` → `submitted`.
   - Immutable audit record: The learner's original prompt and submission text cannot be modified by the reviewer.
2. **Evaluation Storage & Revision Tracking:**
   - Evaluators can save working drafts without locking the assignment.
   - Each draft or final submission increments `revision_number` ($v1, v2, v3, \dots$).
   - A historical trail is preserved in `human_evaluations` linking back to the `assignment_id` and `reviewer_id`.
3. **Four-Criteria Scoring Architecture:**
   - **Writing Studio:**
     - Task Response / Task Achievement (TR/TA)
     - Coherence and Cohesion (CC)
     - Lexical Resource (LR)
     - Grammatical Range and Accuracy (GRA)
   - **Speaking Examiner:**
     - Fluency and Coherence (FC)
     - Lexical Resource (LR)
     - Grammatical Range and Accuracy (GRA)
     - Pronunciation (P)
   - Scores are validated on a 0.0 to 9.0 scale in strict 0.5 band increments (e.g., 6.0, 6.5, 7.0).
   - Overall band is calculated according to official Cambridge rounding rules: arithmetic mean of the four criteria rounded to the nearest half band (with fractional values $\ge 0.25$ rounded up to $0.5$, and $\ge 0.75$ rounded up to the next integer).

### 2.2 Speaking Modality Distinction
In response to assessment governance requirements, human speaking evaluations now explicitly record `assessment_mode`:
- `both`: Full speaking evaluation assessing acoustic audio and verbatim transcript.
- `audio`: Acoustic and phonological evaluation directly from audio stream.
- `transcript`: Textual assessment only.
- **Pedagogical Rule:** If `assessment_mode == "transcript"`, the system prevents claiming acoustic pronunciation scores without verified phonological audio.

### 2.3 Qualitative Feedback Fields
Every human evaluation mandates structured qualitative analysis:
- **Observed Strengths:** Concrete positive evidence tied to criterion descriptors.
- **Priority Growth Areas:** Diagnostic guidance targeting candidate band ceilings.
- **Detailed Commentary:** In-depth instructional narrative for the learner.
- **Private Notes:** Examiner-only commentary excluded from learner-facing reports.

---

## 3. API Endpoints

The Teacher Toolkit exposes secure REST endpoints enforcing RBAC session token validation:

| Method | Endpoint | Authorized Roles | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/teacher/dashboard` | `Teacher`, `Examiner`, `Admin` | Fetches queue of review assignments filtered by reviewer |
| `GET` | `/api/teacher/assignment` | `Teacher`, `Examiner`, `Admin` | Fetches assignment details, learner text, and active evaluation |
| `POST` | `/api/teacher/assignment/create` | `Teacher`, `Examiner`, `Admin` | Enqueues a new learner submission for teacher grading |
| `POST` | `/api/teacher/review/save` | `Teacher`, `Examiner`, `Admin` | Saves a working draft (`status="draft"`), increments revision |
| `POST` | `/api/teacher/review/submit` | `Teacher`, `Examiner`, `Admin` | Commits final official evaluation (`status="submitted"`) |

---

## 4. Frontend Review Studio UI

Integrated into `ui/static/index.html` and `ui/static/app.js`:
1. **Queue Panel:** Left sidebar listing active review assignments with status badges, skill icons, candidate IDs, and submission dates.
2. **Review Workspace:**
   - Stimulus prompt and candidate response viewer with word-count analysis.
   - Interactive criteria scoring sliders (1.0 to 9.0 in 0.5 steps) with live overall band calculation.
   - Qualitative feedback text areas with syntax-highlighted review guidance.
   - Dual action controls: "Save Working Draft" vs. "Submit Official Evaluation".
3. **Session Awareness:** Displays active reviewer credentials and role pill (`teacher_sarah (TEACHER)`).

---

## 5. Automated Verification Results

The test suite in `tests/test_phase16_beta_toolkit.py` validated the following:
- `test_teacher_review_draft_and_revisions`: Verified that saving drafts preserves intermediate scores, increments `revision_number` from 1 to 2, and retains draft status until explicit submission.
- `test_speaking_review_modality`: Verified that speaking assessments accurately track `assessment_mode: "both"` and record pronunciation criteria.
- `scripts/test_phase16_api.py`: Verified HTTP 200 responses, schema validation, and database persistence.

---

## 6. Status & Readiness

The Teacher Toolkit is fully operational, integrated into the multi-platform UI, backed by SQLite audit tables, and verified against regression test suites.
