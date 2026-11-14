# PHASE 16 BLIND DOUBLE-MARKING & RECONCILIATION REPORT
**Project:** IELTS by GAMA  
**Version:** 1.6.0  
**Phase:** 16 — Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit  
**Date:** November 15, 2026  
**Component:** `core/review/double_marking.py`, `ui/server.py`, `ui/static/`  

---

## 1. Objective & Assessment Philosophy

In standardized high-stakes language testing (such as Cambridge IELTS), inter-rater reliability is the cornerstone of assessment defensibility. A single human examiner's score is susceptible to subjectivity, halo effects, and cognitive fatigue. 

Phase 16 implements an independent blind double-marking framework. Submissions selected for human calibration are independently evaluated by two examiners. Marks remain strictly confidential until both have submitted. An algorithmic disagreement matrix evaluates inter-rater congruence, and any criterion divergence exceeding 0.5 band triggers Senior Examiner reconciliation.

---

## 2. Double-Marking Architectural Implementation

### 2.1 Paired Assignment Creation
The `DoubleMarkingManager` creates paired review assignments:
- A single candidate submission (`submission_id`) is mapped to a paired review record (`pair_id`).
- Two independent assignments (`assignment_1_id` and `assignment_2_id`) are generated in `review_assignments` and assigned to distinct qualified examiners (`reviewer_1_id` and `reviewer_2_id`).

### 2.2 Blind Review Protection Protocol
To prevent cognitive anchoring and peer bias, the system enforces strict blind evaluation:
- When Examiner 1 queries the paired assignment, Examiner 2's evaluation is omitted from the API response unless Examiner 1 has already submitted their own official evaluation.
- When Examiner 2 queries the paired assignment, Examiner 1's marks remain masked until Examiner 2 submits.
- Once both evaluations transition to `status="submitted"`, the blind review gate unlocks, and the Inter-Rater Disagreement Matrix is computed.

### 2.3 Inter-Rater Criterion Disagreement Matrix
The matrix evaluates criterion-by-criterion absolute divergence:
$$\Delta_{\text{crit}} = | \text{Score}_{\text{Reviewer 1, crit}} - \text{Score}_{\text{Reviewer 2, crit}} |$$
$$\Delta_{\text{overall}} = | \text{Overall Band}_{\text{Reviewer 1}} - \text{Overall Band}_{\text{Reviewer 2}} |$$

- **Congruence Threshold:** If all $\Delta_{\text{crit}} \le 0.5$, the evaluations are deemed aligned. The consensus band is calculated as the arithmetic mean of the two examiners.
- **Divergence Threshold Alert:** If any $\Delta_{\text{crit}} > 0.5$ (e.g., Examiner 1 awards 7.0 for Task Response while Examiner 2 awards 6.0, $\Delta = 1.0$), the system sets `disagreement_detected = 1` and flags the pair for mandatory Senior Examiner reconciliation.

### 2.4 Senior Examiner Reconciliation Workflow
When a disagreement is flagged:
1. The submission escalates to a Senior Examiner (`examiner_clara` or `admin`).
2. The Senior Examiner inspects:
   - Original stimulus and learner submission.
   - Examiner 1's complete scores, strengths, and criterion commentary.
   - Examiner 2's complete scores, strengths, and criterion commentary.
   - The computed Disagreement Matrix highlighting diverging criteria.
3. The Senior Examiner determines and enters:
   - Final Reconciled Overall Band (e.g., 6.5).
   - Detailed Reconciliation Rationale citing IELTS band descriptor evidence.
4. **Audit Ledger Preservation:** Neither Examiner 1's nor Examiner 2's original scores are overwritten. All three evaluation records (Examiner 1, Examiner 2, and Senior Examiner) are permanently retained in `human_evaluations`, and `review_assignments` is updated with `is_reconciled = 1` and `consensus_overall_band`.

---

## 3. REST API Specifications

| Method | Endpoint | Authorized Roles | Function |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/examiner/double_marking` | `Examiner`, `Admin` | Lists paired double-marking assignments with blind-masking applied |
| `POST` | `/api/examiner/review` | `Examiner`, `Admin` | Submits an independent examiner evaluation |
| `POST` | `/api/examiner/reconcile` | `Examiner`, `Admin` | Commits senior examiner reconciliation determination |

---

## 4. Empirical Test Verification

Automated testing in `tests/test_phase16_beta_toolkit.py`:
1. `test_double_marking_disagreement_and_reconciliation`:
   - Enrolled a paired writing submission between `examiner_mark` and `examiner_clara`.
   - Verified that while only 1 reviewer submitted, `get_double_marked_evaluations(reviewer_id='examiner_mark')` hid Clara's evaluation.
   - Recorded Examiner 1 Overall: 6.5 (TR: 7.0, CC: 6.5, LR: 6.5, GRA: 6.0).
   - Recorded Examiner 2 Overall: 6.0 (TR: 5.5, CC: 6.0, LR: 6.5, GRA: 6.0).
   - Verified that TR divergence was $|7.0 - 5.5| = 1.5 > 0.5$, successfully triggering `disagreement_detected = True`.
   - Executed Senior Examiner reconciliation awarding final consensus band 6.5 with documented rationale.
   - Verified that `is_reconciled == 1` and both original evaluations remained unmodified in the audit ledger.

---

## 5. Conclusion & Assessment Defensibility

The double-marking engine ensures that IELTS by GAMA conforms to high-stakes examination calibration principles. Human scoring subjectivity is mitigated by systematic blind review and transparent, auditable senior reconciliation.
