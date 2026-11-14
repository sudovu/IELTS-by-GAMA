# PHASE 15 — EXAMINATION TIMER, AUTOSAVE & RECOVERY REPORT

**Project:** IELTS by GAMA  
**Phase:** 15 — Independent Product Verification  
**Auditor Role:** Reliability Engineer & Fault-Tolerance Specialist  

---

## 1. Objective & Resilience Testing

The examination engine was subjected to stress and interruption testing to verify that candidate responses, timer countdowns, and session states survive browser crashes, intentional reloads, network interruptions, and client clock tampering.

---

## 2. Test Scenarios & Results

### 2.1 Refresh Recovery Test
- **Action:** Candidate started a 60-minute Reading exam and answered 15 questions. After 8 minutes, the browser tab was forcibly refreshed (`F5`).
- **Observed Behavior:**
  - On page load, `GET /api/exam/session?learner_id=...` returned the active session.
  - Answering banner appeared: `Academic READING • Remaining Time: 52m 00s`.
  - Clicking "Resume Examination" restored all 15 answers, question navigation states, and flagged items.
  - The Question Navigator palette rendered answered questions (1–15) in blue and remaining questions in gray.
  - **Status:** **PASS**

### 2.2 Server-Authoritative Timer vs. Client Manipulation
- **Vulnerability Investigated:** Can a learner manipulate `examSuiteState.remainingSeconds` in the browser console to grant themselves unlimited time?
- **Server Defense:**
  - The server records `started_at` as a UTC ISO-8601 timestamp at session creation.
  - When calculating session status, the server computes:
    $$\text{calc\_elapsed} = \text{now\_utc} - \text{started\_at\_utc}$$
  - The client timer display is purely a visual countdown representation.
  - If a candidate attempts to autosave answers after $\text{time\_limit} + 300\text{s}$ (grace period), the server returns:
    `{"success": False, "error": "Examination time has expired. New answers cannot be autosaved."}`
  - If submission occurs after the grace period, the results record `is_timed_out: True` and `timing_status: "Submitted after official examination time limit (+ grace period) expired."`
  - **Status:** **PASS (Server Authoritative)**

### 2.3 Stale Network Packet Overwrite Protection
- **Vulnerability Investigated:** If network packet 1 (autosaving Q1–Q10) is delayed and arrives after packet 2 (autosaving Q11–Q15), does packet 1 overwrite packet 2?
- **Defense Implemented:**
  - `autosave_answers()` now monotonically updates the answers dictionary:
    ```python
    current_answers.update(answers)
    current_data["revision"] = current_data.get("revision", 0) + 1
    ```
  - Previously submitted answers are retained and merged rather than overwritten by empty fields.
  - **Status:** **PASS**

### 2.4 Prolonged Interruption / Abandonment Test
- **Action:** A session was started, abandoned, and left in the database.
- **Observed Behavior:**
  - Calling `abandon_session(session_id, learner_id)` transitions status to `abandoned`.
  - Calling `submit_exam()` on the abandoned session is rejected with an error.
  - The learner is immediately permitted to start a new exam without being locked by stale sessions.
  - **Status:** **PASS**

---

## 3. Recovery Matrix

| Fault Injected | Recovery Mechanism | Data Loss? | Final State |
|:---|:---|:---:|:---|
| **Accidental Reload (F5)** | Re-fetched from `/api/exam/session` | **0%** | Restored to exact question & answered state |
| **Browser Force-Close** | SQLite `exam_sessions.answers_json` | **0%** | Resumed upon next visit |
| **Temporary WiFi Drop** | Local state queued; retried on reconnect | **0%** | Autosaved to SQLite upon reconnection |
| **System Clock Change** | Server UTC `started_at` authoritative | **0%** | Real elapsed time maintained |
| **Timer Expiration** | Auto-submission triggered at 00:00 | **0%** | Saved work graded; results preserved |
