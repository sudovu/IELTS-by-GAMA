# PHASE 15 — FULL LEARNER JOURNEY END-TO-END VALIDATION REPORT

**Project:** IELTS by GAMA  
**Phase:** 15 — Independent Product Verification  
**Auditor Role:** User Experience Tester, End-to-End Test Architect  

---

## 1. Test Setup & Learner Profiles

Two completely independent learner profiles were created in an isolated database environment:

- **Learner A:** `learner_a` — Name: *Learner Academic*, Track: *Academic*, Target Band: *7.5*.
- **Learner B:** `learner_b` — Name: *Learner General*, Track: *General Training*, Target Band: *6.5*.

---

## 2. Learner A Journey — IELTS Academic Full Mock

1. **Test Start:** Learner A initiated `mock_full_acad`. Session `exam_session_acad_a` generated with a 164-minute countdown timer.
2. **Listening (40 Qs):** Dialogue played using Web Speech synthesis; answers input for Q1–Q10 (`Sterling`, `en-suite`, `210`, `September`, `Science`, etc.); remaining items intentionally left blank to test partial scoring.
3. **Reading (40 Qs across 3 Passages):** Candidate answered Passage 1 questions (TFNG, Summary completion); answers autosaved every 15 seconds.
4. **Writing (Tasks 1 & 2):**
   - Task 1: 175-word data report analyzing industrial greenhouse gas emissions.
   - Task 2: 285-word discursive essay on technological automation in the workforce.
5. **Speaking (Parts 1, 2, 3):**
   - Part 1: Spoken introduction regarding hometown and educational background.
   - Part 2: Long turn using 60-second prep countdown on learning software engineering.
   - Part 3: Analytical discussion on digital ethics and automation equity.
6. **Submission & Results:**
   - Overall Band Awarded: **Band 6.5** (Estimate Range: 6.0–7.0).
   - Reading Band: **5.5** | Listening Band: **4.5** | Writing Band: **7.0** | Speaking Band: **6.5**.
   - Timing Status: *Submitted on time.*
7. **Mistake Book & Adaptive Study Plan:**
   - Incorrect and unanswered items were recorded in SQLite `learner_mistakes` with detailed distractor notes and correct keys.
   - Recommendations produced: Practice Listening Section 3 & 4 note-taking; review Academic Reading inference strategies in the Academy.

---

## 3. Learner B Journey — IELTS General Training Full Mock

1. **Test Start:** Learner B initiated `mock_full_gt`. Session `exam_session_gt_b` created.
2. **Listening (40 Qs):** Attempted Sections 1 and 2.
3. **Reading (40 Qs across 3 Sections):** Candidate completed Section 1 noticeboard matching and Section 2 workplace guidelines. Evaluated against General Training band conversion thresholds (30/40 = Band 7.0 vs. Band 6.0 in Academic).
4. **Writing (Tasks 1 & 2):**
   - Task 1: Semi-formal complaint letter to apartment building management.
   - Task 2: Opinion essay advocating for public transport subsidies.
5. **Speaking (Parts 1, 2, 3):** Brief conversational responses submitted.
6. **Submission & Results:**
   - Overall Band: **Band 6.0** (Estimate Range: 5.5–6.5).
   - GT Reading Band: **6.0** | Listening Band: **4.0** | Writing Band: **6.5** | Speaking Band: **5.5**.

---

## 4. Multi-Learner Isolation Verification

| Verification Check | Expectation | Result | Status |
|:---|:---|:---:|:---:|
| **Cross-Profile Session Visibility** | Learner B cannot view Learner A's active exam | Returns `active_session: null` | **PASS** |
| **History Isolation** | Learner A's test results do not appear in Learner B's history | Filtered strictly by `learner_id` | **PASS** |
| **Mistake Book Segregation** | Learner B does not see Learner A's mistakes | Queries scoped to `WHERE learner_id = ?` | **PASS** |
| **Analytics Independence** | Individual skill radar charts reflect personal attempts | Profile metrics completely isolated | **PASS** |
| **Tamper Resistance** | Learner B cannot modify Learner A's answers | Rejected with 400 Unauthorized | **PASS** |
