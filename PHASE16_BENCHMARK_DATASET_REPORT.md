# PHASE 16 BENCHMARK DATASET & PRIVACY MANAGEMENT REPORT
**Project:** IELTS by GAMA  
**Version:** 1.6.0  
**Phase:** 16 — Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit  
**Date:** November 15, 2026  
**Component:** `core/benchmark/benchmark_manager.py`, `data/ielts_gama.db`  

---

## 1. Ethical Governance & Purpose

Machine learning heuristics and automated assessment algorithms require empirical ground-truth benchmark datasets to calibrate accuracy and detect systemic scoring bias. However, assembling candidate writing and speech data introduces critical privacy, copyright, and ethical obligations.

Phase 16 establishes the `BenchmarkManager` under strict GDPR and assessment privacy standards:
1. **Mandatory Candidate Informed Consent:** No learner submission can enter the benchmark repository without explicit, verifiable candidate consent.
2. **Automated PII Anonymization:** Personally Identifiable Information (PII) is scrubbed prior to storage.
3. **Candidate Right to Erasure:** Candidates maintain the absolute right to withdraw consent, resulting in immediate purge from calibration datasets.
4. **Zero-Fabrication Integrity:** The repository contains zero synthetic or fabricated learner essays, transcripts, or marks.

---

## 2. Technical Architecture & Privacy Safeguards

### 2.1 Consent Gate Enforcement
When enrolling a submission via `BenchmarkManager.enroll_benchmark_submission()`:
```python
if not candidate_consent:
    raise ValueError("Candidate consent is mandatory for benchmark dataset inclusion.")
```
If `candidate_consent` is missing or false, the operation is rejected immediately. No record is created.

### 2.2 Automated PII Scrubbing Engine
Before persisting text to `benchmark_records`, the engine applies regex filters to sanitize learner inputs:
- **Email Addresses:** Replaced with `[EMAIL_REDACTED]`.
- **Phone Numbers:** Replaced with `[PHONE_REDACTED]`.
- **Honorifics & Common Name Formats:** Salutations (e.g., `Mr. John Smith`, `Dr. Sarah`) replaced with `[NAME_REDACTED]`.
- **Learner IDs:** Candidate database primary keys are stripped; benchmark records use randomly generated UUIDs (`benchmark_id`) decoupled from learner accounts.

### 2.3 Storage Architecture (`benchmark_records` Table)
```sql
CREATE TABLE IF NOT EXISTS benchmark_records (
    benchmark_id TEXT PRIMARY KEY,
    skill TEXT NOT NULL,
    anonymized_text TEXT NOT NULL,
    audio_path TEXT,
    human_consensus_band REAL,
    human_criteria_scores TEXT,
    ai_predicted_band REAL,
    ai_criteria_scores TEXT,
    algorithm_version TEXT,
    consent_granted INTEGER DEFAULT 1,
    withdrawn_at TEXT,
    created_at TEXT NOT NULL
);
```

### 2.4 Right to Erasure / Consent Withdrawal
In compliance with data protection laws, learners may revoke consent at any time via `/api/benchmark/withdraw`:
- The engine marks `consent_granted = 0` and records `withdrawn_at = ISO_TIMESTAMP`.
- The `anonymized_text` is overwritten with `[CONSENT_WITHDRAWN_BY_CANDIDATE]`.
- Human and AI score fields are nulled.
- The record is permanently disqualified from the Assessment Calibration Engine.

---

## 3. Empirical Test Evidence

Automated validation in `tests/test_phase16_beta_toolkit.py`:
- `test_benchmark_anonymization_and_consent_withdrawal`:
  1. Attempted to enroll a submission with `candidate_consent=False`. Verified that `ValueError` was raised.
  2. Enrolled a submission containing `john.doe@example.com` and `+1-555-0199` with `candidate_consent=True`.
  3. Verified that the stored `anonymized_text` contained `[EMAIL_REDACTED]` and `[PHONE_REDACTED]`.
  4. Executed `withdraw_consent(benchmark_id)`.
  5. Verified that `consent_granted` was 0, `withdrawn_at` was populated, and text was purged.

---

## 4. Current Dataset Volume & Zero-Fabrication Audit

- **Active Benchmark Records:** $N = 0$.
- **Synthetic Records Seeded:** 0.
- **Fabricated Examiner Marks:** 0.

As mandated by Phase 16 guidelines, the benchmark dataset starts at zero records. The database is primed to collect real candidate submissions as participants enter the beta pilot cohorts.
