# Phase 17 Review Workflow Security Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Security Architecture Team  

---

## 1. Executive Summary

The assessment review workflow introduced in Phase 16—comprising teacher grading, blind double-marking, and senior examiner reconciliation—was subjected to rigorous security and immutability auditing. Phase 17 implemented strict blind review isolation, prevented post-submission tampering of human marks, enforced conflict-of-interest checks for reconcilers, and preserved original learner work against modification.

---

## 2. Blind Double-Marking Protection

In standardized assessment systems, double-marking must be genuinely "blind" to eliminate anchoring bias, where a second examiner's judgment is influenced by the first examiner's scores or commentary:

### 2.1 Server-Side Blind Enforcement
In `core/review/double_marking.py: get_double_marked_evaluations()`:
```python
# If the requesting user is one of the assigned examiners and hasn't submitted yet:
if requesting_reviewer_id and user_role not in ("admin", "senior_examiner"):
    # Filter out all evaluations until the caller's own evaluation is officially submitted
```
- If Examiner 1 submits an evaluation (e.g., Band 6.0), Examiner 2 cannot retrieve or view Examiner 1's criteria scores, band, or comments.
- Queries by Examiner 2 return an empty evaluation list (`[]`) with `blind_active: True`.
- Only after Examiner 2 has submitted their own independent evaluation (or if the requester is an authorized Senior Examiner or Administrator) does the system expose both evaluations simultaneously.

---

## 3. Immutability of Submitted Human Evaluations

### 3.1 Vulnerability Description
In early prototypes, an examiner could potentially re-submit `save_evaluation` to alter previously committed scores after observing peer ratings or student feedback.

### 3.2 Immutability Guard
In `core/review/review_manager.py: save_evaluation()`:
```python
existing = self.db.fetchone(
    "SELECT id, revision, status FROM human_evaluations WHERE assignment_id = ? AND reviewer_id = ?",
    (assignment_id, reviewer_id)
)

if existing:
    eval_id, old_rev, old_status = existing[0], existing[1], existing[2]
    if old_status in ("submitted", "reconciled"):
        return {
            "success": False,
            "error": "Evaluation has already been officially submitted and is immutable."
        }
```
- Once an evaluation is committed with status `submitted` or `reconciled`, all further modification attempts are rejected.
- Evaluators can save drafts iteratively while status remains `in_progress`, but final submission permanently seals the record.

---

## 4. Reconciliation Conflict-of-Interest Guard

Standard assessment governance dictates that an examiner cannot adjudicate a disagreement between their own evaluation and a peer's evaluation:

### 4.1 Independent Adjudication Check
In `core/review/double_marking.py: submit_reconciliation()`:
```python
# Check prior reviewers across both human_evaluations and review_assignments
prior_reviewers = set()
for r in self.db.fetchall("SELECT reviewer_id FROM human_evaluations WHERE submission_id = ? AND reviewer_role != 'senior_examiner'", (submission_id,)):
    prior_reviewers.add(r[0])
for r in self.db.fetchall("SELECT assigned_to FROM review_assignments WHERE submission_id = ?", (submission_id,)):
    prior_reviewers.add(r[0])

if reconciler_id in prior_reviewers:
    return {
        "success": False,
        "error": "Conflict of interest: An examiner who graded or was assigned to this submission cannot act as its Senior Reconciler."
    }
```
If an examiner who participated in the double-marking pair attempts to reconcile their own pair, the operation is blocked. Only an independent Senior Examiner or Administrator may resolve the discrepancy.

---

## 5. Preservation of Original Learner Content

Original learner essays and speaking transcripts are stored in `review_assignments.content_json`:
- Neither `save_evaluation` nor `submit_reconciliation` modifies the original learner text.
- Human evaluations are recorded in separate relational records in `human_evaluations`, preserving the primary learner artifact unchanged for archival and auditing purposes.
