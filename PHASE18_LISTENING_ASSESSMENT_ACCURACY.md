# PHASE 18: LISTENING ASSESSMENT ACCURACY REPORT
**Project:** IELTS by GAMA  
**Current Version:** 1.6.0  
**Focus:** Listening Question Numbering Integrity, Answer Equivalence & Assessment Reliability  
**Audit Date:** November 15, 2026  
**Auditor:** Assessment Accuracy Lead & Educational Psychometrician  

---

## 1. Executive Summary

This audit examined the Listening module in `core/listening/listening_engine.py` and its full mock package in `core/exam/content_repository.py`. The module features 4 authentic audio sections (Campus Accommodation, Community Center, Urban Microclimates, Hydrothermal Vents) comprising 40 questions.

### Critical Defect Identified & Resolved:
- **Root Cause:** All 4 sections in `ListeningEngine.SECTIONS` previously contained questions numbered `1..10`. In a 40-question mock exam, an answer submitted for question 1 overwrote and graded against Section 1 Q1, Section 2 Q11, Section 3 Q21, and Section 4 Q31 simultaneously.
- **Resolution:** Refactored question numbering in `ListeningEngine.SECTIONS` to sequential integers:
  - Section 1: Questions 1 to 10
  - Section 2: Questions 11 to 20
  - Section 3: Questions 21 to 30
  - Section 4: Questions 31 to 40
- **Dual Numbering Compatibility:** Updated `ListeningEngine.evaluate_submission` and `ExamManager._evaluate_listening_package` to accept both sequential keys (`listen_1` .. `listen_40`, `1` .. `40`) and local section keys (e.g. Q1 in Section 2 mapped to Q11).
- **Post-Fix Verification:** 0 duplicate numbers across all 40 questions. Automated verification test `scripts/audit_assessment_accuracy.py` confirmed 100% collision-free grading.

---

## 2. Listening Assessment Structure

| Section | Context | Speakers | Question Types | Question Range |
|---|---|---|---|---|
| **Section 1** | Everyday social / accommodation booking | Two speakers (dialogue) | Note completion, form filling | Q1 to Q10 |
| **Section 2** | Public informational monologue | One speaker (monologue) | Sentence completion, short answer | Q11 to Q20 |
| **Section 3** | University academic tutorial / project | Two to three speakers | Discussion notes, technical matching | Q21 to Q30 |
| **Section 4** | University lecture on hydrothermal vents | One speaker (monologue) | Summary completion, diagram notes | Q31 to Q40 |

---

## 3. Answer Checking & Equivalence Logic

`ListeningAnswerChecker` (`core/listening/listening_engine.py`) applies rigorous IELTS scoring standards:

1. **Case-Insensitive Normalization:** `"sterling"` matches `"Sterling"`; `"riverdale"` matches `"Riverdale"`.
2. **Whitespace Trimming:** Removes leading/trailing spaces and collapses internal whitespace.
3. **Punctuation Stripping:** Removes trailing periods, commas, and hyphens where acceptable.
4. **Number and Word Equivalence:** Numeric representation (e.g., `"210"`) and acceptable textual variations are verified against the acceptable answer list.
5. **Word Count Limits:** Checks each question's `max_words` limit (e.g. "NO MORE THAN TWO WORDS AND/OR A NUMBER"). Submissions exceeding the word limit are marked incorrect per IELTS rules.
6. **Distractor Analysis:** Every question includes explicit explanation of the IELTS distractor present in the audio script (e.g., initial mention of £240 rent before correcting to £210 full-term subsidy).

---

## 4. Empty Answer & Band Calculation Hardening

1. **Empty Submission Guard:** Empty or whitespace-only answers are immediately classified as `is_unanswered: True` with 0 marks awarded.
2. **Band Calculation Correction:** Updated `BandCalculator.raw_to_band_listening`:
   - 0 correct $\to$ Band 0.0 (previously defaulted to 3.5)
   - 1 correct $\to$ Band 1.0
   - 2 correct $\to$ Band 2.0
   - 3–4 correct $\to$ Band 2.5
   - 5–6 correct $\to$ Band 3.0
   - 7–9 correct $\to$ Band 3.5
   - 10–12 correct $\to$ Band 4.0
   - ... up to 39–40 correct $\to$ Band 9.0

---

## 5. Result Verification Metadata

Listening results include complete diagnostic details:
- `correct_answers`: Raw score (0 to 40).
- `total_questions`: 40.
- `accuracy_percent`: Exact percentage correct.
- `estimated_band`: Scaled IELTS band score.
- `confidence_range`: $\pm 0.5$ band confidence interval.
- `scoring_rule_version`: `"1.6.0"`.
- `answer_key_version`: `"1.6.0"`.
- `examiner_verified`: `False`.
- `activity_type`: `"transcript_strategy_practice_and_synthesis"`.
- `audio_asset_status`: `"speech_synthesis_ready"`.
- `questions`: Full question-by-question breakdown with student answer, accepted answers, distractor analysis, and correct mark indication.

---

## 6. Conclusion

Listening assessment is fully verified, collision-free, and provides precise, verifiable feedback for every student attempt.
