# PHASE 18: WRITING FEEDBACK AUDIT REPORT
**Project:** IELTS by GAMA  
**Current Version:** 1.6.0  
**Focus:** Writing Evaluation Engine, Rubrics, Weighting & Automated Feedback Reliability  
**Audit Date:** November 15, 2026  
**Auditor:** Lead Assessment Architect & IELTS Writing Specialist  

---

## 1. Executive Summary

This audit evaluated the automated Writing evaluation pipeline across `core/writing/writing_evaluator.py`, `core/scoring/criteria_evaluator.py`, and `ExamManager._evaluate_writing_package`.

In self-study mode without human examiners, automated writing evaluation must provide constructive, formative feedback while strictly avoiding score inflation on blank, minimal, or off-topic submissions.

### Critical Defect Identified & Resolved:
- **Empty Essay Fallback Bug:** In `ExamManager._evaluate_writing_package`, the overall band was extracted using `eval_t1.get("overall_band", 5.0)`. Because `WritingEvaluator.evaluate_essay` returns `"estimated_band"`, an empty string submission (`""`) fell back to `5.0`, awarding an empty essay Band 5.0!
- **Resolution:** Updated key extraction to `eval_t1.get("estimated_band", eval_t1.get("overall_band", 0.0))`, and added explicit length checks in `_evaluate_writing_package` and `CriteriaEvaluator`:
  ```python
  if len(t1_text.strip().split()) == 0:
      band_t1 = 0.0
  if len(t2_text.strip().split()) == 0:
      band_t2 = 0.0
  ```
  Empty writing submissions now receive strictly **Band 0.0**.

---

## 2. Official IELTS Writing Weighting

The application strictly implements the official Cambridge IELTS formula:
$$\text{Writing Band} = \text{round\_band}\left(\frac{1}{3} \times \text{Task 1 Band} + \frac{2}{3} \times \text{Task 2 Band}\right)$$

This formula is verified in automated test `test_08_transparent_result_breakdown` and `test_10_writing_empty_and_underlength_protection`.

---

## 3. The 4 Official IELTS Writing Criteria

The automated evaluator scores essays across the 4 public IELTS band descriptor dimensions:

1. **Task Achievement / Task Response (25%):**
   - Task 1: Overview presence, key feature coverage, data reporting, minimum 150 words.
   - Task 2: Addressing all prompt parts, clear thesis position throughout, supporting arguments, conclusion, minimum 250 words.
2. **Coherence and Cohesion (25%):**
   - Paragraphing structure (4–5 paragraphs for Task 2).
   - Discourse marker frequency and diversity (e.g., *furthermore*, *consequently*, *in contrast*).
   - Elimination of repetitive mechanical linkers.
3. **Lexical Resource (25%):**
   - Detection of Academic Word List (AWL) vocabulary.
   - Collocation recognition.
   - Detection of informal register or colloquialisms.
4. **Grammatical Range and Accuracy (25%):**
   - Complex clause structures (relative clauses, conditionals, passive voice).
   - Formative error detection (subject-verb agreement, run-on sentences, article omission).

---

## 4. Underlength Penalties & Ceiling Enforcement

To prevent misleading score feedback:
- **0 words:** Band 0.0.
- **1–24 words:** Maximum Band 1.5. Minimal assessable text.
- **25–49 words:** Maximum Band 2.5. Insufficient sample to evaluate task response or cohesion.
- **Underlength deficit penalty:** For responses between 50 words and the required minimum (150 words for Task 1, 250 words for Task 2), a proportional penalty of up to 1.0 band is applied.

---

## 5. Formative Feedback & Disclaimers

The writing evaluation delivers:
1. **Formative Corrections:** Specific structural and grammatical suggestions.
2. **Advantage Checklist:** 8 objective criteria checkboxes (e.g. "Clear thesis position stated", "Distinct paragraphs", "Academic topic vocabulary").
3. **Diagnostic Uncertainty Disclosure:**
   > *"Automated diagnostic estimate for formative practice only; carries an estimated margin of error of ±0.5 to ±1.0 band. Human scoring agreement has not been established with formal examiner cohorts."*
4. **Examiner Status:** `examiner_verified: False`.

---

## 6. Conclusion

The Writing evaluation system is hardened against empty and minimal submissions, applies authentic Cambridge IELTS weighting, and provides actionable, honest formative feedback to independent learners.
