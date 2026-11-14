# Phase 17 Role-Based Access Control (RBAC) & Authorization Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Security Architecture Team  

---

## 1. Executive Summary

Role-Based Access Control (RBAC) and horizontal data isolation were subjected to comprehensive security auditing. Prior to Phase 17, role validation was partially client-enforced, and several REST endpoints permitted unauthenticated or horizontal data access. Phase 17 established strict server-side authorization gates across all administrative, pedagogical, and evaluation routes, prevented privilege escalation during registration, and enforced strict cross-learner data isolation.

---

## 2. Defined Roles & Privilege Matrix

| Capability / Resource | Learner | Teacher | Examiner | Senior Examiner | Administrator |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Self-Registration | Yes | No | No | No | No |
| Access Practice & Curriculum | Yes | Yes | Yes | Yes | Yes |
| Take Full Mock Examinations | Yes | Yes | Yes | Yes | Yes |
| View Own Exam Sessions & History | Yes | Yes | Yes | Yes | Yes |
| View Other Learners' History | **No (403)** | Assigned Only | Assigned Only | Assigned Only | Yes |
| Access Teacher Dashboard | **No (403)** | Yes | Yes | Yes | Yes |
| Grade Assigned Submissions | **No (403)** | Yes | Yes | Yes | Yes |
| Blind Double-Marking | **No (403)** | No | Yes | Yes | Yes |
| Reconcile Double-Marking Discrepancies | **No (403)** | No | No | **Yes** | **Yes** |
| Reconcile Self-Graded Submission | **No (COI)** | **No (COI)** | **No (COI)** | **No (COI)** | **No (COI)** |
| Create Beta Cohorts & Enrollments | **No (403)** | No | No | No | **Yes** |
| View Raw PII / Audit Logs | **No (403)** | No | No | No | **Yes** |
| Manage System Users & Roles | **No (403)** | No | No | No | **Yes** |

*(COI = Denied due to Conflict-of-Interest prevention)*

---

## 3. Privilege Escalation Prevention

### 3.1 Self-Registration Guard
In `core/auth/auth_manager.py: register_user()`, the `role` parameter is strictly checked:
- If a client attempts to pass `role="teacher"`, `role="examiner"`, or `role="admin"`, the request is rejected unless `authorizing_admin_user_id` is supplied.
- If an authorizing ID is passed, the database verifies that the authorizing user exists, is active, and possesses the `admin` role.
- If no admin is present in the database (initial system bootstrap), an admin can only be created via the local CLI (`scripts/provision_admin.py`).

### 3.2 Frontend UI Guard
In `ui/static/index.html` and `ui/static/app.js`:
- Visual role-switching demo buttons were completely removed.
- Registration UI forms permit only learner enrollment. Privileged user management is accessible solely via the authenticated Admin panel.

---

## 4. Cross-Learner Data Isolation (Horizontal Authorization)

Horizontal privilege escalation (where Learner A accesses records of Learner B by manipulating URL identifiers) has been eliminated across all examination and results endpoints in `ui/server.py`:

1. **Session Access (`/api/exam/session`):**
   - The server validates the session token.
   - If the authenticated role is `learner`, the server verifies that the requested session's `learner_id` matches the authenticated user's ID or username.
   - Any ID mismatch immediately aborts with **HTTP 403 Forbidden**.
2. **Results Access (`/api/exam/results`):**
   - Attempting to inspect completed exam results belonging to another learner is rejected with **HTTP 403 Forbidden**.
3. **History Listing (`/api/exam/history`):**
   - The query parameter `?learner_id=<target>` is checked against the authenticated user context. Learners querying any ID other than their own receive **HTTP 403 Forbidden**.

---

## 5. Review & Reconciler Boundary Controls

1. **Discrepancy Reconciliation (`/api/examiner/reconcile`):**
   - In `ui/server.py`, access to this route is explicitly restricted to `["admin", "senior_examiner"]`.
   - General examiners and teachers attempting to submit final reconciliations are rejected with **HTTP 403 Forbidden**.
2. **Conflict of Interest Protection:**
   - In `core/review/double_marking.py: submit_reconciliation()`, the database inspects both `human_evaluations` and `review_assignments` for the target submission.
   - If the reconciling Senior Examiner was either Reviewer 1 or Reviewer 2 on that submission, the operation is blocked with:
     `"Conflict of interest: An examiner who graded or was assigned to this submission cannot act as its Senior Reconciler."`
