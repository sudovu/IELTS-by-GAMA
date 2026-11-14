# Phase 17 Controlled Beta Launch Gate Checklist

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Gate Decision Date:** 2026-11-15  
**Review Status:** Controlled Beta Preparation Authorized  

---

## 1. Overview

Before real human learners, teachers, or examiners are admitted into the supervised beta pilot, all technical, operational, pedagogical, and privacy prerequisites must be verified. This checklist distinguishes between **technical engineering controls** (which are fully implemented and verified in code) and **operational prerequisites** (which require real human staffing and participant onboarding).

---

## 2. Technical & Security Gate Criteria

| Item # | Technical Requirement | Verification Method | Status |
| :---: | :--- | :--- | :---: |
| **SEC-01** | Password hashing modernized to standard `scrypt` ($N=16384, r=8, p=1$) | Unit test `test_01`, DB schema audit | **SATISFIED** |
| **SEC-02** | Hardcoded default accounts removed from migrations and seed files | Inspected `migrations.py`, zero defaults | **SATISFIED** |
| **SEC-03** | Administrator provisioning restricted to authenticated CLI tool | Verified `scripts/provision_admin.py` | **SATISFIED** |
| **SEC-04** | Sliding-window authentication rate limiting (5 attempts / 15 mins) | Unit test `test_05`, HTTP 429 response | **SATISFIED** |
| **SEC-05** | Anti-enumeration constant-time dummy verification on non-existent users | Unit test `test_04` | **SATISFIED** |
| **SEC-06** | Query-string session token transport completely eliminated | Unit test `test_09`, HTTP 401 response | **SATISFIED** |
| **SEC-07** | Mandatory HTTP security headers (nosniff, DENY, CSP, Referrer-Policy) | Unit test `test_08`, server inspection | **SATISFIED** |
| **SEC-08** | Cross-learner data isolation enforced on exam sessions/results | Unit test `test_10`, HTTP 403 response | **SATISFIED** |
| **SEC-09** | Blind double-marking review isolation verified on server | Unit test `test_11`, evaluation filtering | **SATISFIED** |
| **SEC-10** | Immutability of submitted human evaluations enforced | Unit test `test_12`, DB update rejection | **SATISFIED** |
| **SEC-11** | Conflict of interest check prevents reviewer from reconciling own work | Unit test `test_13`, double-marking check | **SATISFIED** |
| **SEC-12** | External deployment path gated behind `--deploy-external` flag | Inspected `build_ios_distribution.py` | **SATISFIED** |

---

## 3. Privacy, Consent & Data Governance Criteria

| Item # | Privacy & Governance Requirement | Verification Method | Status |
| :---: | :--- | :--- | :---: |
| **PRV-01** | Explicit candidate informed consent required prior to benchmark enrollment | Unit test `test_14`, DB consent gate | **SATISFIED** |
| **PRV-02** | Multi-entity PII pseudonymization pipeline (email, phone, ID, address, name) | Unit test `test_15`, regex pipeline | **SATISFIED** |
| **PRV-03** | Right-to-erasure workflow with content purge, score nulling, audio deletion | Unit test `test_16`, filesystem check | **SATISFIED** |
| **PRV-04** | Non-identifying audit logging for consent revocation | Verified `system_settings` audit logs | **SATISFIED** |
| **PRV-05** | Zero third-party trackers, commercial analytics, or external telemetry | Source code inspection of static web assets | **SATISFIED** |

---

## 4. Assessment Validity & Operational Prerequisites

| Item # | Operational Requirement | Responsible Party | Status |
| :---: | :--- | :--- | :---: |
| **OPS-01** | Supervised pilot participant agreement and informed consent form drafted | Lead Project Coordinator | **SATISFIED** |
| **OPS-02** | Independent certified IELTS teachers recruited for double-marking calibration | Academic Director | **PENDING EXECUTION** |
| **OPS-03** | Teacher calibration rubric training session conducted | Academic Director | **PENDING EXECUTION** |
| **OPS-04** | Initial baseline calibration benchmark dataset (minimum 30 human-graded essays) | Academic Team | **PENDING ADMISSION** |
| **OPS-05** | Beta bug triage schedule and escalation workflow defined | QA Lead | **SATISFIED** |

---

## 5. Launch Gate Assessment

All technical security and privacy engineering gates have **PASSED**. The application architecture is fully prepared to support a supervised pilot. The release gate is classified as **READY FOR CONTROLLED BETA PREPARATION**. Real pilot candidate admission may commence as soon as operational staffing (OPS-02 and OPS-03) is completed.
