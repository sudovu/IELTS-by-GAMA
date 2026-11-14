# Phase 17 Baseline Audit Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Execution Date:** 2026-11-15  
**Audit Status:** Completed & Verified  

---

## 1. Executive Summary

Phase 17 commenced with a mandatory, non-destructive baseline audit of the IELTS by GAMA repository, database, runtime configurations, and external synchronization scripts. The primary objective was to independently assess the security posture following the implementation of Phase 16 (Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit), identify architectural vulnerabilities, prevent exposure of credentials or learner data, and establish verified backups before executing any modifications.

The baseline audit revealed significant pedagogical and functional assets introduced in Phase 16, but also critical security and privacy shortcomings—most notably hardcoded default user credentials seeded during database migration, weak salted SHA-256 password hashing, query-string session token transmission, and an unshielded static build script syncing assets to a local external project directory (`c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts`).

---

## 2. Environment & Version Control State

| Component | State / Value |
| :--- | :--- |
| **Operating System** | Windows 11 Enterprise (x86_64) |
| **Python Runtime** | Python 3.14.7 |
| **SQLite Version** | 3.50.4 |
| **Git Branch** | `master` |
| **Baseline Git Commit** | `890eeb1cea17a5216f0b39e840e0c758eff5275e` |
| **Baseline Commit Message** | `feat(phase16): Implement Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit (v1.6.0)` |
| **Repository Path** | `c:\Users\Sudo\Projects\IELTS by GAMA` |

---

## 3. Database State & Pre-Hardening Checkpoint

Before performing any code modifications or migrations, an atomic online backup of the primary SQLite database was executed using the standard SQLite Online Backup API.

### 3.1 Primary Database Baseline Metrics
- **Path:** `data/ielts_gama.db`
- **File Size:** 552,960 bytes
- **SQLite Page Size:** 4,096 bytes
- **Journal Mode:** `wal` (Write-Ahead Logging)
- **Total Tables:** 25
- **Integrity Check:** `PRAGMA integrity_check` returned `ok`.
- **Foreign Key Violations:** `PRAGMA foreign_key_check` returned 0 violations.

### 3.2 Pre-Migration Backup Verification
- **Backup Path:** `data/ielts_gama_phase17_backup.db`
- **Backup File Size:** 552,960 bytes
- **Backup Verification Command:** `scripts/audit_phase17_db.py`
- **Integrity Check:** `ok`
- **Foreign Key Violations:** 0
- **Restoration Test:** Verified by restoring into an isolated temporary database in `%TEMP%`, confirming schema recreation, querying all 25 tables, and verifying zero record corruption before cleanly deleting the temporary test database.

### 3.3 Database Table Inventory (25 Tables)
1. `learners`
2. `mistake_book`
3. `srs_items`
4. `knowledge_base`
5. `study_plans`
6. `test_results`
7. `smart_cache`
8. `system_settings`
9. `schema_migrations`
10. `curriculum_lessons`
11. `lesson_progress`
12. `vocabulary_vault`
13. `exam_sessions`
14. `writing_drafts`
15. `ai_conversations`
16. `users`
17. `user_sessions`
18. `teacher_assignments`
19. `review_assignments`
20. `human_evaluations`
21. `benchmark_records`
22. `beta_cohorts`
23. `beta_participants`
24. `beta_feedback`
25. `beta_bug_reports`

---

## 4. Phase 16 Vulnerability Assessment

The baseline inspection identified six major security defects that required remediation before any pilot participants could be admitted:

1. **Hardcoded Initial User Credentials in Migrations:**
   - `core/database/migrations.py` automatically seeded default accounts (`admin`, `teacher_sarah`, `examiner_mark`, `examiner_clara`, `learner_alice`, `senior_reconciler`) with predictable default passwords (`admin123`, `teacher123`, `examiner123`, etc.).
   - If executed on any shared or networked instance, these accounts presented an immediate authentication bypass.

2. **Weak Password Hashing:**
   - `core/auth/auth_manager.py` utilized single-iteration salted SHA-256 (`hashlib.sha256(password + salt)`).
   - This did not comply with modern security baselines (OWASP recommended scrypt, Argon2id, or PBKDF2-HMAC-SHA256) and was vulnerable to GPU dictionary and rainbow table cracking.

3. **Query-String Session Token Exposure:**
   - `ui/server.py` accepted authentication tokens via `?token=` query parameters in `_get_auth_token()`.
   - This exposed sensitive session tokens to server access logs, web proxy caches, browser histories, and HTTP `Referer` headers.

4. **Frontend Quick-Login Demonstration Bypass:**
   - `ui/static/index.html` contained visual "Quick Demo Login" buttons that hardcoded role logins (`quickLogin('admin', 'admin123')`), bypassing standard authentication procedures.

5. **Missing Security Headers & Permissive Policies:**
   - The embedded HTTP server did not emit `Content-Security-Policy` (CSP), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, or modern `Referrer-Policy` headers.

6. **Automated External Build Synchronization:**
   - `scripts/build_ios_distribution.py` automatically copied built static assets to an external folder (`c:\Users\Sudo\Projects\gautambhuwan.com.np\ielts`) without explicit flag gating or environmental boundaries.

---

## 5. Audit Conclusion

The application core logic and educational materials are structurally sound, but the authentication, deployment, and session boundaries in Phase 16 were designed for local prototyping rather than secure supervised beta testing. Phase 17 remediation was confirmed as necessary.
