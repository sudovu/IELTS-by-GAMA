# PHASE 16 SECURITY & PRIVACY AUDIT REPORT
**Project:** IELTS by GAMA  
**Version:** 1.6.0  
**Phase:** 16 — Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit  
**Date:** November 15, 2026  
**Auditor:** Application Security Engineer & Data Protection Auditor  

---

## 1. Executive Summary

A comprehensive security and privacy audit of the Phase 16 implementation was executed, focusing on role-based access control (RBAC), password cryptography, session management, input sanitization, PII redaction, and offline data privacy.

The assessment confirmed that Phase 16 introduces enterprise-grade security controls without disrupting existing offline-first capabilities or learner database integrity.

---

## 2. Authentication & Cryptographic Controls

### 2.1 Password Storage & Verification
- Passwords are stored in the `users` table using salted cryptographic hashes.
- Formulation:
  $$\text{Salt} = \text{os.urandom}(16).\text{hex}()$$
  $$\text{Hash} = \text{hashlib.sha256}((\text{Salt} + \text{Password}).\text{encode}('utf-8')).\text{hexdigest}()$$
- Plaintext passwords are never logged, stored, or returned in API responses.
- Verification uses constant-time string comparison (`hmac.compare_digest`) to prevent timing side-channel attacks.

### 2.2 Session Token Management
- Session tokens are generated using cryptographically secure pseudorandom numbers (`secrets.token_hex(32)`).
- Sessions are stored in `user_sessions` with mandatory `expires_at` timestamps (default TTL: 24 hours).
- The system supports session validation (`validate_session`) and immediate revocation (`revoke_session`).
- Tokens are accepted via:
  - `X-Session-Token` custom header.
  - `Authorization: Bearer <token>` standard header.
  - Query parameter fallback for constrained mobile environments.

---

## 3. Server-Side Role-Based Access Control (RBAC)

Client-side role checks are inherently vulnerable to tampering. In IELTS by GAMA, all permission checks are enforced strictly on the server:
- **Defined Roles:**
  - `Learner`: Access to own profile, curriculum, practice exams, feedback, and mistakes.
  - `Teacher`: Access to Teacher Dashboard, review queues, draft saving, and evaluation submission.
  - `Examiner`: Access to paired double-marking assignments, blind reviews, inter-rater matrices, and Senior Examiner reconciliation.
  - `Admin`: Unrestricted access across all system administrative and configuration domains.
- **Enforcement Function (`AuthManager.authorize_request`):**
  - Validates session token existence and expiration.
  - Verifies user active status.
  - Confirms role membership against the allowed roles list.
  - Returns explicit HTTP 401 (Unauthorized) or HTTP 403 (Forbidden) if criteria fail.
- **Verification Evidence:** `scripts/test_phase16_api.py` and `tests/test_phase16_beta_toolkit.py` confirmed that requests from `learner_alice` to `/api/teacher/dashboard` or `/api/examiner/double_marking` are rejected with HTTP 403.

---

## 4. Candidate Privacy & PII Redaction

### 4.1 Informed Consent Requirement
Submissions cannot be transferred into benchmark datasets or presented for double-marking without explicit candidate consent. Attempting to enroll a submission without consent raises an immediate `ValueError` and writes no database record.

### 4.2 Automated PII Redaction
Candidate submissions undergo automated regex scrubbing before benchmark enrollment:
- Emails: Pattern `r'[\w\.-]+@[\w\.-]+\.\w+'` $\longrightarrow$ `[EMAIL_REDACTED]`
- Phone Numbers: Pattern `r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'` $\longrightarrow$ `[PHONE_REDACTED]`
- Common Honorifics: Salutations like `Mr.`, `Mrs.`, `Dr.`, `Prof.` followed by capitalized words $\longrightarrow$ `[NAME_REDACTED]`
- Learner Primary Keys: Decoupled; replaced with anonymized UUIDs.

### 4.3 Candidate Right to Erasure
Upon consent withdrawal (`withdraw_consent`), all candidate text is immediately replaced with `[CONSENT_WITHDRAWN_BY_CANDIDATE]`, score linkages are nulled, and the record is permanently excluded from calibration runs.

---

## 5. Web Application Vulnerability Review

### 5.1 SQL Injection Protection
All database queries across `core/database/`, `core/auth/`, `core/review/`, `core/benchmark/`, and `core/beta/` utilize parameterized SQLite queries (`cursor.execute(sql, params)`). No user-supplied string concatenation is used in SQL execution.

### 5.2 Path Traversal Protection
The static file server in `ui/server.py` normalizes and verifies all file paths:
- Incoming URIs are unquoted and stripped of directory traversal sequences (`..`, `/`, `\`).
- Resolved physical paths are checked with `os.path.commonpath([resolved_path, STATIC_DIR]) == STATIC_DIR`.
- Attempts to access external system files (e.g., `win.ini` or `/etc/passwd`) return HTTP 404.

### 5.3 Offline Mode Privacy Assurance
When `Forced Offline Mode` is active in the UI:
- All outbound network calls to external LLM providers or remote endpoints are short-circuited.
- All evaluation, scoring, and practice activities execute entirely against the local SQLite database and client-side JavaScript engine.
- Zero candidate telemetry or audio is transmitted outside the local machine.

---

## 6. Security Audit Conclusion

IELTS by GAMA version 1.6.0 demonstrates a mature, robust security posture. Access control is strictly enforced on the backend, passwords and sessions are protected by standard cryptographic primitives, and candidate privacy rights are rigorously observed.
